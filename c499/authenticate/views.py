# Django
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# DRF 
from rest_framework import status
from rest_framework.authtoken.models import Token 
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# DRF_simplejwt
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

# Project
from .serializers import AuthUserSerializer,MyTokenObtainPairSerializer
from utils import strip_token

# Misc
import base64
from binascii import hexlify
from datetime import datetime
from hashlib import sha1
import jwt as jwt_utils

@api_view(['POST'])
def signup(request):
    status_message = {}
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            try:
                device = Token.objects.get(user=user)
            except Token.DoesNotExist:
                status_message["criticalError"] = "token not created on signup"
                return Response(status_message,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except err:
                status_message["serviceError"] = err
                return Response(status_message,status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
            status_message["deviceToken"] = device.key
            return Response(status_message,status=status.HTTP_200_OK)
        else:
            status_message["formError"] = form.errors 
            return Response(status_message,status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

# for use in signup API
@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance=None,created=False,**kwargs):
    if created:
        Token.objects.create(user=instance)

@api_view(['POST'])
def login(request):
    status_message = {}
    if request.method == 'POST':   
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password) # select backends?
        if user is not None:
            auth_login(request,user)
            try:
                device = Token.objects.get(user=user)
            except Token.DoesNotExist:
                status_message["authError"] = "user does not have token"
                return Response(status_message,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except err:
                status_message["databaseError"] = err
                return Response(status_message,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            status_message["deviceToken"] = device.key
            return Response(status_message,status=status.HTTP_200_OK)
        else:
            status_message["authError"] = "bad login"
            return Response(status_message,status=status.HTTP_401_UNAUTHORIZED) 
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    status_message = {}
    if request.method == 'POST':   
        try:
            device = request.headers["Authorization"]
        except KeyError:
            status_message["authError"] = "device token not supplied"
            return Response(status_message,status=status.HTTP_401_UNAUTHORIZED)
        
        device = strip_token(device)

        try:
            token = Token.objects.get(key=device)
            user = User.objects.get(username=token.user)
        except (Token.DoesNotExist,User.DoesNotExist):
            status_message["authError"] = "invalid token"
            return Response(status_message,status=status.HTTP_401_UNAUTHORIZED)
        except err:
            status_message["serviceError"] = err
            return Response(status_message,status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        auth_logout(request)
            
        status_message["logout"] = "success"
        return Response(status_message,status=status.HTTP_200_OK)
         
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def del_logout(request):
    status_message = {}
    if request.method == 'POST':   
        try:
            device = request.headers["Authorization"]
        except KeyError:
            status_message["authError"] = "device token not supplied"
            return Response(status_message,status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            session_id = request.cookies["sessionid"]
        except KeyError:
            status_message["authError"] = "session_id missing"
            return Response(status_message,status=status.HTTP_400_BAD_REQUEST)
        
        device = strip_token(device)

        try:
            token = Token.objects.get(key=device)
            user = User.objects.get(username=token.user)
            session = PersistentSession.objects.get(session_id=session_id)
        except (Token.DoesNotExist,User.DoesNotExist):
            status_message["authError"] = "invalid token"
            return Response(status_message,status=status.HTTP_401_UNAUTHORIZED)
        except PersistentSession.DoesNotExist:
            status_message["sessionError"] = "invalid session_id"
            return Response(status_message,status=status.HTTP_400_BAD_REQUEST)
        except err:
            status_message["serviceError"] = err
            return Response(status_message,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        auth_logout(request)
        session.delete()

        status_message["logout"] = "success"
        return Response(status_message,status=status.HTTP_200_OK)
         
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtain_jwt_pair(request):
    status_message = {}
    if request.method == 'GET':
        stripped = strip_token(request.headers["Authorization"])
        
        try:
            user = Token.objects.get(key=stripped).user
        except Token.DoesNotExist:
            status_message["tokenError"] = "how did you get past authentication?"
            return Response(status_message,status.HTTP_401_UNAUTHORIZED)
        except err:
            status_message["databaseError"] = err
            return Response(status_message,status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        
        refresh = RefreshToken.for_user(user)

        decodeJTW = jwt_utils.decode(str(refresh.access_token), 'a-=!v#7apaipy8!pkq$rhyt0he@t%3!+irci7ytp_(t&03z(tt', algorithms=["HS256"])
        decodeJTW['token'] = stripped
        encoded = jwt_utils.encode(decodeJTW, 'a-=!v#7apaipy8!pkq$rhyt0he@t%3!+irci7ytp_(t&03z(tt', algorithm="HS256")

        status_message["refresh"] = str(refresh)
        status_message["access"] = str(encoded)
        return Response(status_message,status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

