from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from account.models import CustomUser
from account.utils import send_activation_code


class RegisterSerializer(ModelSerializer):
    password = serializers.CharField(min_length=8, required=True, write_only=True)
    password_confirm = serializers.CharField(min_length=8, required=True, write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'password_confirm')

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Passwords do not match!')
        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        send_activation_code(user.email, user.activation_code)
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=120)
    password = serializers.CharField(max_length=120, min_length=8)
    token = serializers.CharField(max_length=255, read_only=True)