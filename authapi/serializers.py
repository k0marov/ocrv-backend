from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import ModelSerializer


class SignUpSerializer(ModelSerializer):
    def validate(self, data):
        validate_password(data.get('password'))
        return data

    def create(self, validated_data):
        return User.objects.create_user(username=validated_data.get('username'), password=validated_data.get('password'))

    class Meta:
        model = User
        fields = ('username', 'password')