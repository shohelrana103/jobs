from django.urls import path
from .views.job_view import *
urlpatterns = [
    path('categories/', get_job_category),
    path('get/<int:category_id>/', get_job_by_category),
    path('details/<int:job_id>/', get_job_detail),
    path('get/industry/<int:industry_id>/', get_job_by_industry),
]
