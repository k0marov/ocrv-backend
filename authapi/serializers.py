from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.core import exceptions
from rest_framework import serializers


class SignUpSerializer(serializers.ModelSerializer):
    def validate(self, data):
        errors = dict()
        try:
            password_validation.validate_password(password=data.get('password'))
        # the default django ValidationError, not the drf one
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return data

    def create(self, validated_data):
        return User.objects.create_user(username=validated_data.get('username'), password=validated_data.get('password'))

    class Meta:
        model = User
        fields = ('username', 'password')