from django.urls import path
from .views.job_view import *
from .views.company_job_view import *
urlpatterns = [
    path('categories/', get_job_category),
    path('get/<int:category_id>/', get_job_by_category),
    path('details/<int:job_id>/', get_job_detail),
    path('get/industry/<int:industry_id>/', get_job_by_industry),
    path('all/', get_all_job),
    path('all/<int:worker_id>/', get_all_job_worker_id),
    path('types/', get_job_type),
    path('levels/', get_job_levels),
    path('employment/status/', get_job_employment_status),
    path('work/places/', get_job_work_places),
    path('benefits/', get_job_benefits),
    path('cv/receiving/option/', get_job_cv_receiving_options),
    path('create/basic/', create_job_basic_information),
    path('create/requirements/', create_job_requirements),
    path('create/address/', create_job_address),
    path('skills/', get_job_skills),
]
