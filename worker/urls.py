from django.urls import path
from .views.worker_view import *
urlpatterns = [
    path('all/', get_all_worker),
    path('details/<int:worker_id>/', get_worker_details)
]
