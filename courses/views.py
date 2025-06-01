from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from accounts.serializers import UserSerializer
from courses.serializers import CourseSerializer, CategorySerializer, CourseUpdateSerializer
from courses.models import Course, Category
from courses.pagination import *
from courses.filters import CourseFilter
from courses.permissions import IsAdminUser

class AddCategoryAPIView(APIView):
    def post(self, request):
        category = CategorySerializer(data=request.data)
        category.is_valid(raise_exception=True)
        category.save()
        return Response(category.data)


class CourseModelViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by('-created_at')
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CourseFilter

    search_fields = [
        'title',
        'description',
        'category__name',
        'owner__first_name',
    ]

    ordering_fields = [
        'id', 'title', 'price', 'created_at', 'updated_at',
        'category__name', 'owner__first_name'
    ]

    ordering = ['-created_at']

    pagination_class = PageNumberPagination
    # pagination_class = CourseLimitOffsetPagination
    # pagination_class = CourseCursorPagination

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsAuthenticated()]
        if self.action in ['my_courses']:
            return [IsAdminUser()]
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

    @action(methods=['get'], detail=False)
    def my_courses(self, request):
        queryset = self.filter_queryset(
            Course.objects.filter(owner=request.user).select_related('category', "owner")
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

