from django.core.exceptions import ValidationError
from django.db import models
from apps.models import Payment
from apps.models.product_model import CoffeeAndTea, Product
from apps.models.size_model import CoffeeSize
from decimal import Decimal
from django.db import models


class Order(models.Model):
    user = models.ForeignKey(
        'apps.User',
        on_delete=models.CASCADE,
        related_name='orders'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_amount(self) -> Decimal:
        """Orderdagi barcha itemlarning umumiy narxi"""
        return sum(
            (item.sub_amount for item in self.order_items.all()),
            Decimal('0.00')
        )

    @property
    def paid_amount(self) -> Decimal:
        """Faqat completed paymentlarning umumiy summasi"""
        return sum(
            (payment.amount for payment in self.payments.filter(
                status=Payment.PaymentStatus.COMPLETED
            )),
            Decimal('0.00')
        )

    @property
    def due_amount(self) -> Decimal:
        """Qolgan to‘lov summasi"""
        return max(self.total_amount - self.paid_amount, Decimal('0.00'))

    @property
    def is_paid(self) -> bool:
        """Order to‘liq to‘langan bo‘lsa True"""
        return self.due_amount == 0

    def __str__(self):
        return f"Order #{self.id} - {self.user.email}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_items'
    )

    coffee = models.ForeignKey(
        CoffeeAndTea,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    size = models.ForeignKey(
        CoffeeSize,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    quantity = models.PositiveIntegerField(default=1)

    # 🔑 order vaqtidagi narx (history uchun)
    price_snapshot = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(coffee__isnull=False) | models.Q(product__isnull=False),
                name='orderitem_at_least_one_product'
            )
        ]

    def clean(self):
        if not self.coffee and not self.product:
            raise ValidationError("Coffee yoki Product tanlanishi shart")

        if self.coffee:
            if not self.size:
                raise ValidationError("Coffee uchun size majburiy")
            if self.size.product_id != self.coffee.id:
                raise ValidationError("Size ushbu coffee ga tegishli emas")

        # ⚠️ faqat product bo‘lsa
        if self.product and not self.coffee and self.size:
            raise ValidationError("Product uchun size bo‘lmaydi")

    def save(self, *args, **kwargs):
        if not self.price_snapshot:
            if self.coffee:
                self.price_snapshot = self.size.price
            else:
                self.price_snapshot = (
                    self.product.price_discounted or self.product.price_out
                )

        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def sub_amount(self) -> Decimal:
        return self.price_snapshot * self.quantity

    def __str__(self):
        name = self.coffee.name if self.coffee else self.product.name
        return f"{name} x {self.quantity}"

