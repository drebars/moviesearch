from django_filters import rest_framework as filters
from .models import Movie



class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass

class MovieFilter(filters.FilterSet):
    category = CharFilterInFilter(field_name='category__name', lookup_expr='in')
    genres = CharFilterInFilter(field_name='genres__name', lookup_expr='in')
    year = filters.RangeFilter()

    class Meta:
        model = Movie
        fields = ['category', 'genres', 'year']