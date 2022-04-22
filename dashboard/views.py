from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.utils.timezone import now, localtime
from django.views import View
from django.views.generic import TemplateView

from core.models import User
from product.models import ProductVariant, Order, OrderedItem, OtherCost


class DashboardView(LoginRequiredMixin, TemplateView):
    login_url = 'user:login'
    redirect_field_name = 'redirect_to'
    template_name = "dashboard/dashboard.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return redirect('user:login')
        if not request.user.is_superuser and not request.user.is_admin:
            self.template_name = 'dashboard/seller_dashboard.html'
        return super(DashboardView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        if self.request.user.is_seller:
            kwargs['seller_data'] = User.objects.calculate_seller_performance_curmonth(self.request.user.code)
        else:
            net_stock = ProductVariant.objects.net_stock()
            net_order = Order.objects.net_order()
            net_sold_item = OrderedItem.objects.net_sold_item()
            net_profit_and_revenue = OrderedItem.objects.calculate_net_profit_and_revenue()
            net_profit_and_revenue_current_month = list(
                OrderedItem.objects.calculate_net_profit_and_revenue_current_month())
            order_month_statics = list(Order.objects.order_statistics_month())
            current_month_statics = []
            flag = 0
            for i in range(1, int(localtime(now()).day) + 1):
                if flag < len(net_profit_and_revenue_current_month) and net_profit_and_revenue_current_month[flag][
                    'order__ordered_date__day'] is i and order_month_statics[flag]['ordered_date__day'] is i:
                    net_profit_and_revenue_current_month[flag]['order'] = order_month_statics[flag]['total_order']
                    current_month_statics.append(net_profit_and_revenue_current_month[flag])
                    flag += 1
                else:
                    current_month_statics.append(
                        {'order__ordered_date_day': i, 'net_profit': 0, 'net_revenue': 0, 'total_item': 0, 'order': 0})

            kwargs['net_stock'] = net_stock['net_stock']
            kwargs['net_order'] = net_order['net_order']
            kwargs['semi_paid_order'] = net_order['semi_paid_order']
            kwargs['full_paid_order'] = net_order['full_paid_order']
            kwargs['net_sold_item'] = net_sold_item['net_sold_item']
            kwargs['net_profit'] = net_profit_and_revenue['net_profit']
            kwargs['net_revenue'] = net_profit_and_revenue['net_revenue']
            kwargs['sell_cost'] = net_profit_and_revenue['net_revenue'] - net_profit_and_revenue['net_profit']
            kwargs['total_due'] = net_order['total_due']
            kwargs['current_month_revenue_profit'] = current_month_statics
            kwargs['all_year_month_statistics'] = OrderedItem.objects.calculate_profit_revenue_all_month()
        return super().get_context_data(**kwargs)
