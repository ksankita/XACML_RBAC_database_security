from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

def check_access(request):
    return JsonResponse({"message": "Access checked successfully!"})

def index(request):
    return render(request, 'index.html')
# Create your views here.
