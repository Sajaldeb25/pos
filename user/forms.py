from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.forms import TextInput, PasswordInput, ModelForm, NumberInput, ImageField, FileInput, DateInput, \
    RadioSelect, Select, CheckboxInput

from core.models import User


class UserForm(forms.ModelForm):
    #     class Meta:
    #         model = User
    #         fields = '__all__'
    #
    #     def __init__(self, *args, **kwargs):
    #         super(UserForm, self).__init__(*args, **kwargs)
    #         self.fields['name'].required = True
    #         self.fields['nid'].required = True
    pass


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Code',
                                                       'autofocus': True}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password',
                                                           'autofocus': True}))

    def clean(self):
        if self.cleaned_data['username']:
            user = User.objects.get(code=self.cleaned_data['username'])
            if not user.is_active:
                self.add_error('username', 'This user does not exist')
                raise forms.ValidationError('This user does not exist')
        if authenticate(username=self.cleaned_data['username'], password=self.cleaned_data['password']) is None:
            self.add_error('username', 'Username or password is incorrect')
            raise forms.ValidationError('Username or password is incorrect')


class AddNewEmployeeForm(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'phone_no1', 'phone_no2', 'profile_pic', 'nid', 'gender', 'city', 'country',
                  'address', 'dob', 'is_seller', 'is_admin', 'is_superuser']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'id': 'fullname', 'placeholder': 'Full Name',
                                     'oninput': 'showName()', 'autofocus': True, 'required': True}),
            'email': TextInput(attrs={'class': 'form-control', 'type': 'email', 'placeholder': 'Email'}),
            'phone_no1': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Phone no 1'}),
            'phone_no2': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Phone no 2'}),
            'nid': NumberInput(attrs={'class': 'form-control', 'type': 'number', 'placeholder': 'NID',
                                      'required': True}),
            'city': TextInput(attrs={'class': 'form-control', 'placeholder': 'City', 'required': True}),
            'country': TextInput(attrs={'class': 'form-control', 'placeholder': 'Country', 'required': True}),
            'address': TextInput(attrs={'class': 'form-control', 'placeholder': 'Address', 'required': True}),
            'is_active': CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_admin': CheckboxInput(attrs={'class': 'form-check-input radio'}),
            'is_seller': CheckboxInput(attrs={'class': 'form-check-input radio'}),
            'is_superuser': CheckboxInput(attrs={'class': 'form-check-input radio'})
        }

    def __init__(self, *args, **kwargs):
        super(AddNewEmployeeForm, self).__init__(*args, **kwargs)
        self.fields['nid'].required = True
        self.fields['email'].required = False
        self.fields['dob'].required = True
        self.fields['phone_no2'].required = False
        # self.fields['dob'] = forms.DateField(input_formats=['%d-%m-%Y'])
        self.fields['dob'] = forms.DateField(input_formats=['%d/%m/%Y'],
                                             widget=forms.DateInput(
                                                 attrs={'class': 'form-control', 'placeholder': 'DOB',
                                                        'id': 'datepicker',
                                                        'data-select': 'datepicker', 'readonly': True,
                                                        'required': True},
                                                 format='%d/%m/%Y'), )
        self.fields['profile_pic'] = forms.ImageField(required=False, widget=FileInput(attrs={'id': 'img_input', 'hidden': True,
                                                                              'accept': 'image/*'}))
