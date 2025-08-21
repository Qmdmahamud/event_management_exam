from django.contrib import admin
from django.urls import path, include
from users.views import group_list,create_group,signup_view,login,logout,activate_user,admin_dashboard,assign_role,no_permission
from . import views

urlpatterns =[
    # path('admin/', admin.site.urls),
    # # path('', include('users.urls')), # users app এর urls
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("fornt_page/",views.fornt_page,name='fornt_page'),
    path('activate/<int:user_id>/<str:token>/',activate_user),
    # path('admin/dashboard/',admin_dashboard,name='admin-dashboard'),
    path('admin_dashboard/',views.admin_dashboard,name='admin_dashboard'),
    path('admin/<int:user_id>/assign-role/',assign_role,name="assign-role"),
    path('admin/group-list/',group_list,name='group-list'),
    path('admin/create-group/',create_group,name='create-group'),
    path('admin/group_list/',group_list,name='group_list'),
    path("no_permission/", views.no_permission, name="no-permission"),
    ] 
