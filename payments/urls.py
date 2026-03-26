from django.urls import path
from .views import initiate_payment, mpesa_callback

urlpatterns = [
    path("stkpush/", initiate_payment),
    path("callback/", mpesa_callback),
]