from django.urls import path
from users.views import api

urlpatterns = [
    path('', api.urls),
]
