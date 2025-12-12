import uuid

from django.db.models import Model, CharField, SlugField, DateTimeField
from django.db.models.enums import TextChoices
from django.utils.text import slugify


class TimeBasedModel(Model):
    updated_at = DateTimeField(auto_now_add=True)
    created_at = DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Payment(TimeBasedModel):
    class PaymentMethod(TextChoices):
        PAYME = 'payme', 'Payme'
        CLICK = 'click', 'Click'
        CASH = 'cash', 'Cash'
        CARD = 'card', 'Card'

    payment_method = CharField(max_length=120, choices=PaymentMethod.choices, default=PaymentMethod.CASH)

    class Meta:
        abstract = True

    # todo birdan qara xam click xam yoki naqd qib qolish mumkin. qara shu uchun bitada 2 ta qisek boladi


class SlugBasedModel(Model):
    name = CharField(max_length=255)
    slug = SlugField(max_length=255, unique=True, editable=False)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while self.__class__.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug or str(uuid.uuid4())[:8]

        super().save(*args, **kwargs)
