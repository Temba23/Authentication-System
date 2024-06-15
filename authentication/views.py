from .serializers import UserSerializer, UserRegisterSerializer, SecurityQuestionSerializer
from rest_framework.views import APIView
from .models import CustomUser, OTPVerification, SecurityQuestion
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import render
import random
import datetime
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            user_otp, created = OTPVerification.objects.get_or_create(user=user)
            # max_otp_try = int(user_otp.max_otp_try) if user_otp.max_otp_try else 0
            # if max_otp_try < 3:
            otp = random.randint(10000, 99999)
            otp_expiry = timezone.now() + datetime.timedelta(minutes=3)
            user_otp.otp_code = otp
            user_otp.is_verified = False
            user_otp.otp_expiry = otp_expiry
            # user_otp.max_otp_try = str(max_otp_try + 1)
            user_otp.save()

            send_mail(
                subject='OTP Verification',
                message=f'Hi {user.username}, Your OTP code is {otp}.',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
            )
            return Response("Successfully generated OTP", status=status.HTTP_200_OK)
            # else:
            #     return Response("Maximum OTP tries exceeded.", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Authentication Credentials Error.", status=status.HTTP_400_BAD_REQUEST)


class VerifyAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        otp_code = request.data.get('otp_code')
        user_id = request.data.get('user')

        otp = OTPVerification.objects.filter(otp_code=otp_code, user=user_id, is_verified=False).first()
        current_time = timezone.now()
        
        if otp is None:
            otp_user = OTPVerification.objects.filter(user_id=user_id).first()
            otp_user.max_try += 1
            otp_user.save()
            return Response("Invalid OTP.", status=status.HTTP_400_BAD_REQUEST)
        
        if otp.otp_expiry and current_time < otp.otp_expiry:
            if otp.max_try < 3:
                otp.is_verified = True
                otp.save()
                refresh = RefreshToken.for_user(otp.user)

                try:
                    send_mail(
                        subject="Login Alert!",
                        message="Login successful.",
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[otp.user.email],
                    )
                except Exception as e:
                    return Response(f"Error sending email: {str(e)}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                return Response({'message': "Login Successful", 'isLogin': True, 'refresh_token': str(refresh), 'access_token': str(refresh.access_token)})
            else:
                return Response("Max OTP tries reached. Thus, token is deactivated.", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("OTP has expired.", status=status.HTTP_400_BAD_REQUEST)

class LogoutAPIView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            print("Received refresh token:", refresh_token)
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response("Logout Successful", status=status.HTTP_200_OK)
        except KeyError:
            return Response("Refresh token not provided", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response("An error occurred: " + str(e), status=status.HTTP_400_BAD_REQUEST)
           

class UserDetailAPI(APIView):
  def get(self,request,*args,**kwargs):

    user = CustomUser.objects.get(id=request.user.id)
    if user:
        serializer = UserSerializer(user)
        return Response(serializer.data)
    else:
       return Response("No Such User")
    
class RegisterUserAPIView(generics.CreateAPIView):
  permission_classes = [AllowAny]
  serializer_class = UserRegisterSerializer

  def perform_create(self, serializer):
    user = serializer.save()
    serializer.send_mail()

def profile(request):
    return render(request, 'profile.html')

class SecurityQuestionAPIView(APIView):
    serializer_class = SecurityQuestionSerializer    

    def get(self, request):
        user = request.user
        question = SecurityQuestion.objects.filter(user=user)
        serializer_data = self.serializer_class(question, many=True)
        return Response({"Data" : serializer_data.data}, status=status.HTTP_200_OK)
    
    def post(Self, request):
        user = request.user
        serializer = Self.serializer_class(data=request.data, context={"request":request})
        if serializer.is_valid():
            serializer.save(user=user)
            return Response({"Data" : serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)       
    
    def put(self, request):
        user = request.user

        question = request.data.get('questions')
        print(question)
        try :
            instance = SecurityQuestion.objects.get(questions=question, user=user)
            print(instance)
        except SecurityQuestion.DoesNotExist:
            return Response("Question Not Found.")
        serializer = self.serializer_class(instance, data=request.data, context={"request":request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("Security Question Updated.", status=status.HTTP_200_OK)

class UserPasswordReset(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        return Response("Not Allowed.")
    
    def post(self, request):
        username = request.data.get('username')
        user = CustomUser.objects.get(username=username)
        if user :
            req_question = request.data.get('question')
            req_answer= request.data.get('answer')
            question = SecurityQuestion.objects.get(questions=req_question)
            answer = SecurityQuestion.objects.get(answer=req_answer, user=user)

            if answer == user.user_security:
                user_otp, created = OTPVerification.objects.get_or_create(user=user)
                otp = random.randint(10000, 99999)
                otp_expiry = timezone.now() + datetime.timedelta(minutes=3)
                user_otp.otp_code = otp
                user_otp.is_verified = False
                user_otp.otp_expiry = otp_expiry
                user_otp.save()

                send_mail(
                    subject='OTP Verification',
                    message=f'Hi {user.username}, Your OTP code is {otp}.',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.email],
                )
                return Response("Successfully generated OTP", status=status.HTTP_200_OK)
            else:
                return Response("Security Answers Incorrect.", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("User don't exist.", status=status.HTTP_400_BAD_REQUEST)

            

