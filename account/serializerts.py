from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from account.models import CustomUser
from account.utils import send_activation_code




class UserSerializer(serializers.ModelSerializer):
    # name = serializers.CharField(max_length=8, required=True, write_only=True)
    password = serializers.CharField(min_length=8, required=True, write_only=True)
    password_confirm = serializers.CharField(min_length=8, required=True, write_only=True)
    class Meta:
        model = CustomUser
        fields =('email', 'name', 'password', 'password_confirm' )

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Passwords do not match!')
        return attrs


    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        send_activation_code(user.email, user.activation_code, status='register')
        return user

# password reset
class CreateNewPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    activation_code = serializers.CharField(max_length=25, required=True)
    password = serializers.CharField(max_length=8, required=True)
    password_confirmation = serializers.CharField(max_length=8, required=True)

    def validate_email(self, email):
        if not CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('пользователь не найден')
        return email

    def validate_activation_code(self, act_code):
        if not CustomUser.objects.filter(activation_code=act_code, is_active=False).exists():
            raise serializers.ValidationError('Неверный код активации')
        return act_code

    def validate(self, attrs):  # attrs == validated_data
        password = attrs.get('password')
        password_conf = attrs.pop('password_confirmation')
        if password != password_conf:
            raise serializers.ValidationError('Passwords do not match')
        return attrs

    def save(self, **kwargs):
        data = self.validated_data
        email = data.get('email')
        activation_code = data.get('activation_code')
        password = data.get('password')
        try:
            user = CustomUser.objects.get(email=email, activation_code=activation_code, is_active=False)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError('Пользователь не найден')

        user.is_active = True
        user.activation_code = ''
        user.set_password(password)
        user.save()
        return user

# class RegisterSerializer(ModelSerializer):
#     password = serializers.CharField(min_length=8, required=True, write_only=True)
#     password_confirm = serializers.CharField(min_length=8, required=True, write_only=True)
#
#     class Meta:
#         model = CustomUser
#         fields = ('email', 'password', 'password_confirm')
#
#     def validate(self, attrs):
#         password = attrs.get('password')
#         password_confirm = attrs.pop('password_confirm')
#         if password != password_confirm:
#             raise serializers.ValidationError('Passwords do not match!')
#         return attrs
#
#     def create(self, validated_data):
#         user = CustomUser.objects.create_user(**validated_data)
#         # send_activation_code(user.email, user.activation_code)
#         return user
#
# class UserLoginSerializer(serializers.Serializer):
#     email = serializers.CharField(max_length=120)
#     password = serializers.CharField(max_length=120, min_length=8)
#     token = serializers.CharField(max_length=255, read_only=True)