from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    # return HttpResponse("Welcome to the Event Management System ")
    return render(request,"home.html")
def manager_dashboard(request):
    return render(request,"manager_dashboard.html")
def event_base(request):
    return render(request,"event_base.html")
def contruct(request):
    return HttpResponse("This is contruct page")
def show_task(request):
    return HttpResponse("This is Task Page")
def show_specific_task(request,id):
    print("Id",id)
    print("Id type",type(id))
    return HttpResponse(f"This is specific_task id {id}")
def test(request):
    context ={
        "name":["mahamud","hasan","noman"]
    }
    return render(request,'test.html',context)


def create_task(request):
    return render(request,"task_form.html")

