from django.core.exceptions import ObjectDoesNotExist
from apps.models.branches_model import Branch
from django.db.models import (
    Model, ForeignKey, CASCADE, DateTimeField, CharField, PositiveIntegerField
)

PRODUCT_TYPES = (
    ("coffee", "Coffee & Tea"),   # CoffeeSize orqali
    ("product", "Product"),
)


class Order(Model):
    user = ForeignKey('apps.User', CASCADE, related_name='orders')
    branch = ForeignKey(Branch, CASCADE, related_name='orders')
    created_at = DateTimeField(auto_now_add=True)


    @property
    def total_amount(self):
        return sum(item.sub_amount for item in self.order_items.all())

    def __str__(self):
        return f"Order {self.id} - {self.user.email}"


class OrderItem(Model):
    order = ForeignKey('apps.Order', CASCADE, related_name='order_items')
    user = ForeignKey('apps.User', CASCADE, related_name='order_items')

    product_type = CharField(max_length=20, choices=PRODUCT_TYPES)

    # agar coffee bo‘lsa — bu CoffeeSize.id bo‘ladi
    # Agar product bo‘lsa — Product.id bo‘ladi
    product_id = PositiveIntegerField()

    quantity = PositiveIntegerField(default=1)

    def get_product(self):
        try:
            if self.product_type == "coffee":
                from apps.models import CoffeeSize
                return CoffeeSize.objects.select_related("product").get(id=self.product_id)

            else:
                # Oddiy Product
                from apps.models import Product
                return Product.objects.get(id=self.product_id)

        except ObjectDoesNotExist:
            return None

    @property
    def sub_amount(self):
        product = self.get_product()
        if not product:
            return 0

        if self.product_type == "coffee":
            # CoffeeSize.price -> always correct
            return product.price * self.quantity

        # Oddiy product bo‘lsa:
        price = product.price_discounted or product.price_out
        return price * self.quantity

    def __str__(self):
        return f"{self.product_type} - {self.product_id}"


# yarmi carda yarmi naqt tolovlar