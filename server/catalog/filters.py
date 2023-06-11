from django.db.models import Q

from django_filters.rest_framework import CharFilter, FilterSet

from .models import Wine


class WineFilterSet(FilterSet):
    query = CharFilter(method='filter_query')

    def filter_query(self, queryset, name, value):
        search_query = Q(
            Q(variety__search=value) |
            Q(winery__search=value) |
            Q(description__search=value)
        )
        return queryset.filter(search_query)

    class Meta:
        model = Wine
        fields = ('query', 'country', 'points',)
