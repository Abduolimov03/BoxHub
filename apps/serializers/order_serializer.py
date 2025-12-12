from rest_framework import serializers
from apps.models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    sub_amount = serializers.ReadOnlyField()

    class Meta:
        model = OrderItem
        fields = (
            'id',
            'order',
            'product_type',
            'product_id',
            'quantity',
            'product',
            'sub_amount',
        )
        read_only_fields = (
            'order',
            'user'
        )
    def get_product(self, obj):
        product = obj.get_product()
        if not product:
            return None


        return {
            "id": product.id,
            "name": getattr(product, "name", None),
            "price": getattr(product, "price", None),
        }



class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(
        many=True,
        read_only=True,
        source='order_items'
    )
    total_amount = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = (
            'id',
            'created_at',
            'items',
            'total_amount',
        )