import copy
import json
from datetime import datetime
from json import JSONEncoder

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.timezone import localtime, now
from django.views.generic import TemplateView

from investor.form import InvestorForm, InvestForm
from investor.models import ShareHolder, InvestHistory, ShareHolderReleaseHistory
from product.models import OrderedItem


class InvestorList(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'investor/investor.html'
    permission_required = ('investor.view_shareholder')

    def handle_no_permission(self):
        messages.error(self.request, 'You have no permission')
        return HttpResponseRedirect(reverse('dashboard:dashboard'))

    def get_context_data(self, **kwargs):
        if self.request.user.has_perm('investor.add_shareholder') and self.request.user.has_perm('investor.add_investhistory'):
            kwargs['investor_form'] = InvestorForm()
            kwargs['invest_form'] = InvestForm()
        kwargs['investors'] = ShareHolder.objects.all_investor()
        return super().get_context_data(**kwargs)

    def post(self, request):
        data = request.POST
        if request.is_ajax():
            if 'dlt_id' in data:
                if not self.request.user.has_perm('investor.delete_shareholder'):
                    return JsonResponse({'permission_denied': 'Permission denied'}, status=400, safe=False)
                if ShareHolder.objects.release_investor(data['dlt_id']):
                    return JsonResponse("success", status=201, safe=False)
                else:
                    return JsonResponse("error", status=400, safe=False)
            else:
                if not self.request.user.has_perm('investor.add_shareholder'):
                    return JsonResponse({'permission_denied': 'Permission denied'}, status=400, safe=False)
                investor_form = InvestorForm(data)
                invest_form = InvestForm(data)
                if not investor_form.is_valid() and not investor_form.is_valid():
                    return JsonResponse([investor_form.errors, invest_form.errors], status=400, safe=False)
                elif not invest_form.is_valid():
                    return JsonResponse(invest_form.errors, status=400)
                elif not investor_form.is_valid():
                    return JsonResponse(investor_form.errors, status=400)
                if investor_form.is_valid() and invest_form.is_valid():
                    investor_data = investor_form.cleaned_data
                    invest_data = invest_form.cleaned_data
                    # This update method is for updating the dict
                    investor_data.update(**invest_data)
                    new_investor = ShareHolder.objects.create_investor(investor_data)
                    new_investor_data = {
                        'id': new_investor.id,
                        'joining_date': datetime.strftime(new_investor.joining_date, '%d/%m/%Y'),
                        'name': new_investor.name,
                        'phone_no': new_investor.phone_no,
                        'address': new_investor.address
                    }
                    return JsonResponse(new_investor_data, status=201, safe=False)
                return JsonResponse("error", status=400, safe=False)


class ReleaseHistory(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'investor/relase_history.html'
    permission_required = ('investor.view_shareholderreleasehistory',)

    def handle_no_permission(self):
        messages.error(self.request, 'You have no permission')
        return HttpResponseRedirect(reverse('dashboard:dashboard'))

    def get_context_data(self, **kwargs):
        kwargs['release_histories'] = ShareHolderReleaseHistory.objects.get_all_release_history()
        return super().get_context_data(**kwargs)

    def post(self, request):
        if request.is_ajax():
            if 'id' in request.POST:
                id = request.POST['id']
            else:
                return JsonResponse("error", status=400, safe=False)
            if not self.request.user.has_perm('investor.view_shareholderreleasehistory'):
                return JsonResponse({'permission_denied': 'Permission denied'}, status=400, safe=False)
            if ShareHolderReleaseHistory.objects.delete_release_history(id):
                return JsonResponse("success", status=201, safe=False)
            else:
                return JsonResponse("error", status=400, safe=False)


class JsonSerializer(JSONEncoder):
    def default(self, obj):
        data = {
            'id': obj.id,
            'amount': obj.amount,
            'date': datetime.strftime(obj.date, '%d/%m/%Y %I:%M %p'),
            'profit': obj.profit,
            'profit_percent': obj.profit_percent
        }
        return data


class ShareholderDetails(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'investor/investor_details.html'
    permission_required = ('investor.view_shareholder',)

    def handle_no_permission(self):
        messages.error(self.request, 'You have no permission')
        return HttpResponseRedirect(reverse('dashboard:dashboard'))

    def get_context_data(self, **kwargs):
        id = kwargs['shareholder_id']
        cur_month = localtime(now()).month
        cur_year = localtime(now()).year
        if cur_month is 1:
            cur_month = 12
            cur_year -= 1
        else:
            cur_month -= 1
        all_month_profit = list(OrderedItem.objects.calculate_profit_revenue_all_month())
        investor_details = ShareHolder.objects.investor_details(id)
        total_profit = 0
        for profit in all_month_profit:
            if profit['order__ordered_date__year'] == now().year and profit[
                'order__ordered_date__month'] == now().month:
                continue
            max_date = now()
            if profit['order__ordered_date__month'] is 12:
                max_date = max_date.replace(year=max_date.year + 1, month=1, day=1)
            else:
                max_date = max_date.replace(month=profit['order__ordered_date__month'] + 1, day=1)

            investor_profit = InvestHistory.objects.calculate_shareholder_profit(net_profit=profit['net_profit'],
                                                                                 invest_history=investor_details.invest_history,
                                                                                 invest_max_date=max_date)
            profit['invest_history'] = json.dumps(copy.deepcopy(investor_profit['invest_history']),
                                                  cls=JsonSerializer)
            # profit['invest_history'] = copy.deepcopy(investor_profit['invest_history'])
            profit['this_month_profit'] = investor_profit['total_profit']
            profit['this_month_profit_percent'] = (investor_profit['total_profit'] * 100.0) / profit['net_profit']
            total_profit += investor_profit['total_profit']
            if profit['order__ordered_date__year'] == cur_year and profit[
                'order__ordered_date__month'] == cur_month:
                investor_details.latest_profit = investor_profit['total_profit']
                investor_details.latest_profit_percent = profit['this_month_profit_percent']

        investor_details.total_earning = total_profit
        if self.request.user.has_perm('investor.add_shareholder') and self.request.user.has_perm('investor.add_investhistory'):
            kwargs['investor_form'] = InvestorForm(initial={
                'name': investor_details.name,
                'phone_no': investor_details.phone_no,
                'address': investor_details.address
            })
            kwargs['invest_form'] = InvestForm()
        kwargs['investor_details'] = investor_details
        kwargs['profit_details'] = all_month_profit

        return super().get_context_data(**kwargs)

    def post(self, request, shareholder_id):
        if request.is_ajax():
            data = request.POST
            investor = None
            if 'id' in data:
                if not self.request.user.has_perm('investor.chane_shareholder'):
                    return JsonResponse({'permission_denied': 'Permission denied'}, status=400, safe=False)
                investor = get_object_or_404(ShareHolder, pk=data['id'])
                investor_form = InvestorForm(data, instance=investor)
            else:
                investor_form = InvestorForm(data)
            if not self.request.user.has_perm('investor.add_investhistory'):
                return JsonResponse({'permission_denied': 'Permission denied'}, status=400, safe=False)
            invest_form = InvestForm(data)
            if 'dlt_id' in data:
                if not self.request.user.has_perm('investor.delete_investhistory'):
                    return JsonResponse({'permission_denied': 'Permission denied'}, status=400, safe=False)
                if InvestHistory.objects.release_invest(data['dlt_id']):
                    return JsonResponse('success', status=201, safe=False)
                else:
                    return JsonResponse('error', status=400, safe=False)
            elif investor_form.is_valid():
                if investor_form.save():
                    return JsonResponse('success', status=201, safe=False)
                else:
                    return JsonResponse('error', status=400, safe=False)
            elif invest_form.is_valid():
                data = invest_form.cleaned_data
                data['share_holder'] = investor
                created_invest = InvestHistory.objects.create_invest(data)
                result = {
                    'id': created_invest.id,
                    'date': datetime.strftime(created_invest.date, '%d/%m/%Y %I:%M %p'),
                    'amount': created_invest.amount
                }
                return JsonResponse(result, status=201)
            else:
                if not investor_form.is_valid() and not invest_form.is_valid():
                    return JsonResponse({'investor_error': investor_form.errors, 'invest_error': invest_form.errors},
                                        status=400)
                elif not invest_form.is_valid():
                    return JsonResponse(invest_form.errors, status=400)
                if not investor_form.is_valid():
                    return JsonResponse(investor_form.errors, status=400)
