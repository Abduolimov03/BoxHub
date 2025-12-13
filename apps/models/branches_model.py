from django.db.models import Model, CharField, BooleanField

class Branch(Model):
    name = CharField(max_length=25)
    address = CharField(max_length=25)
    phone = CharField(max_length=15, null=True, blank=True)
    is_active = BooleanField(default=True)

    def __str__(self):
        return self.name
