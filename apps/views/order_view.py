from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    CreateAPIView,
)
from rest_framework.permissions import  AllowAny, IsAuthenticated
from rest_framework.exceptions import ValidationError
from apps.models import Order, OrderItem
from apps.serializers.order_serializer import OrderSerializer, OrderItemSerializer




class OrderListCreateAPIView(ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderRetrieveAPIView(RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)
    lookup_url_kwarg = "order_id"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderDestroyAPIView(DestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)
    lookup_url_kwarg = "order_id"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_destroy(self, instance):
        if instance.order_items.exists():
            raise ValidationError(
                {"detail": "Order bo‘sh emas"}
            )
        instance.delete()



class OrderItemCreateAPIView(CreateAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        order_id = self.kwargs.get("order_id")

        try:
            order = Order.objects.get(
                id=order_id,
                user=self.request.user
            )
        except Order.DoesNotExist:
            raise ValidationError(
                {"detail": "Order topilmadi"}
            )

        serializer.save(
            order=order,
            user=self.request.user
        )


class OrderItemRetrieveAPIView(RetrieveAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = (IsAuthenticated,)
    lookup_url_kwarg = "item_id"

    def get_queryset(self):
        return OrderItem.objects.filter(
            order__user=self.request.user
        )


class OrderItemUpdateAPIView(UpdateAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = (IsAuthenticated,)
    lookup_url_kwarg = "item_id"

    def get_queryset(self):
        return OrderItem.objects.filter(
            order__user=self.request.user
        )


class OrderItemDestroyAPIView(DestroyAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = (IsAuthenticated,)
    lookup_url_kwarg = "item_id"

    def get_queryset(self):
        return OrderItem.objects.filter(
            order__user=self.request.user
        )
