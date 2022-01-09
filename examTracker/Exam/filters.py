import django_filters
from django_filters import DateFilter
from .models import *
from django_filters import DateRangeFilter, DateFilter, DateTimeFilter
from django.contrib.auth import get_user_model


class ExamFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="date", lookup_expr='gte')
    end_date = DateFilter(field_name="date", lookup_expr='lte')
    date_range = DateRangeFilter(field_name='date', label='date range')

    class Meta:
        model = Exam
        fields = '__all__'


class CourseFilter(django_filters.FilterSet):
    class Meta:
        model = Course
        fields = '__all__'


class RoomFilter(django_filters.FilterSet):
    class Meta:
        model = Room
        fields = '__all__'
