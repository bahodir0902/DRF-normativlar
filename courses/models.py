from django.db import models
from accounts.models import User

class Category(models.Model):
    name = models.CharField(max_length=255)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='category')

    class Meta:
        db_table = 'Categories'

    def __str__(self):
        return f"{self.name} category"

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=5, default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Courses"

    def __str__(self):
        return f"{self.title} course"


