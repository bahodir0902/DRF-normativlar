from django.urls import path
from notifications.views import MyNotifications

app_name = "notifications"
urlpatterns = [
    path('', MyNotifications.as_view({"get": "list"}), name="my_notifications")
]