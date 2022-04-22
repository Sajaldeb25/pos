from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
]
