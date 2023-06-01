from django.urls import path
from .views.company_view import CompanyView
urlpatterns = [
    path('all/', CompanyView.as_view()),
]
