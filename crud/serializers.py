from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'password',
            'is_active', 'last_login', 'is_superuser',
        ]
        read_only_fields = ['last_login', 'is_superuser']
        extra_kwargs = {
            'username': {'required': True},
            'password': {'write_only': True, 'required': True},
            'is_active': {'required': True}
        }
