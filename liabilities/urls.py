from django.urls import path

from liabilities import views

app_name = 'liabilities'
urlpatterns = [
    path('liabilities', views.Liabilities.as_view(), name='liabilities'),
    path('liability_details/<int:liability_id>', views.LiabilityDetails.as_view(), name='liability_details'),
]
