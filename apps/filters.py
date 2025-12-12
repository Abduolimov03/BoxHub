from django_filters import FilterSet, NumberFilter

from apps.models import Product


class ProductFilter(FilterSet):
    category = NumberFilter(field_name="category_id")

    class Meta:
        model = Product
        fields = 'category',
