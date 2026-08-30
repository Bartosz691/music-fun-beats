from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'password2',
        ]

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({
                'password2': 'Hasła nie są takie same.'
            })

        validate_password(data['password'])

        return data

    def create(self, validated_data):
        validated_data.pop('password2')

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )

        return user