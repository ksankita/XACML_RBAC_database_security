from django.urls import path
from .views import evaluate_access

urlpatterns = [
    path('', evaluate_access, name='home'),
    path('evaluate/', evaluate_access, name='evaluate_access'),
]
