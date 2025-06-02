from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User
from accounts.tasks import send_welcome_email
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from notifications.models import Notification

@receiver(post_save, sender=User)
def send_welcome_email_signal(sender, instance: User, created, **kwargs):
    if created:
        send_welcome_email.delay(instance.pk)

        channel_layer = get_channel_layer()
        message = f"A new user with {instance.email} has registered"
        Notification.objects.create(
            title="New user Registration",
            message=message,
            user=instance
        )

        async_to_sync(channel_layer.group_send)(
            "superusers",
            {
                "type": "notification_message",
                "message": message
            }
        )