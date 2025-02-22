from django.urls import path
from django.contrib import admin
from .views import index, check_access

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('check_access/', check_access, name='check_access'),
]
