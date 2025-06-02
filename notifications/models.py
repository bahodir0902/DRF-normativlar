from django.db import models
from accounts.models import User

class Notification(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Notifications"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.user.email}"
