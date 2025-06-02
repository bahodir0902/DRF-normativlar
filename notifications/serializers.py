from rest_framework import serializers
from notifications.models import Notification
from accounts.serializers import UserSerializer


class ListNotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Notification
        fields = ['id','title', 'message', 'user', 'is_read', 'created_at']
        extra_kwargs = {
            "id": {"read_only": True},
            "created_at": {"read_only": True}
        }