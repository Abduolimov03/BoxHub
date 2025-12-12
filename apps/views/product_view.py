from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny

from apps.filters import ProductFilter
from apps.models import Product, Category, CoffeeAndTea
from apps.pagination import StandardResultsSetPagination
from apps.serializers import ProductModelSerializer, CategoryModelSerializer, CoffeeAndTeaModelSerializer


@extend_schema(
    tags=["Product-Category"],
    description="Mahsulotlar Royhati",
    request=ProductModelSerializer,
)
class ProductListCreateAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    permission_classes = (AllowAny,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
    # permission_classes = (IsAuthenticated,)
    pagination_class = StandardResultsSetPagination


@extend_schema(
    tags=["Product-Category"],
    description="Mahsulotlar Royhati",
    request=CategoryModelSerializer,
)
class CategoryListCreateAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    permission_classes = (AllowAny,)
    # permission_classes = (IsAuthenticated,)
    pagination_class = StandardResultsSetPagination


@extend_schema(
    tags=["Product-Category"],
    description="Coffee & Tea",
    request=CategoryModelSerializer,
)
class CoffeeAndTeaListCreateAPIView(ListCreateAPIView):
    queryset = CoffeeAndTea.objects.all()
    serializer_class = CoffeeAndTeaModelSerializer
    permission_classes = (AllowAny,)
    pagination_class = StandardResultsSetPagination
