from django.db.models import Model
from django.db.models.fields import IntegerField


class Settings(Model):
    coffee_percentage = IntegerField(default=0, help_text="O'rtacha necha foiz xar bir coffee dan foyda qoladi")
