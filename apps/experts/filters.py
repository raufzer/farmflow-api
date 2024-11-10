import django_filters
from .models import Expert


class ExpertFilter(django_filters.FilterSet):
    expert_job = django_filters.CharFilter(lookup_expr='icontains')
    location = django_filters.CharFilter(lookup_expr='icontains')
    studies_degree = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Expert
        fields = ('expert_job', 'location', 'studies_degree')