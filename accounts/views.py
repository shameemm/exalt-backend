import datetime
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework import status
from .serializers import UserSerializer,MyTokenObtainPairSerializer,MyAdminTokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django_otp import devices_for_user
from .permissions import IsSuperUser,IsPartner
from twilio.rest import Client
from .models import UserData
from rest_framework_simplejwt.tokens import RefreshToken
import os
from decouple import config

from rest_framework.permissions import IsAuthenticated, AllowAny
# from django_otp.plugins.otp_twilio.models import TwilioSMSDevice



# view for registering users
class RegisterView(APIView):
    def post(self, request):
        print(request.data)
        phone = request.data.get('phone')
        email = request.data.get('email')
        if UserData.objects.filter(phone=phone).exists():
            return Response({'error':'phone number already exists'},status=status.HTTP_400_BAD_REQUEST)
        elif UserData.objects.filter(email=email).exists():
            return Response({'error':'email already exists'},status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
    
class InitiateVerificationView(APIView):
    def post(self, request):
        print(request.data)
        ACCOUNT_SID = config('TWILIO_ACCOUNT_SID',default='')
        AUTH_TOKEN = config('TWILIO_AUTH_TOKEN', default='')
        VERIFY_SERVICE_SID = config('TWILIO_VERIFY_SERVICE_SID', default='')
        phone = "+91"+request.data.get('phone')
        if not phone:
            return Response({'error':'phone number is requied'})
        try:
            client = Client(ACCOUNT_SID , AUTH_TOKEN)
            verification = client.verify \
                .services(VERIFY_SERVICE_SID) \
                .verifications \
                .create(to=phone, channel='sms')
            return Response({'message': 'Verification initiated.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
class VerifyUserView(APIView):
    def post(self, request):
        ACCOUNT_SID = config('TWILIO_ACCOUNT_SID',default='')
        AUTH_TOKEN = config('TWILIO_AUTH_TOKEN', default='')
        VERIFY_SERVICE_SID = config('TWILIO_VERIFY_SERVICE_SID', default='')
        print(request.data)
        phone_number = "+91"+request.data.get('phone_number')
        code = request.data.get('code')
        print(phone_number)
        if not phone_number or not code:
            return Response({'error': 'Phone number and code are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            client = Client(ACCOUNT_SID, AUTH_TOKEN)
            verification_check = client.verify \
                .services(VERIFY_SERVICE_SID) \
                .verification_checks \
                .create(to=phone_number, code=code)
            if verification_check.status == 'approved':
                # Create or update user object here
                return Response({'message': 'User verified.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid verification code.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    
class MyAdminTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyAdminTokenObtainPairSerializer
    
class SendOtp(APIView):
    permission_classes = [IsPartner]
    def post(self,request):
        user = request.user
        return Response(data=user.name)
    
class SentOtpForPartnerLogin(APIView):
    
    def post(self, request):
        print(request.data)
        ACCOUNT_SID = config('TWILIO_ACCOUNT_SID',default='')
        AUTH_TOKEN = config('TWILIO_AUTH_TOKEN', default='')
        VERIFY_SERVICE_SID = config('TWILIO_VERIFY_SERVICE_SID', default='')
        phone = request.data.get('phone')
        if not phone:
            return Response({'error':'phone number is requied'})
        if not UserData.objects.filter(phone=phone).exists():
            return Response({'error':'phone number does not exists'},status=status.HTTP_400_BAD_REQUEST)
        try:
            phone = '+91'+phone
            client = Client(ACCOUNT_SID , AUTH_TOKEN)
            verification = client.verify \
                .services(VERIFY_SERVICE_SID) \
                .verifications \
                .create(to=phone, channel='sms')
            return Response({'message': 'Verification initiated.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class VerifyPartnerLoginOtpView(APIView):
    serializer_class = MyTokenObtainPairSerializer
    def post(self, request):
        ACCOUNT_SID = config('TWILIO_ACCOUNT_SID',default='')
        AUTH_TOKEN = config('TWILIO_AUTH_TOKEN', default='')
        VERIFY_SERVICE_SID = config('TWILIO_VERIFY_SERVICE_SID', default='')
        phone_number = "+91"+request.data.get('phone_number')
        phone = request.data.get('phone_number')
        code = request.data.get('code')   
        if not phone_number or not code:
            return Response({'error': 'Phone number and code are required.'}, status=status.HTTP_400_BAD_REQUEST) 
        try:
            client = Client(ACCOUNT_SID, AUTH_TOKEN)
            verification_check = client.verify \
                .services(VERIFY_SERVICE_SID) \
                .verification_checks \
                .create(to=phone_number, code=code)
            if verification_check.status == 'approved':
                user = UserData.objects.get(phone=phone)
                
                refresh = RefreshToken.for_user(user)
                refresh['is_partner'] = user.is_partner
                refresh['is_active'] = user.is_active
                access = str(refresh.access_token)
                payload = {
                    'access': str(access),
                    'refresh': str(refresh),
                }
                return Response(payload, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid verification code.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   