from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ValidationError
from .models import User, PhoneVerification


# 전화번호 인증 Serializer ---
class PhoneVerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneVerification
        fields = [
            'id',
            'phone',
            'security_code'
        ]


# 인증 번호 Serializer ---
class SecurityCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneVerification
        fields = ['security_code']


# 회원가입 Serializer ---
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

    def validate(self, data):
        input_password = data['password']
        input_email = data['email']
        input_nickname = data['nickname']
        if not 7 < len(input_password) < 13:
            raise serializers.ValidationError("패스워드는 8자 이상 12자 이내로 만들어주세요.")
        if not any(char.isdigit() for char in input_password):
            raise serializers.ValidationError("패스워드에는 최소 1개의 숫자가 포함되어야 합니다.")
        if not any(char.isalpha() for char in input_password):
            raise serializers.ValidationError("패스워드에는 최소 1개의 영문자가 포함되어야 합니다.")
        if input_password in input_email.split("@")[0] \
                or input_email.split("@")[0] in input_password:
            raise serializers.ValidationError("패스워드에는 이메일과 동일한 문자가 포함되어서는 안됩니다.")
        if input_password in input_nickname \
                or input_nickname in input_password:
            raise serializers.ValidationError("패스워드에는 닉네임과 동일한 문자가 포함되어서는 안됩니다.")
        return data

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


# 로그인 Serializer ---
class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'password'
        ]


# 유저 정보 Serializer ---
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


# 비밀번호 변경 Serializer ---
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

    def update(self, instance, validated_data):
        new_password = make_password(validated_data['password'])
        instance.password = new_password
        instance.save()
        return instance