from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User
from accounts.tasks import send_welcome_email

@receiver(post_save, sender=User)
def send_welcome_email_signal(sender, instance: User, created, **kwargs):
    if created:
        send_welcome_email.delay(instance.pk)