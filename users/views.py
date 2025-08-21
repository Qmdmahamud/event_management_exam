# from django.shortcuts import render
from django.utils import timezone

# Create your views here.
from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth.models import User,Group
# from users.forms import CustomRegistrationForm,
from django.contrib import messages
from users.forms import LoginForm
from django.contrib.auth.tokens import default_token_generator
from .forms import SignUpForm
from users.forms import RegisterFrom,CustomRegistrationForm,AssignedRoleForm,CreateGroupForm
from django.contrib.auth.decorators import login_required,user_passes_test

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render

def superuser_check(user):
    return user.is_superuser   # শুধু superuser ঢুকতে পারবে

# @user_passes_test(superuser_check, login_url='/users/no_permission/')
# def admin_dashboard(request):
#     return render(request, "admin/dashboard.html")

def is_admin(user):
    return user.groups.filter(name='Admin').exists()
# Signup
def signup_view(request):
    form=CustomRegistrationForm()
    if request.method == "POST":

        # form = SignUpForm(request.POST)
        form =CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active=False
            user.save()
            messages.success(request,"A conformation mail was sent your email , please cheak your email")
            return redirect("login")
        else:
            print("Form is not valid")
            messages.error(request, "Form is not valid. Please fix the errors below.")
    # else:
        #     login(request, user) 
        #     return redirect("fornt_page") 
        # form = SignUpForm()
    return render(request, "users/login.html", {"form": form})


# Login
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("fornt_page")
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})


# Logout
@login_required
def logout_view(request):
    if request.method=="POST":
        logout(request)
        return redirect("login")

# @user_passes_test(superuser_check, login_url='/users/no_permission/')
@user_passes_test(superuser_check,login_url='no-permission')
def admin_dashboard(request):
    users=User.objects.all()
    return render(request,'admin/dashboard.html',{"users":users})
def fornt_page(request):
    # fornt_page(request)
    # return render(request, "home.html", {"year": timezone.now().year})
    return render(request,"users/fornt_page.html")

def activate_user(request,user_id,token):
    try:
        user=User.objects.get(id=user_id)
        if default_token_generator.check_token(user,token):
            user.is_active=True
            user.save()
            return redirect("login")
        else:
            return HttpResponse('Invalid id or token')
    except User.DoesNotExist:
        return HttpResponse('User not found')
    

@user_passes_test(superuser_check,login_url='no-permission')
def assign_role(request,user_id):
    user=User.objects.get(id=user_id)
    form=AssignedRoleForm()

    if request.method=='POST':
        form=AssignedRoleForm(request.POST)
        if form.is_valid():
            role=form.cleaned_data.get('role')
            if role:
                user.groups.clear()
                user.groups.add(role)
                messages.success(request,f"User {user.username} has been assigned to the {role.name} role")
                return redirect('admin_dashboard')
    return render(request,'admin/assign_role.html',{"form":form})

@user_passes_test(superuser_check,login_url='no-permission')
def create_group(request):
    form=CreateGroupForm()
    if request.method=='POST':
        form=CreateGroupForm(request.POST)
        if form.is_valid():
            group=form.save()
            messages.success(request,f'Group {group.name} has been created successfully')
            return redirect('create-group')
    return render(request,'admin/create_group.html',{"form":form})

@user_passes_test(superuser_check,login_url='no-permission')
def group_list(request):
    groups=Group.objects.prefetch_related("permissions").all()
    return render(request,'admin/group_list.html',{'groups':groups})

# from django.shortcuts import render

def no_permission(request):
    return render(request,"admin/no_permission.html")
