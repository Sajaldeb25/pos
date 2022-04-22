from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('login/', views.GetLoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('add_employee/', views.AddEmployeeView.as_view(), name="add_employee"),
    path('employee_list/', views.EmployeeListView.as_view(), name="employee_list"),
    path('deactivate_employees/', views.DeactivateEmployeeView.as_view(), name="deactivate_employees"),
    path('employee_details/<slug:code>/', views.UserDetails.as_view(), name="user_details"),
]
