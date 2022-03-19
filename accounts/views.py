from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import User, PhoneVerification
from django.contrib.auth.hashers import make_password
from .serializers import *
import random

# Create your views here.
class PhoneVerify(APIView):
    permission_classes = [AllowAny]
    def generate_code(self):
        code = ""
        for i in range(6):
            code += str(random.randint(0, 9))
        return code

    def post(self, request):
        serializer = PhoneVerifySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            generated_code = self.generate_code()
            serializer.save(security_code=generated_code)
            return Response({"message":f"인증번호:{generated_code}"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Register(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            input_code = request.data['security_code']
            code_record = PhoneVerification.objects.get(security_code=input_code)

            if code_record.is_expired:
                return Response({'message': '인증번호가 만료되었습니다.'}, status=status.HTTP_400_BAD_REQUEST)
            elif request.data['password'] != request.data['password2']:
                return Response({'message': '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer = RegisterSerializer(data=request.data)
                if serializer.is_valid(raise_exception=True):
                    # 비밀번호 암호화
                    serializer.save(password=make_password(request.data['password']))
                    return Response({'message':'회원가입이 완료되었습니다.'}, status=status.HTTP_200_OK)
                return Response({'message': 'error'}, status=status.HTTP_400_BAD_REQUEST)

        except PhoneVerification.DoesNotExist:
            return Response({'message':'전화번호 인증을 진행해주세요.'}, status=status.HTTP_400_BAD_REQUEST)
