from . models import Product
import django_filters

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name',lookup_expr='icontains')
    maxprice = django_filters.NumberFilter(field_name='price',lookup_expr='lte')
    # 100 >
    minprice = django_filters.NumberFilter(field_name='price',lookup_expr='gte')
    # 100 <
    class Meta:
        model=Product
        fields = ['id','name','brand']
       
