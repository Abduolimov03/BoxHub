# from django.contrib.auth.models import AbstractUser
# from django.db.models import EmailField, BooleanField, TextChoices
# from django.db.models.fields import CharField
#
# from apps.models.managers import CustomUserManager
#
#
# class User(AbstractUser):
#     class USER_TYPE(TextChoices):
#         MANAGER = 'manager', 'manager'
#         USER = 'user', 'user'
#
#     username = None
#     first_name = CharField(max_length=255)
#     last_name = CharField(max_length=255)
#     phone_number = CharField(max_length=20, null=True, blank=True)
#     email = EmailField(unique=True)
#     # todo is_active true qib qoyish kerak avtamatik tasdiqlaganda
#     is_active = BooleanField(default=False)
#     user_type = CharField(max_length=255, choices=USER_TYPE.choices, default=USER_TYPE.USER)
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []
#     objects = CustomUserManager()


from django.contrib.auth.models import AbstractUser
from django.db.models import EmailField, BooleanField, TextChoices, ForeignKey, CASCADE
from django.db.models.fields import CharField

from apps.models.managers import CustomUserManager

class User(AbstractUser):
    class USER_TYPE(TextChoices):
        MANAGER = 'manager', 'manager'
        USER = 'user', 'user'

    username = None
    first_name = CharField(max_length=255)
    last_name = CharField(max_length=255)
    phone_number = CharField(max_length=20, null=True, blank=True)
    email = EmailField(unique=True)
    is_active = BooleanField(default=False)
    user_type = CharField(max_length=255, choices=USER_TYPE.choices, default=USER_TYPE.USER)

    branch = ForeignKey(
        'apps.Branch',
        on_delete=CASCADE,
        related_name='users',
        null=True,
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email
