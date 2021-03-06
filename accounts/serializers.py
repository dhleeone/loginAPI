from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User, PhoneVerification
from .constants import message


# 전화번호 인증 Serializer ---
class PhoneVerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneVerification
        fields = [
            'id',
            'phone',
            'security_code'
        ]

    def validate_phone(self, value):
        if any(num.isalpha() for num in value):
            raise serializers.ValidationError(message.PHONE_NUMBER_ERROR)
        return value


# 인증 번호 Serializer ---
class SecurityCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneVerification
        fields = ['security_code']




# 회원가입 Serializer ---
class RegisterSerializer(serializers.ModelSerializer):
    security_code = SecurityCodeSerializer(read_only=True)
    password2 = serializers.CharField(max_length=128, read_only=True)
    gender = serializers.ChoiceField(choices=User.GenderChoices)

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
            'security_code',
            'gender',
        ]

    def validate(self, data):
        input_password = data['password']
        input_email = data['email'].split("@")[0]
        input_nickname = data['nickname']
        if not 7 < len(input_password) < 13:
            raise serializers.ValidationError(message.PASSWORD_LENGTH_ERROR)

        if not any(char.isdigit() for char in input_password):
            raise serializers.ValidationError(message.PASSWORD_COMBINATION_ERROR)

        if not any(char.isalpha() for char in input_password):
            raise serializers.ValidationError(message.PASSWORD_COMBINATION_ERROR)

        if input_password in input_email \
                or input_email in input_password:
            raise serializers.ValidationError(message.PASSWORD_UNIQUE_ERROR)

        if input_password in input_nickname \
                or input_nickname in input_password:
            raise serializers.ValidationError(message.PASSWORD_UNIQUE_ERROR)
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
            'phone',
            'gender'
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

    def validate(self, data):
        input_password = data['password']
        input_email = data['email'].split("@")[0]
        nickname = User.objects.get(email=data['email']).nickname
        if not 7 < len(input_password) < 13:
            raise serializers.ValidationError(message.PASSWORD_LENGTH_ERROR)

        if not any(char.isdigit() for char in input_password):
            raise serializers.ValidationError(message.PASSWORD_COMBINATION_ERROR)

        if not any(char.isalpha() for char in input_password):
            raise serializers.ValidationError(message.PASSWORD_COMBINATION_ERROR)

        if input_password in input_email \
                or input_email in input_password:
            raise serializers.ValidationError(message.PASSWORD_UNIQUE_ERROR)

        if input_password in nickname \
                or nickname in input_password:
            raise serializers.ValidationError(message.PASSWORD_UNIQUE_ERROR)
        return data

    def update(self, instance, validated_data):
        new_password = make_password(validated_data['password'])
        instance.password = new_password
        instance.save()
        return instance

