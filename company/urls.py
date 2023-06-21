from django.urls import path
from .views.company_view import *
from .views.industry_view import *
urlpatterns = [
    path('details/<company_id>/', CompanyView.as_view()),
    path('all/', get_all_company),
    path('all/industry/', get_all_industry),
    path('update/profile/', company_profile_update),
    path('jobs/<int:company_id>/', get_all_job_by_company),
    path('job/applied/candidate/<int:company_id>/<int:job_id>/', get_applied_candidate),
    path('candidate/shortlist/', company_make_candidate_shortlist),
    path('get/shortlisted/candidate/<int:company_id>/<int:job_id>/', get_shortlisted_candidate),
]
