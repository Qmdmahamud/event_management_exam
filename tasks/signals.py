from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Participant

@receiver(post_save, sender=Participant)
def send_rsvp_email(sender, instance, created, **kwargs):
    if created and instance.rsvp:   # ✅ শুধুমাত্র নতুন RSVP হলে
        subject = f"RSVP Confirmation for {instance.event.title}"
        message = f"Hi {instance.user.username},\n\nYou have successfully RSVP’d for {instance.event.title}."
        send_mail(subject, message, "noreply@myevents.com", [instance.user.email])
