from rest_framework.serializers import Serializer, ModelSerializer, CharField, EmailField
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


# проверка имени пользователя
def validate_username(value):
    print(value)
    print("_" in value)
    if "_" in value:
        raise ValidationError(
            _("Имя пользователя не должно содержать _"),
            params={'value': value}
        )


class UserSerializer(ModelSerializer):
    e_msg = {'null': 'Поле не может иметь значение Null!',
             'blank': 'Поле не может быть пустым!',
             'invalid': 'Пожалуйста, введите корректное значения для поля!',
             'min_length': 'Минимальная длина пароля - 8 символов!',
             'max_length': 'Максимальная длина имени пользователя - 32 символа!'}
    # invalid, invalid_choice
    email = EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="Этот Email-адрес уже используется!")],
        error_messages=e_msg
    )
    username = CharField(
        max_length=32,
        validators=[UniqueValidator(queryset=User.objects.all(), message="Это имя пользователя уже используется!"),
                    validate_username],
        error_messages=e_msg
    )
    password = CharField(min_length=8, write_only=True, error_messages=e_msg)

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'],
                                        validated_data['password'])
        return user

    def clean(self):
        if "_" in self.username:
            return ValidationError("Имя пользователя не должно содержать _")

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'date_joined')


class LoginRequestSerializer(Serializer):
    model = User
    username = CharField(required=True)
    password = CharField(required=True)


class TokenSerializer(ModelSerializer):
    class Meta:
        model = Token
        fields = ['key']
