from django_filters import rest_framework
from courses.models import Course

class CourseFilter(rest_framework.FilterSet):
    category = rest_framework.NumberFilter(field_name='category__id')
    owner = rest_framework.NumberFilter(field_name='owner__id')

    price_min = rest_framework.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = rest_framework.NumberFilter(field_name='price', lookup_expr='lte')
    price_range = rest_framework.RangeFilter(field_name='price')

    created_after = rest_framework.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = rest_framework.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    created_date = rest_framework.DateFilter(field_name='created_at', lookup_expr='date')

    title_contains = rest_framework.CharFilter(field_name='title', lookup_expr='icontains')
    description_contains = rest_framework.CharFilter(field_name='description', lookup_expr='icontains')

    category_name = rest_framework.CharFilter(field_name='category__name', lookup_expr='iexact')
    owner_first_name = rest_framework.CharFilter(field_name='owner__first_name', lookup_expr='icontains')

    class Meta:
        model = Course
        fields = {
            'title': ["exact", "icontains", "startswith"],
            "price": ['exact', "gte", "lte"],
            "category": ['exact'],
            "owner": ['exact'],
            'created_at': ['exact', 'gte', 'lte', 'date']
        }