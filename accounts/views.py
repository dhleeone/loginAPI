from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User, PhoneVerification
from django.contrib.auth.hashers import make_password
from .serializers import *
import random
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import AnonymousUser

# Create your views here.
class PhoneVerify(APIView):
    permission_classes = [AllowAny]
    def generate_code(self):
        code = ""
        for i in range(6):
            code += str(random.randint(0, 9))
        return code

    def post(self, request):
        input_phone = request.data['phone']
        record = PhoneVerification.objects.filter(phone=input_phone)
        if (record.exists()) and (not record.last().is_expired):
            return Response({"message": "인증번호가 이미 발급되었습니다."}, status=status.HTTP_200_OK)
        else:
            serializer = PhoneVerifySerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            generated_code = self.generate_code()
            serializer.save(security_code=generated_code)
            return Response({"message": f"인증번호:{generated_code}"}, status=status.HTTP_200_OK)


class Register(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            input_code = request.data['security_code']
            input_phone = request.data['phone']
            code_record = PhoneVerification.objects.get(security_code=input_code)
            if input_phone != code_record.phone:
                return Response({'message': '유효한 인증번호가 아닙니다.'}, status=status.HTTP_400_BAD_REQUEST)
            elif input_phone == code_record.phone and code_record.is_expired:
                return Response({'message': '인증번호가 만료되었습니다.'}, status=status.HTTP_400_BAD_REQUEST)
            elif request.data['password'] != request.data['password2']:
                return Response({'message': '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer = RegisterSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                # 비밀번호 암호화
                serializer.save(password=make_password(request.data['password']))
                return Response({'message':'회원가입이 완료되었습니다.'}, status=status.HTTP_200_OK)
        except PhoneVerification.DoesNotExist:
            return Response({'message':'전화번호 인증을 진행해주세요.'}, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return Response({'message':'로그인이 완료되었습니다.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message':'아이디 혹은 패스워드 오류입니다.'}, status=status.HTTP_400_BAD_REQUEST)


class UserProfile(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        current_user = request.user
        try:
            instance = User.objects.get(id=current_user.id)
            serializer = UserSerializer(instance)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ResetPassword(APIView):
    permission_classes = [AllowAny]
    def patch(self, request):
        input_code = request.data['security_code']
        input_email = request.data['email']
        try:
            code_record = PhoneVerification.objects.get(security_code=input_code)
            instance = User.objects.get(email=input_email)
            if request.user != AnonymousUser():
                return Response({'message': '접근 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
            elif instance.phone != code_record.phone:
                return Response({'message': '유효한 인증번호가 아닙니다.'}, status=status.HTTP_400_BAD_REQUEST)
            elif instance.phone == code_record.phone and code_record.is_expired:
                return Response({'message': '인증번호가 만료되었습니다.'}, status=status.HTTP_400_BAD_REQUEST)
            elif request.data['password'] != request.data['password2']:
                return Response({'message': '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer = ResetPasswordSerializer(instance, data=request.data)
                serializer.is_valid(raise_exception=True)
                # 비밀번호 암호화
                serializer.save(password=make_password(request.data['password']))
                return Response({'message': '비밀번호 변경이 완료되었습니다.'}, status=status.HTTP_200_OK)

        except PhoneVerification.DoesNotExist:
            return Response({'message':'전화번호 인증을 진행해주세요.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'message':'올바른 이메일 주소를 입력해주세요.'}, status=status.HTTP_400_BAD_REQUEST)

