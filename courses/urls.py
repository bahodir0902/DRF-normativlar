from rest_framework.routers import DefaultRouter
from django.urls import path
from courses.views import *

router = DefaultRouter()
router.register('', CourseModelViewSet, basename='courses')

urlpatterns = [
    # path("list/", CourseViewSet.as_view({"get": "list"}), name="courses_list")
    path('add-category/', AddCategoryAPIView.as_view(), name="add_category"),
] + router.urls