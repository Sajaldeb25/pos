from django.contrib import admin
from django.contrib.admin import widgets
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from django.utils.translation import gettext as _

from core import models

from user.forms import UserForm, AddNewEmployeeForm


class RichTextEditorWidget(object):
    pass


class UserAdmin(BaseUserAdmin, admin.ModelAdmin):
    add_form = AddNewEmployeeForm
    form = AddNewEmployeeForm
    ordering = ['id']
    list_display = ['code', 'name']
    fieldsets = (
        (None, {"fields": ['code', 'password']}),
        (_('Personal Info'), {
            "fields": ['profile_pic', 'name', 'email', 'phone_no1', 'phone_no2', 'nid', 'gender', 'dob', 'city',
                       'country', 'address']}),
        (_('Permission'),
         {"fields": ['is_active', 'is_staff', 'is_superuser', 'is_admin']}),
        (_('Important Dates'), {"fields": ['last_login']})
    )

    add_fieldsets = (
        (None, {
            'classes': ['wide'],
            'fields': ['name', 'email', 'phone_no1', 'phone_no2', 'nid', 'gender', 'dob', 'city', 'country', 'address']
        }), (_('Permission'),
             {"fields": ['is_active', 'is_staff', 'is_superuser', 'is_admin']}),
    )
    readonly_fields = ['code']

    def formfield_for_dbfield(self, db_field, **kwargs):
        """Over riding the specific form field."""
        print(db_field)
        if db_field.name == 'dob':
            kwargs['widget'] = widgets.AdminDateWidget()
        if db_field.name == 'profile_pic':
            kwargs['widget'] = widgets.AdminDateWidget()
        return super(UserAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    def save_model(self, request, obj, form, change):
        extra_field = form.cleaned_data
        if change:
            obj.save()
        else:
            get_user_model().objects.create_user(**extra_field)


admin.site.register(models.User, UserAdmin)
