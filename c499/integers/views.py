# Django 
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# DRF 
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Project
from .models import Integer,IntegerSet,Session
from .serializers import IntegerSerializer,IntegerSetSerializer,SessionPostSerializer,IntegerSetPostSerializer
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
        working_set = request.data['set_id']

        queried = IntegerSet.objects.filter(set_id=working_set)
        
        if not queried:
            return Response("bad request") # replace with 400
        else:     
            set_dict = set_to_dict(queried)
            return Response(set_dict)
        

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
            return Response("bad request")
        
    elif request.method == 'DELETE':
        working_set = request.data['set_id']       
        queried = IntegerSet.objects.get(set_id=working_set)

        if not queried:
            queried.delete()
            return Response(working_set+" delete successful")
        else:
            return Response("bad request")

@api_view(['GET','POST','DELETE'])
def sessionAPIv1(request):
    if request.method == 'GET':
        working_session = request.data['session_id']

        queried = Session.objects.filter(session_id=working_session)
        
        if not queried:
            return Response("bad request") # replace with 400
        else:     
            session_dict = session_to_dict(queried)
            return Response(session_dict)

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
        working_session = request.data['session_id']       
        queried = Session.objects.get(set_id=working_session)

        if not queried:
            queried.delete()
            return Response(working_session+" delete successful")
        else:
            return Response("bad request")


def create_set_id():
    set_id = hash(str(datetime.utcnow())+server_secret)
    set_utf = str(set_id).encode("utf-8")
    return hexlify(set_utf).decode('utf-8')

