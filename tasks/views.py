from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("Welcome to the Event Management System ")
def contruct(request):
    return HttpResponse("This is contruct page")
def show_task(request):
    return HttpResponse("This is Task Page")
