from rest_framework.exceptions import ValidationError
from rest_framework.fields import EmailField, CharField
from rest_framework.serializers import Serializer, ModelSerializer

from apps.models import User


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = 'id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'user_type',


class UserDetailModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = 'id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'user_type',


class RegisterModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password',)

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginModelSerializer(Serializer):
    email = EmailField()
    password = CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError("Invalid email or password")
        if not user.check_password(password):
            raise ValidationError("Invalid email or password")

        attrs["user"] = user
        return attrs
