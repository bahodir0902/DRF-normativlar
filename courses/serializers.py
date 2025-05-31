from courses.models import Course, Category
from accounts.models import User
from accounts.serializers import UserSerializer
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent_category']
        extra_kwargs = {
            'id': {"read_only": True}
        }

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'category', 'price', 'created_at', 'updated_at']
        extra_kwargs = {
            'id': {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True}
        }

class CourseUpdateSerializer(CourseSerializer):
    class Meta(CourseSerializer.Meta):
        fields = ['title', 'description', 'category', 'price']
        extra_kwargs = {
            "title": {"required": False},
            "description": {"required": False},
            "category": {"required": False},
            "price": {"required": False},
        }

