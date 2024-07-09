from django.contrib import admin
from django.urls import path, include
from .health_check import health_check


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('', health_check, name='health_check'),
]
