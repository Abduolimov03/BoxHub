from django.core.exceptions import ValidationError
from django.db.models import CharField, ForeignKey, CASCADE, DecimalField, ImageField, \
    IntegerField, Model
from django_ckeditor_5.fields import CKEditor5Field

from apps.models import SlugBasedModel


class Category(SlugBasedModel):
    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"

    def __str__(self):
        return self.name


class CoffeeAndTea(SlugBasedModel):
    name = CharField(max_length=255)
    image = ImageField(upload_to='coffee/image/', null=True, blank=True)
    category = ForeignKey('apps.Category', CASCADE, related_name='coffee_products')

    class Meta:
        verbose_name = "Coffee & Tea"
        verbose_name_plural = "Coffee & Tea"

    def __str__(self):
        return self.name


class CoffeeSize(Model):
    SIZES = [
        (200, "200 ml"),
        (300, "300 ml"),
        (400, "400 ml"),
        (500, "500 ml"),
        (700, "700 ml"),
    ]

    product = ForeignKey(CoffeeAndTea, CASCADE, related_name="sizes")
    size = IntegerField(choices=SIZES, null=True, blank=True)
    price = IntegerField()
    preparation = CKEditor5Field(null=True, blank=True)

    def __str__(self):
        return f"{self.product.name} - {self.size} ml"

    class Meta:
        verbose_name = "Size of Coffee & Tea"
        verbose_name_plural = "Size of Coffee & Tea"


class Product(SlugBasedModel):
    category = ForeignKey('apps.Category', CASCADE, related_name='products')
    quantity = DecimalField(decimal_places=2, max_digits=10)
    price_in = DecimalField(max_digits=12, decimal_places=2, help_text="Kelish narxi (so‘mda)")
    price_out = DecimalField(max_digits=12, decimal_places=2, help_text="Sotish narxi (so‘mda)")
    image = ImageField(upload_to='products/', blank=True, null=True)
    description = CKEditor5Field()
    price_discounted = DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Agar chegirma bo‘lsa, bu narxni kiriting (so‘mda)"
    )

    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"

    def __str__(self):
        return f"{self.name} ({self.category.name})"

    def clean(self):
        if self.price_discounted is not None:
            profit = self.price_out - self.price_in
            if self.price_discounted > profit:
                raise ValidationError({
                    'price_discounted': f"Chegirma narxi kelish narxidan ({profit}) kata bo‘la olmaydi!"
                })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
