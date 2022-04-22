from datetime import datetime
from django.db import models, transaction, DatabaseError
from django.db.models import Prefetch, Sum, F, Value, Count, FloatField, ExpressionWrapper, DurationField, IntegerField
from django.db.models.functions import Coalesce, Extract, ExtractMonth, Cast, TruncDate, ExtractDay
from django.utils.timezone import localtime, now


class ReleaseHistoryManager(models.Manager):
    def get_all_release_history(self):
        data = self.model.objects.all()
        return data

    def delete_release_history(self, id):
        try:
            self.model.objects.get(id=id).delete()
        except DatabaseError as e:
            raise DatabaseError("Technical Problem while deleting release history")
        return True


class InvestorManager(models.Manager):
    def all_investor(self):
        data = self.model.objects.prefetch_related(
            Prefetch(
                'investor_history',
                to_attr='invest_history'
            )
        ).annotate(
            total_invest=Coalesce(Sum(F('investor_history__amount')), Value(0)))
        return data

    def investor_details(self, id):
        data = self.model.objects.filter(id=id).prefetch_related(
            Prefetch(
                'investor_history',
                to_attr='invest_history'
            )
        ).annotate(
            total_invest=Coalesce(Sum(F('investor_history__amount')), Value(0))).first()
        return data

    @transaction.atomic
    def create_investor(self, investor_data):
        try:
            new_investor = self.model(name=investor_data['name'], phone_no=investor_data['phone_no'],
                                      address=investor_data['address'], joining_date=investor_data['joining_date'])
            new_investor.save(using=self.db)
            from investor.models import InvestHistory
            invest = InvestHistory(share_holder=new_investor, amount=investor_data['amount'])
            invest.save(using=self.db)
        except DatabaseError as e:
            raise DatabaseError("Technical problem to create investor")
        return new_investor

    @transaction.atomic
    def update_investor(self, id, form_data):
        try:
            old_investor = self.model.objects.get(id=id)
            old_investor.name = form_data['name']
            old_investor.phone_no = form_data['phone_no']
            if 'address' in form_data:
                old_investor.address = form_data['address']
            old_investor.save(using=self.db)
        except DatabaseError as e:
            raise DatabaseError('Technical problem while updating shareholder')
        return True

    @transaction.atomic
    def release_investor(self, id):
        try:
            investor = self.model.objects.filter(id=id).prefetch_related('investor_history').annotate(
                total_invest=Coalesce(Sum(F('investor_history__amount')), Value(0))).first()
            from investor.models import ShareHolderReleaseHistory
            release_investor = ShareHolderReleaseHistory(joining_date=investor.joining_date, name=investor.name,
                                                         phone_no=investor.phone_no, address=investor.address,
                                                         total_investment=investor.total_invest)
            release_investor.save(using=self.db)
            investor.delete()
        except DatabaseError as e:
            raise DatabaseError("Technical problem to releasing shareholder")

        return True


class InvestHistoryManager(models.Manager):
    def create_invest(self, form_data):
        try:
            new_invest = self.model(**form_data)
            new_invest.save(using=self.db)
        except DatabaseError as e:
            raise DatabaseError("Technical problem occurred while adding new invest")

        return new_invest

    def release_invest(self, invest_id):
        try:
            invest = self.model.objects.filter(id=invest_id).select_related('share_holder').first()
            from investor.models import ShareHolderReleaseHistory
            release_invest = ShareHolderReleaseHistory(joining_date=invest.share_holder.joining_date,
                                                       name=invest.share_holder.name,
                                                       phone_no=invest.share_holder.phone_no,
                                                       address=invest.share_holder.address,
                                                       total_investment=invest.amount)
            release_invest.save(using=self.db)
            invest.delete()
        except DatabaseError as e:
            raise DatabaseError("Error occurred while releasing invest")
        return True

    def calculate_shareholder_profit(self, net_profit, invest_history, invest_max_date=now()):
        if not isinstance(invest_history, list):
            raise ValueError("invest_history must be a list")
        invest_max_date = invest_max_date.replace(day=1)
        # print(todayDate.replace(day=1)
        total_investment = self.model.objects.filter(date__lt=invest_max_date).aggregate(
            total_investor=Count('id'),
            total_investment=Sum(F('amount') * (
                ExpressionWrapper(ExtractDay(invest_max_date - TruncDate(F('date'))), output_field=IntegerField())),
                                 output_field=FloatField())
        )
        sum = 0
        for invest in invest_history:
            if invest.date < invest_max_date:
                profit = (invest.amount * (
                    (datetime.date(invest_max_date) - datetime.date(invest.date)).days) * net_profit) / \
                         total_investment[
                             'total_investment']
                invest.profit = profit
                invest.profit_percent = (profit * 100.00) / net_profit
                sum += profit
            else:
                invest.profit = 0
                invest.profit_percent = 0

        return {'invest_history': invest_history, 'total_profit': sum,
                'total_profit_percent': (sum * 100.0) / net_profit}
