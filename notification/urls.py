from django.urls import path
from .views.company_device_token_view import *
from .views.worker_device_token_view import *
urlpatterns = [
    path('get/company/device/token/<int:company_id>/', CompanyDeviceTokenView.as_view()),
    path('set/company/device/token/', CompanyDeviceTokenView.as_view()),
    path('get/worker/device/token/<int:worker_id>/', WorkerDeviceTokenView.as_view()),
    path('set/worker/device/token/', WorkerDeviceTokenView.as_view()),

]
