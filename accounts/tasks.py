from datetime import timedelta
from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from decouple import config
from accounts.models import User

@shared_task
def send_welcome_email(user_id):
    try:
        user = User.objects.get(id=user_id)

        send_mail(
            subject="Welcome to our platform",
            message=f"HI {user.first_name or user.email}!\n"
            f"XULASS XUSH KELIBSIZ",
            from_email=config("EMAIL_HOST_USER"),
            recipient_list=[user.email],
            fail_silently=False
        )
        return f"Welcome email sent to {user.email}"
    except User.DoesNotExist:
        return "User doesn\'t exists"
    except Exception as e:
        return f"Error occurred: {e}"

@shared_task
def log_user_statistics():
    total_users = User.objects.all().count()

    thirty_days_ago = timezone.now() - timedelta(days=30)
    active_users = User.objects.filter(last_login__gte=thirty_days_ago).count()

    today = timezone.now().date()
    new_users_today = User.objects.filter(date_joined__date=today).count()

    print(f"\n\n\t\t\t\t ---- USER STATISTICS ----")
    print(f"Total: {total_users} users")
    print(f"Active (30d): {active_users} users")
    print(f"New today: {new_users_today} users")