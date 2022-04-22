from datetime import datetime
from time import strptime, strftime

from django import forms
from django.forms import TextInput, NumberInput, Textarea, Select
from django.utils.timezone import localtime, now

from investor.models import ShareHolder, InvestHistory


class InvestorForm(forms.ModelForm):
    class Meta:
        model = ShareHolder
        fields = ['name', 'phone_no', 'address', 'joining_date']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'required': True}),
            'phone_no': NumberInput(attrs={'class': 'form-control'}),
            'address': Textarea(attrs={'class': 'form-control', 'required': False}),
        }

    def __init__(self, *args, **kwargs):
        super(InvestorForm, self).__init__(*args, **kwargs)
        self.fields['joining_date'] = forms.DateField(input_formats=['%d/%m/%Y'],
                                                      widget=forms.DateInput(
                                                          attrs={'class': 'form-control datepicker-readonly', 'id': 'datepicker',
                                                                 'data-toggle': 'datepicker', 'readonly': True,
                                                                 'value': datetime.strftime(localtime(now()),
                                                                                            '%d/%m/%Y'),
                                                                 'required': True},
                                                          format='%d/%m/%Y'), )


class InvestForm(forms.ModelForm):
    class Meta:
        model = InvestHistory
        fields = ['amount']
        widgets = {
            'amount': NumberInput(attrs={'class': 'form-control'})
        }
