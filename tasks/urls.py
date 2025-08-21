from django.urls import path
from . import views
from tasks.views import show_task,show_specific_task,manager_dashboard,event_base,test,create_task,view_task,update_task,delete_task,event_overview

urlpatterns = [
    path('',event_base,name='home'),
    path('show_task/',show_task),
    path('show_task/<int:id>/',show_specific_task),
    path('manager_dashboard/',manager_dashboard),
    path('event_base/',event_base, name="event_manager"),
    path('test/',test),
    path('create_task/',create_task),
    path('view_task/',view_task),
    path('update_task/<int:id>/',update_task,name='update-task'),
    path('delete_task/<int:id>/',delete_task,name='delete-task'),
    path('event_overview/',event_overview,name="event_overview"),
    
   
]
