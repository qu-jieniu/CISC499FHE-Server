# Django 
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# DRF 
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Project
from .models import Integer,IntegerSet,Session
from .serializers import IntegerSerializer,IntegerSetGetSerializer,IntegerSetRequestSerializer,IntegerSetSerializer,SessionPostSerializer,IntegerSetPostSerializer
from rest_framework.authtoken.models import Token

# Misc
import base64
from binascii import hexlify
from datetime import datetime
from hashlib import sha1
from lark import Lark, Transformer

server_secret = "cisc499_fully_homomorphic_encryption"

@api_view(['GET','POST','DELETE'])
def setAPIv1(request):
    if request.method == 'GET':
        req_serializer = IntegerSetRequestSerializer(data = request.data)
        if req_serializer.is_valid():
            integers = Integer.objects.filter(set_id=req_serializer.validated_data['set_id']) 
            serialized = IntegerSerializer(data=integers,many=True,read_only=True)
            if serialized.is_valid():
                return Response(serializer.validated_data)        
            return Response("bad serializer")
        return Response("bad request")

    elif request.method == 'POST':
        serializer = IntegerSetPostSerializer(data = request.data)
        
        if serializer.is_valid():      
            sent_user = serializer.validated_data.pop('user_id')
            session = Session.objects.get(session_id=serializer.validated_data.pop('session_id'))
            
            serializer.validated_data['set_id']=create_set_id()  
            serializer.validated_data['session_id']=session
            
            serializer.save()
            return Response(serializer.validated_data['set_id'])
        else:
            return Response(serializer.initial_data)
        
    elif request.method == 'DELETE':
        return Response("set delete")

@api_view(['GET','POST','DELETE'])
def sessionAPIv1(request):
    if request.method == 'GET':
        return Response("set get")
    elif request.method == 'POST':
        serializer = SessionPostSerializer(data = request.data)
        
        if serializer.is_valid():      
            user = Token.objects.get(key=serializer.validated_data.pop('user_id'))
            serializer.validated_data['user_id']=user
            serializer.save()
            return Response("it worked")
        else:
            return Response("didnt work")
        
    elif request.method == 'DELETE':
        return Response("set delete")

def create_set_id():
    set_id = hash(str(datetime.utcnow())+server_secret)
    set_utf = str(set_id).encode("utf-8")
    return hexlify(set_utf).decode('utf-8')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def integerList(request):
    integers = Integer.objects.all()
    serializer = IntegerSerializer(integers,many=True)
    return Response(serializer.data)

