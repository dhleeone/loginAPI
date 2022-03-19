from rest_framework import serializers
from .models import User, PhoneVerification


class PhoneVerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneVerification
        fields = [
            'id',
            'phone',
            'security_code'
        ]


class SecurityCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneVerification
        fields = ['security_code']


class RegisterSerializer(serializers.ModelSerializer):
    security_code = SecurityCodeSerializer(read_only=True)
    password2 = serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'password',
            'password2',
            'nickname',
            'name',
            'phone',
            'security_code'
        ]
    def validate_email(self, email):
        if User.objects.filter(email=email):
            raise ValidationError('이미 존재하는 이메일 입니다.')
        return email


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'password'
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'nickname',
            'name',
            'phone'
        ]

class ResetPasswordSerializer(serializers.ModelSerializer):
    security_code = SecurityCodeSerializer(read_only=True)
    password2 = serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = [
            'security_code',
            'email',
            'password',
            'password2'
        ]