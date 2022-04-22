from django.db import models
from django.utils.timezone import now

from investor.manager import InvestorManager, InvestHistoryManager, ReleaseHistoryManager


class ShareHolder(models.Model):
    joining_date = models.DateField(default=now)
    name = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=11, unique=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    objects = InvestorManager()


class InvestHistory(models.Model):
    date = models.DateTimeField(default=now)
    amount = models.FloatField()
    share_holder = models.ForeignKey('ShareHolder', related_name='investor_history', on_delete=models.CASCADE)

    objects = InvestHistoryManager()


class ShareHolderReleaseHistory(models.Model):
    releasing_date = models.DateTimeField(default=now)
    joining_date = models.DateTimeField()
    name = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=11)
    address = models.CharField(max_length=255, blank=True, null=True)
    total_investment = models.FloatField(default=0.0)

    objects = ReleaseHistoryManager()
