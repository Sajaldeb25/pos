from django.urls import path

from investor import views

app_name = 'investor'
urlpatterns = [
    path('shareholder_list', views.InvestorList.as_view(), name='investors'),
    path('release_history', views.ReleaseHistory.as_view(), name='release_history'),
    path('shareholder_details/<int:shareholder_id>', views.ShareholderDetails.as_view(), name='shareholder_details'),
]
