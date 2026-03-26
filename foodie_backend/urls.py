from django.contrib import admin
from django.urls import path, include

def home(request):
    from django.http import JsonResponse
    return JsonResponse({"message": "Welcome to the Foodie API!"})

urlpatterns = [
    path('', home),  # Root route
    path('admin/', admin.site.urls),
    path('api/', include('payments.urls')),
]