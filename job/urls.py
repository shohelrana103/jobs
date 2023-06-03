from django.urls import path
from .views.job_view import *
urlpatterns = [
    path('categories/', get_job_category),
    path('get/<category_id>/', get_job_by_category),
    path('details/<job_id>/', get_job_detail),
]
