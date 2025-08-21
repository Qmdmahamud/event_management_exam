from django.db import models
# from tasks.forms import TaskDetailModelForm
from django.db.models.signals import post_save, pre_save, m2m_changed, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
# from django.db import models
from django.contrib.auth.models import User

from datetime import date

# Create your models here.
class Employee(models.Model):
    name=models.CharField(max_length=250)
    email=models.EmailField(unique=True)

    def __str__(self):
        return self.name

# project = Project.objects.create(name="Test Project", start_date="2024-01-01")
# emp = Employee.objects.create(name="Hasan", email="hasan@example.com")
class Task(models.Model):
    STATUS_CHOICES=[
        ('COMPLETED','Completed'),
        ('IN_PROGRESS','In_progress'),
        ('UNCOMPLETED','UNCOMPLETED')
    ]
    project=models.ForeignKey(
        "Project",
        on_delete=models.CASCADE,
        default=1
    )
    assigned_to=models.ManyToManyField('Employee',related_name='tasks')
    # Project=models.ForeignKey("Project",on_delete=models.CASCADE)
    title =models.CharField(max_length=250)
    description=models.TextField()
    due_date=models.DateField()
    status=models.CharField(max_length=15,choices=STATUS_CHOICES,default="UNCOMPLETED")
    is_completed=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class TaskDetail(models.Model):
    HIGH='H'
    MEDIUM='M'
    LOW='L'
    PRIORITY_OPTIONS=(
        ('HIGH','High'),
        ('MEDIUM','Medium'),
        ('LOW','Low')
    )
    # task=models.OneToOneField(Task,on_delete=models.DO_NOTHING,related_name='details,')
    # std_id=models.CharField(max_length=200,primary_key=True)
    task=models.OneToOneField('Task',on_delete=models.CASCADE,related_name='details')
    assigned_to=models.CharField(max_length=100)
    asset=models.ImageField(upload_to='task_asset',blank=True,null=True)
    priority=models.CharField(max_length=6,choices=PRIORITY_OPTIONS,default='L')
    notes=models.TextField(blank=True,null=True)

    def __str__(self):
        return f"Details form Task{self.task.title}"
    
# from django.db import models
# from django.contrib.auth.models import User

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    image = models.ImageField(upload_to="events/", default="events/default.jpg")  # ✅ image field

    def __str__(self):
        return self.title


class Participant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="participants")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rsvp = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"


class Project(models.Model):
    title=models.CharField(max_length=100,default="Untitled Project")
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True,null=True)
    start_date=models.DateField()

    def __str__(self):
        return self.name



@receiver(m2m_changed, sender=Task.assigned_to.through)
def notify_employees_on_task_creation(sender, instance, action, **kwargs):
    if action == 'post_add':
        print(instance, instance.assigned_to.all())
        assigned_emails = [emp.email for emp in instance.assigned_to.all()]
        print("Checking....", assigned_emails)
        send_mail(
            "New Task Assigned",
            f"You have been assigned to the task: {instance.title}",
            "slashupdates@gmail.com",
            assigned_emails,
            fail_silently=False,
        )

@receiver(post_delete, sender=Task)
def delete_associate_details(sender, instance, **kwargs):
    if instance.details:
        print(isinstance)
        instance.details.delete()
        print("Deleted successfully")