from django.urls import path
from .views.common_views import *
urlpatterns = [
    path('countries/', get_all_country),
    path('states/<int:country_id>/', get_all_state),
    path('cities/<int:country_id>/', get_all_city),
    path('areas/<int:country_id>/', get_all_area),
    path('degrees/', get_all_degrees)
]
