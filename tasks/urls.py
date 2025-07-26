from django.urls import path
from tasks.views import show_task,show_specific_task,manager_dashboard,event_base,test,create_task,view_task,show_task
urlpatterns = [
    path('show_task/',show_task),
    path('show_task/<int:id>/',show_specific_task),
    path('manager_dashboard/',manager_dashboard),
    path('event_base/',event_base),
    path('test/',test),
    path('create_task',create_task),
    path('view_task/',view_task),
    path('show_task/',show_task)
]
