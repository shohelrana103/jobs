from django.urls import path
from .views.company_view import *
from .views.industry_view import *
urlpatterns = [
    path('details/<company_id>/', CompanyView.as_view()),
    path('all/', get_all_company),
    path('all/industry/', get_all_industry),
    path('update/profile/', company_profile_update)
]
