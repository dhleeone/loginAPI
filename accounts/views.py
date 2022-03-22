from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import AnonymousUser
from .models import User, PhoneVerification
from .constants import message
import random


# 전화번호 인증 ---
class PhoneVerify(APIView):
    permission_classes = [AllowAny]
    def generate_code(self):
        code = ""
        for _ in range(6):
            code += str(random.randint(0, 9))
        return code

    def post(self, request):
        input_phone = request.data['phone']
        record = PhoneVerification.objects.filter(phone=input_phone)
        if (record.exists()) and (not record.last().is_expired):
            return Response({"message": message.CODE_ISSUE_ERROR}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = PhoneVerifySerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            generated_code = self.generate_code()
            serializer.save(security_code=generated_code)
            return Response({"message": f"인증번호:{generated_code}"}, status=status.HTTP_201_CREATED)


# 회원가입 ---
class Register(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            input_code = request.data['security_code']
            input_phone = request.data['phone']
            code_record = PhoneVerification.objects.get(security_code=input_code)
            if input_phone != code_record.phone:
                return Response({'message': message.PHONE_VERIFICATION_ERROR}, status=status.HTTP_400_BAD_REQUEST)
            elif input_phone == code_record.phone and code_record.is_expired:
                return Response({'message': message.CODE_EXPIRED_ERROR}, status=status.HTTP_400_BAD_REQUEST)
            elif request.data['password'] != request.data['password2']:
                return Response({'message': message.PASSWORD_MISMATCH_ERROR}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer = RegisterSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({'message': message.REGISTER_SUCCESS}, status=status.HTTP_201_CREATED)
        except PhoneVerification.DoesNotExist:
            return Response({'message': message.PHONE_VERIFICATION_ERROR}, status=status.HTTP_400_BAD_REQUEST)


# 로그인 ---
class Login(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return Response({'message': message.LOGIN_SUCCESS}, status=status.HTTP_200_OK)
        else:
            return Response({'message': message.LOGIN_ERROR}, status=status.HTTP_400_BAD_REQUEST)


# 유저 정보 조회 ---
class UserProfile(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        current_user = request.user
        try:
            instance = User.objects.get(id=current_user.id)
            serializer = UserSerializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 비밀번호 변경 ---
class ResetPassword(APIView):
    permission_classes = [AllowAny]
    def patch(self, request):
        input_code = request.data['security_code']
        input_email = request.data['email']
        try:
            code_record = PhoneVerification.objects.get(security_code=input_code)
            instance = User.objects.get(email=input_email)
            if request.user != AnonymousUser():
                return Response({'message': message.ACCESS_ERROR}, status=status.HTTP_403_FORBIDDEN)

            elif instance.phone != code_record.phone:
                return Response({'message': message.PHONE_VERIFICATION_ERROR}, status=status.HTTP_400_BAD_REQUEST)

            elif instance.phone == code_record.phone and code_record.is_expired:
                return Response({'message': message.PHONE_VERIFICATION_ERROR}, status=status.HTTP_400_BAD_REQUEST)

            elif request.data['password'] != request.data['password2']:
                return Response({'message': message.PASSWORD_MISMATCH_ERROR}, status=status.HTTP_400_BAD_REQUEST)

            else:
                serializer = ResetPasswordSerializer(instance, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({'message': message.PASSWORD_CHANE_SUCCESS}, status=status.HTTP_200_OK)

        except PhoneVerification.DoesNotExist:
            return Response({'message': message.PHONE_VERIFICATION_ERROR}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'message': message.EMAIL_NOT_FOUND_ERROR}, status=status.HTTP_400_BAD_REQUEST)

