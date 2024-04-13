import django_filters
from .models import *

class monFilter(django_filters.FilterSet):
    keyword=django_filters.filters.CharFilter(field_name='name',lookup_expr="icontains")
    maxP=django_filters.filters.NumberFilter(field_name='price',lookup_expr='lte')
    minP=django_filters.filters.NumberFilter(field_name='price',lookup_expr='gte')

    class Meta:
    
        model = Produit
        fields= ('bland','price','category','keyword','maxP','minP')