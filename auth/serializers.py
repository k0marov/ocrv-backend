from rest_framework.serializers import Serializer, ModelSerializer, CharField
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


class UserSerializer(ModelSerializer):
    username = CharField(max_length=32)
    password = CharField(min_length=8, write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['password'])
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password')


class LoginRequestSerializer(Serializer):
    model = User
    username = CharField(required=True)
    password = CharField(required=True)


class TokenSerializer(ModelSerializer):
    class Meta:
        model = Token
        fields = ['key']
