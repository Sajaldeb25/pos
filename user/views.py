import copy
import json
from datetime import datetime
from json import JSONEncoder

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db import DatabaseError
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView, FormView, RedirectView
from django.contrib.auth import authenticate, login, logout, get_user_model

from core.models import User
from user.forms import LoginForm

from user.forms import AddNewEmployeeForm


class GetLoginView(FormView):
    template_name = "user/login.html"
    form_class = LoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard:dashboard')
        return super(GetLoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            return redirect('dashboard:dashboard')
        return redirect('user:login')


class LogoutView(RedirectView):
    permanent = True
    query_string = False
    pattern_name = 'user:login'

    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return super().get_redirect_url(*args, **kwargs)


class AddEmployeeView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    permission_required = ('user.view_user',)
    template_name = 'user/create_user.html'
    form_class = AddNewEmployeeForm

    def handle_no_permission(self):
        messages.error(self.request, 'You have no permission')
        return HttpResponseRedirect(reverse('dashboard:dashboard'))

    def form_valid(self, form):
        extra_field = form.cleaned_data
        try:
            user = get_user_model().objects.create_user(**extra_field)
        except DatabaseError:
            return HttpResponse(DatabaseError.message)
        return HttpResponse(user)


class EmployeeListView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = ('user.view_user',)
    template_name = 'user/user_list.html'

    def handle_no_permission(self):
        messages.error(self.request, 'You have no permission')
        return HttpResponseRedirect(reverse('dashboard:dashboard'))

    def get_context_data(self, **kwargs):
        kwargs['users'] = User.objects.get_all_users()
        return super().get_context_data(**kwargs)


class UpdateUserSerializer(JSONEncoder):
    def default(self, obj):
        data = {
            'name': obj.name,
            'email': obj.email,
            'phone_no1': obj.phone_no1,
            'phone_no2': obj.phone_no2,
            'gender': obj.gender,
            'country': obj.country,
            'city': obj.city,
            'profile_pic': obj.profile_pic.url,
            'nid': obj.nid,
            'address': obj.address,
            'is_seller': obj.is_seller,
            'is_admin': obj.is_admin,
            'is_superuser': obj.is_superuser,
            'dob': datetime.strftime(obj.dob, '%d/%m/%Y')
        }
        return data


class UserDetails(LoginRequiredMixin, TemplateView):
    template_name = 'user/user_details.html'

    @staticmethod
    def check_perm(user, code, request):
        if user.code != code and not user.is_admin and not user.is_superuser:
            raise PermissionDenied

        if not User.objects.get(code=code):
            raise Http404('Employee not found')

    def dispatch(self, request, *args, **kwargs):
        user = User.objects.filter(code=kwargs['code'])
        if request.user.is_anonymous:
            return redirect('user:login')
        if user is None:
            raise Http404('Employee not found')
        if request.user.code != kwargs['code'] and not request.user.is_admin and not request.user.is_superuser:
            messages.error(request, 'You have no permission')
            return HttpResponseRedirect(reverse('dashboard:dashboard'))
        return super(UserDetails, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        code = kwargs['code']
        kwargs['user_details'] = User.objects.user_details(code)
        return super().get_context_data(**kwargs)

    def post(self, request, code):
        user = request.user
        if request.is_ajax():
            self.check_perm(user=user, code=code, request=request)
            if 'dlt_code' in request.POST:
                if User.objects.deactivate_user(request.POST['dlt_code']):
                    return JsonResponse("success", status=201, safe=False)
                return JsonResponse("error", status=400, safe=False)
            elif 'act_code' in request.POST:
                if User.objects.activate_user(request.POST['act_code']):
                    return JsonResponse("success", status=201, safe=False)
                return JsonResponse("error", status=400, safe=False)
            elif 'pass_user_code' in request.POST:
                data = request.POST
                user_password = data['old_password']
                new_password = data['new_password']
                if user.check_password(user_password):
                    user = User.objects.filter(code=data['pass_user_code']).first()
                    if user is None:
                        return JsonResponse("Employee not found", status=400, safe=False)
                    user.set_password(new_password)
                    try:
                        user.save()
                    except DatabaseError as e:
                        return JsonResponse("Error occurred while changing password", status=400, safe=False)
                    return JsonResponse("success", status=201, safe=False)
                else:
                    return JsonResponse("Wrong password", status=400, safe=False)

            user = User.objects.get(code=code)
            form = AddNewEmployeeForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                if User.objects.update_user(form):
                    return JsonResponse(json.dumps(user, cls=UpdateUserSerializer), status=200, safe=False)
                return JsonResponse({'db_error': 'Error occurred while updating'}, status=400)
            else:
                return JsonResponse(form.errors, status=400)


class DeactivateEmployeeView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = ('user.view_user',)
    template_name = 'user/deactivate_userlist.html'

    def get_context_data(self, **kwargs):
        kwargs['deactivate_employees'] = User.objects.deactivate_user_list()
        return super().get_context_data(**kwargs)

    def post(self, request):
        if request.is_ajax():
            if request.user.has_perm('delete_user'):
                dlt_user = User.objects.filter(code=request.POST['dlt_user_code']).first()
                if dlt_user is None:
                    return JsonResponse({'permission_denied': "Forbidden 403"}, status=400, safe=False)
                try:
                    dlt_user.delete()
                    return JsonResponse({'success': "Forbidden 403"}, status=201, safe=False)
                except DatabaseError as e:
                    return JsonResponse({'db_error': "Error occurred while deleting"}, status=400, safe=False)
            else:
                return JsonResponse({'permission_denied': "Forbidden 403"}, status=400, safe=False)
