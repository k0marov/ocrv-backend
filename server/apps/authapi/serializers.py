from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.core import exceptions
from rest_framework import serializers


class SignUpSerializer(serializers.ModelSerializer):
    def _validate_password(self, password: str) -> None:
        """Validates the password using the default django validation and converts the error to the DRF one"""
        try:
            password_validation.validate_password(password=password)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'password': e.messages})

    def validate(self, data):
        self._validate_password(data.get('password'))
        return data

    def create(self, validated_data):
        return User.objects.create_user(username=validated_data.get('username'), password=validated_data.get('password'))

    class Meta:
        model = User
        fields = ('username', 'password')
