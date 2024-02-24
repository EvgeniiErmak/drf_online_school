# drf_online_school/urls.py
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('materials/', include('materials.urls')),
]
