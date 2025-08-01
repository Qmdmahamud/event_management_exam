from django.contrib import admin
from .models import Employee,Project,Task,TaskDetail

admin.site.register(Employee)
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(TaskDetail)


