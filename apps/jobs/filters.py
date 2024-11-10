import django_filters
from .models import Job


class JobFilter(django_filters.FilterSet):
    job_name = django_filters.CharFilter(lookup_expr='icontains')
    location = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Job
        fields = ('job_name', 'location')