from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from notifications.serializers import ListNotificationSerializer
from notifications.models import Notification
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet


class MyNotifications(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Notification.objects.all()
    serializer_class = ListNotificationSerializer
    def list(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_staff:
            notifications = self.get_queryset()
            serializer = ListNotificationSerializer(notifications, many=True)
            return Response(serializer.data)

        notifications = Notification.objects.filter(user=request.user)
        serializer = ListNotificationSerializer(notifications, many=True)
        return Response(serializer.data)