from django.shortcuts import render

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from django.contrib.auth.decorators import login_required

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from hashlib import sha1
from datetime import datetime

from binascii import hexlify

from lark import Lark,Transformer

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token 
import base64
from rest_framework.permissions import IsAuthenticated

from .serializers import AuthUserSerializer,MyTokenObtainPairSerializer

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            device = Token.objects.get(user=user)
            return Response(device.key)
    else:
        form = UserCreationForm()
    return Response("signup fialed")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_jwt(request):
    stripped = strip_token(request.headers["Authorization"])
    user = Token.objects.get(key=stripped).user
    
    refresh = RefreshToken.for_user(user)
    
    
    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    })

def strip_token(token_string):
    return token_string.split()[1]
        

'''
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def get(self, *args, **kwargs):
        username = Token.objects.get(key=self.request._request.headers["auth"]).user
        user = User.objects.get()
'''
'''
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtain_jwt_pair(request):

    serializer = MyTokenObtainPairSerializer(data=)    

        if serializer.is_valid():
            
            serializer.validated_data["set_id"] = hexed
        
            serializer.save()

    return Response(hexed)
    return Response("sick")
'''
# for use in signup API
@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance=None,created=False,**kwargs):
    if created:
        Token.objects.create(user=instance)