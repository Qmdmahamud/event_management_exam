from django.shortcuts import render,redirect
from django.http import HttpResponse
from tasks.forms import TaskForm,TaskModelForm,TaskDetailModelForm
from tasks.models import Employee,Task,TaskDetail,Project
from datetime import date
from django.utils.timezone import now
from django.db.models import Q,Count,Max,Min,Avg
from django.contrib import messages
# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.forms import AuthenticationForm
# from .forms import SignUpForm

# Create your views here.
def home(request):
    # return HttpResponse("Welcome to the Event Management System ")
    return render(request,"event_base.html")
def event_overview(request):
    return render(request,"event_overview.html")
def manager_dashboard(request):
    
    return render(request,"manager_dashboard.html")

def event_base(request):
    type = request.GET.get('type', 'all')

    
    if request.method == "POST":
        task_form = TaskModelForm(request.POST) 
        if task_form.is_valid():
            task_form.save()
            messages.success(request, "Task created successfully!")
            return redirect('event_base') 
    else:
        task_form = TaskModelForm() 

   
    counts = Task.objects.aggregate(
        total=Count('id'),
        completed=Count('id', filter=Q(status='COMPLETED')),
        in_progress=Count('id', filter=Q(status='IN_PROGRESS')),
        upcoming_events=Count('id', filter=Q(status='UNCOMPLETED'))
    )

  
    base_query = Task.objects.select_related('details').prefetch_related('assigned_to')

   
    if type == 'completed':
        tasks = base_query.filter(status='COMPLETED')
    elif type == 'in-progress':
        tasks = base_query.filter(status='IN_PROGRESS')
    elif type == 'uncompleted':
        tasks = base_query.filter(status='UNCOMPLETED')
    else:
        tasks = base_query.all()

 
    context = {
        "tasks": tasks,
        "counts": counts,
        "task_form": task_form,
    }

    return render(request, "event_base.html", context) 

def contruct(request):
    return HttpResponse("This is contruct page")
def show_task(request):
    return render(request,'show_task.html')
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
    # employees=Employee.objects.all()
    # form =TaskModelForm(employees)
    task_form =TaskModelForm()
    task_detail_form=TaskDetailModelForm()
    
    if request.method=="POST":
        task_from=TaskModelForm(request.POST)
        task_detail_form=TaskDetailModelForm(request.POST)
        form = TaskModelForm(request.POST)
        if task_form.is_valid() and task_detail_form.is_valid():
            task=task_form.save()
            task_detail=task_detail_form.save(commit=False)
            task_detail.task=task
            task_detail.save()
            messages.success(request,"Task Created Successfully")
            return redirect('create-task')
            
    context={"task_form":task_form,"task_detail_form":task_detail_form}
    return render(request,"task_form.html",context)

def view_task(request):
   
    task_count=Project.objects.annotate(num_task=Count('task'))
    print("✅ task_count =>", task_count) 
    return render(request,"show_task.html",{"task_count":task_count})

def update_task(request,id):
    task=Task.objects.get(id=id)
    # employees= Employees.objects.all()
    # # form =TaskForm(employees={"name":"johon","id":1})
    task_form =TaskModelForm(instance=task)
    if task.details:
        task_detail_form=TaskDetailModelForm(instance=task.details)

    if request.method =="POST":
        task_form =TaskModelForm(request.POST,instance=task)
        task_detail_form=TaskDetailModelForm(request.POST,instance=task.details)
        form = TaskModelForm(request.POST)
        if task_form.is_valid() and task_detail_form.is_valid():
            """for django form data"""
            '''for django  form data'''
            # form.save()
            task=task_form.save()
            task_detail=task_detail_form.save(commit=False)
            task_detail.task=task
            task_detail_form.save()
            # return render(request,'task_form.html',{"form":TaskModelForm(),"message":"task added sucessfully"})
            messages.success(request,"Task Updated Successfully")
            return redirect('update-task',id)
           
    context ={"task_form" : task_form,"task_detail_form":task_detail_form}
    return render(request,"task_form.html",context)

def delete_task(request,id):
    if request.method=='POST':
        task=Task.objects.get(id=id)
        task.delete()
        messages.success(request,'task deleted successfully')
        return redirect('event_manager')
    else:
        messages.success(request,'task deleted Error')
        return redirect('event_manager')
    
