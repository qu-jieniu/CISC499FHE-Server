# Django 
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# DRF 
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Project
from eqparser import parse_eq
from .models import Integer,IntegerSet,PersistentSession
from .serializers import IntegerSerializer,IntegerSetSerializer,SessionPostSerializer,IntegerSetPostSerializer,IntegerNewSetSerializer
from utils import strip_token

# Misc
import base64
from binascii import hexlify
from datetime import datetime
from hashlib import sha1
import jwt as jwt_utils

server_secret = "cisc499_fully_homomorphic_encryption"

@api_view(['GET','POST','DELETE'])
@permission_classes([IsAuthenticated])
def setAPIv1(request):
    status_message = {}
    if request.method == 'GET':
        try:
            jwt = request.headers["Bearer"]
        except KeyError:
            status_message['authError'] = "JWT not supplied"
            return Response(status_message,status=status.HTTP_401_UNAUTHORIZED)
        
        jwt = strip_token(jwt)
        decode_jwt = jwt.decode(jwt, 'a-=!v#7apaipy8!pkq$rhyt0he@t%3!+irci7ytp_(t&03z(tt', algorithms=["HS256"])

        try:
            token = Token.objects.get(key=decode_jwt['token'])
        except Token.DoesNotExist:
            status_message['authError'] = "invalid JWT"
            return Response(status_message,status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            session_id = request.COOKIES['sessionid']
        except KeyError:
            status_message['sessionError'] = "session cookie not supplied"
            return Response(status_message,status=status.HTTP_400_BAD_REQUEST)
        
        try:
            session = PersistentSession.objects.get(session_id=session_id)
        except PersistentSession.DoesNotExist:
            status_message['sessionError'] = "invalid session_id"
            return Response(status_message,status=status.HTTP_400_BAD_REQUEST)
        
        try:
            working_set = request.data['set_id']
        except KeyError:
            status_message['argError'] = "set_id not supplied"
            return Response(status_message,status=status.HTTP_400_BAD_REQUEST)
        
        queried = IntegerSet.objects.filter(set_id=working_set)
        
        if not queried:
            status_message["invalidArgument"] = "set_id not found"
            return Response(status_message,status=status.HTTP_400_BAD_REQUEST) 
        else:     
            set_dict = set_to_dict(queried)
            return Response(set_dict,status=status.HTTP_200_OK)
        
    elif request.method == 'POST':
        try:
            jwt = request.headers["Authorization"]
        except KeyError:
            status_message['authError'] = "JWT not supplied"
            return Response(status_message,status=status.HTTP_401_UNAUTHORIZED)
        jwt = strip_token(jwt)
        decode_jwt = jwt_utils.decode(jwt, 'a-=!v#7apaipy8!pkq$rhyt0he@t%3!+irci7ytp_(t&03z(tt', algorithms=["HS256"])

        try:
            token = Token.objects.get(key=decode_jwt['token'])
        except Token.DoesNotExist:
            status_message['authError'] = "invalid JWT"
            return Response(status_message,status=status.HTTP_401_UNAUTHORIZED)
            
        try:
            session_id = request.COOKIES['sessionid']
        except KeyError:
            status_message['sessionError'] = "session cookie not supplied"
            return Response(status_message,status=status.HTTP_400_BAD_REQUEST)
            
        try:
            session = PersistentSession.objects.get(session_id=session_id)
        except PersistentSession.DoesNotExist:
            session = PersistentSession.objects.create(user_id=token,session_id =session_id)
            status_message['sessionCreated'] = session_id

        serializer = IntegerNewSetSerializer(data = request.data) 
        serializer.initial_data['session_id'] = session_id
        
        if serializer.is_valid():      
            
            serializer.validated_data['set_id']=create_set_id()  
            
            serializer.save()

            status_message['setCreated'] = serializer.validated_data['set_id'] 
            return Response(status_message,status=status.HTTP_200_OK)
        else:
            status_message["serializerError"] = serializer.errors
            return Response(status_message, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
        try:
            jwt = request.headers["Bearer"]
        except KeyError:
            status_message['authError'] = "JWT not supplied"
            return Response(status_message,status=status.HTTP_401_UNAUTHORIZED)

        jwt = strip_token(jwt)
        decode_jwt = jwt.decode(jwt, 'a-=!v#7apaipy8!pkq$rhyt0he@t%3!+irci7ytp_(t&03z(tt', algorithms=["HS256"])

        try:
            token = Token.objects.get(key=decode_jwt['token'])
        except Token.DoesNotExist:
            status_message['authError'] = "invalid JWT"
            return Response(status_message,status=status.HTTP_401_UNAUTHORIZED)
        try:
            session_id = request.COOKIES['sessionid']
        except KeyError:
            status_message['sessionError'] = "session cookie not supplied"
            return Response(status_message,status=status.HTTP_400_BAD_REQUEST)
        try:
            session = PersistentSession.objects.get(session_id=session_id)
        except PersistentSession.DoesNotExist:
            status_message['sessionError'] = "invalid session_id"
            return Response(status_message,status=status.HTTP_400_BAD_REQUEST)

        try:
            working_set = request.data['set_id']
        except KeyError:
            status_message['argError'] = "set_id not supplied"
            return Response(status_message,status=status.HTTP_400_BAD_REQUEST)

        queried = IntegerSet.objects.get(set_id=working_set)

        if not queried:
            status_message["invalidArgument"] = "set_id not found"
            return Response(status_message,status=status.HTTP_400_BAD_REQUEST) 
        else:     
            queried.delete()
            return Response(set_dict,status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET','POST','DELETE'])
@permission_classes([IsAuthenticated])
def sessionAPIv1(request):
    if request.method == 'GET':
        working_session = request.data['session_id']

        queried = PersistentSession.objects.filter(session_id=working_session)
        
        if not queried:
            status_message[""] = ""
            return Response(status_message,status=status.HTTP_400_BAD_REQUEST) # replace with 400
        else:     
            session_dict = session_to_dict(queried)
            return Response(session_dict)

    elif request.method == 'POST':
        serializer = SessionPostSerializer(data = request.data)
        
        if serializer.is_valid():      
            user = Token.objects.get(key=serializer.validated_data.pop('user_id'))
            serializer.validated_data['user_id']=user
            serializer.save()
            status_message["sessionPosted"] = serializer["session_id"]
            return Response(status_message,status=status.HTTP_200_OK)
        else:
            status_message["serializerError"] = serializer.errors
            return Response(status_message,status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
        working_session = request.data['session_id']       
        queried = PersistentSession.objects.get(set_id=working_session)

        if not queried:
            queried.delete()
            return Response(working_session+" delete successful")
        else:
            return Response("bad request")
    
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def operationAPIv1(request):
    if request.method == 'POST':
        session_id = request.data['session_id']
        equation = request.data['equation']
        try:
            parsed = parse_eq(str(equation))
        except:
            return Response("bad equation")

        session = PersistentSession.objects.get(session_id=session_id)
        set_obj = IntegerSet.objects.create(set_id=create_set_id(),session_id=session)

        index = 0
        for int_val in parsed:
            Integer.objects.create(set_id=set_obj,index=index,X=int_val)
            index += 1
        return Response(set_obj.set_id)
    
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


def create_set_id():
    set_id = hash(str(datetime.utcnow())+server_secret)
    set_utf = str(set_id).encode("utf-8")
    return hexlify(set_utf).decode('utf-8')

