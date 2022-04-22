from django.shortcuts import render
from django.views.generic import TemplateView


class Liabilities(TemplateView):
    template_name = 'liabilities/liabilities.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class LiabilityDetails(TemplateView):
    template_name = 'liabilities/liability_details.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
