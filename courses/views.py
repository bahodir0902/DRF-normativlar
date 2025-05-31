from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from accounts.serializers import UserSerializer
from courses.serializers import CourseSerializer, CategorySerializer, CourseUpdateSerializer
from courses.models import Course, Category


class AddCategoryAPIView(APIView):
    def post(self, request):
        category = CategorySerializer(data=request.data)
        category.is_valid(raise_exception=True)
        category.save()
        return Response(category.data)


class CourseModelViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by('-created_at')
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.action in ['update']:
            return CourseUpdateSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(methods=['get'], detail=True)
    def owner_info(self, request, pk=None):
        course = self.get_object()
        user = course.owner
        serializer = UserSerializer(user)
        return Response(serializer.data)


# class CourseViewSet(mixins.ListModelMixin,
#                     mixins.RetrieveModelMixin,
#                     mixins.CreateModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     viewsets.GenericViewSet):
#     queryset = Course.objects.all().order_by('-created_at')
#     serializer_class = CourseSerializer


# class CourseViewSet(viewsets.ViewSet):
#     def get_permissions(self):
#         if self.action in ['create', 'update', 'destroy']:
#             return [IsAuthenticated()]
#         return [AllowAny()]
#
#
#     def list(self, request):
#         courses = Course.objects.all().order_by('-created_at')
#         serializers = CourseSerializer(courses, many=True)
#         return Response(serializers.data)
#
#     def retrieve(self, request, pk=None):
#         course = get_object_or_404(Course, pk=pk)
#         serializer = CourseSerializer(course)
#         return Response(serializer.data)
#
#     def create(self, request):
#         user = request.user
#         serializer = CourseSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save(owner=user)
#         return Response({"success": True})
#
#
#     def update(self, request, pk=None):
#         course = get_object_or_404(Course, pk=pk)
#         serializer = CourseSerializer(course, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({"success": True})
#
