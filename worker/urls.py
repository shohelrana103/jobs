from django.urls import path
from .views.worker_view import *
urlpatterns = [
    path('all/', get_all_worker),
    path('details/<int:worker_id>/', get_worker_details),
    path('job/apply/', worker_apply_job),
    path('applied/job/<int:worker_id>/', worker_applied_job),
    path('job/shortlist/', worker_shortlist_job),
    path('shortlist/job/<int:worker_id>/', worker_shortlisted_job),
    path('set/experiences/', set_worker_experiences),
    path('upload/resume/', upload_worker_resume),
    path('upload/video/resume/', upload_worker_video_resume),

]
