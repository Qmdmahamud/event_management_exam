from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm,TaskModelForm
from tasks.models import Employee,Task,TaskDetail,Project
from datetime import date
from django.db.models import Q,Count,Max,Min,Avg

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
    employees=Employee.objects.all()
    form =TaskModelForm()
    if request.method=="POST":
        form=TaskModelForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request,'task_form.html',{"form":TaskModelForm(),"message":"Task added succesfully"})
            '''For django form data'''
            # data=form.cleaned_data
            # title=data.get('title')
            # description=data.get('description')
            # due_date=data.get('due_date')
            # assigned_to=data.get('assigned_to')
            
            # task=Task.objects.create(title=title,description=description,due_date=due_date)
            # # task.objects.add()
            # for emp_id in assigned_to:
            #     employee=Employee.objects.get(id=emp_id)
            #     task.assigned_to.add(employee)
            # return HttpResponse("Task Added successfully")
            # print(form.cleaned_data)
    context={"form":form}
    return render(request,"task_form.html",context)

def view_task(request):
    # tasks=Task.objects.all()
    # task_3=Task.objects.get(id=1)
    # tasks=Task.objects.filter(status='UNCOMPLETED')
    # tasks=Task.objects.filter(due_date=date.today())
    # tasks=TaskDetail.objects.exclude(priority="L")
    # tasks=Task.objects.filter(title__icontains="p",status="COMPLETED")
    # tasks=TaskDetail.objects.select_related('task').all()
    # tasks=Task.objects.prefetch_related('assigned_to').all()
    tasks=Project.objects.annotate(num_task=Count('task')).order_by('num_task')
    return render(request,"show_task.html",{"tasks":tasks})

