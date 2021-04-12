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
from .models import Integer,IntegerSet,PersistentSession
from .serializers import *
from utils.utils import *
from utils.eqparser import *
# Misc
import base64
from binascii import hexlify
from datetime import datetime
from hashlib import sha1,sha256
import jwt as jwt_utils
import json
import copy

with open('etc\config.json','r') as config_file:
    config = json.load(config_file)


@api_view(['GET','POST','DELETE'])
def setAPIv1(request):
    status_message = {}

    # get JWT and obtain corresponding device token object
    try:
        jwt = request.headers["Authorization"]
    except KeyError:
        status_message['authError'] = "JWT not supplied"
        return Response(status_message,status=status.HTTP_401_UNAUTHORIZED)

    try:
        jwt = strip_bearer(jwt)
        secret_key = sha256(config['SECRET_KEY'].rstrip().encode('utf-8')).hexdigest()
        decode_jwt = jwt_utils.decode(jwt, secret_key, algorithms=["HS256"])
        token = Token.objects.get(key=decode_jwt['token'])
    except ValueError:
        status_message['authError'] = "device token supplied, need JWT"
        return Response(status_message,status=status.HTTP_400_BAD_REQUEST)
    except Token.DoesNotExist:
        status_message['authError'] = "invalid JWT"
        return Response(status_message,status=status.HTTP_401_UNAUTHORIZED)

    # get session_id from cookie
    try:
        session_id = request.COOKIES['sessionid']
    except KeyError:
        status_message['sessionError'] = "session cookie not supplied"
        return Response(status_message,status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        # query existence of session, if PersistentSession doesn't exist set doesn't either
        try:
            session = PersistentSession.objects.get(session_id=session_id)
            working_set = request.data['set_id']
        except PersistentSession.DoesNotExist:
            status_message['sessionError'] = "invalid session_id"
            return Response(status_message,status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            status_message['argError'] = "set_id not supplied"
            return Response(status_message,status=status.HTTP_400_BAD_REQUEST)

        queried = IntegerSet.objects.filter(set_id=working_set)

        # Check if queried set has any values (if set exists in DB)
        if not queried:
            status_message["invalidArgument"] = "set_id not found"
            return Response(status_message,status=status.HTTP_400_BAD_REQUEST)
        else:
            set_dict = set_to_dict(queried)
            return Response(set_dict,status=status.HTTP_200_OK)

    elif request.method == 'POST':
        # load PersistentSession, if DNE for current session this is first post, create PersistentSession
        try:
            session = PersistentSession.objects.get(session_id=session_id)
        except PersistentSession.DoesNotExist:
            session = PersistentSession.objects.create(user_id=token,session_id =session_id)
            status_message['session_id'] = session_id

        
        request.data['set_id']=create_set_id()
        
        serializer = IntegerSetSerializer(data = request.data) 
        
        
        if serializer.is_valid():        
            status_message['set_id'] = serializer.validated_data['set_id'] 
            serializer.validated_data['session_id']=session
            serializer.save()
            return Response(status_message,status=status.HTTP_200_OK)
        else:
            status_message["serializerError"] = serializer.errors
            return Response(status_message, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # If PersistentSession DNE, set DNE
        try:
            session = PersistentSession.objects.get(session_id=session_id)
        except PersistentSession.DoesNotExist:
            status_message['sessionError'] = "invalid session_id"
            return Response(status_message,status=status.HTTP_400_BAD_REQUEST)

        # get set_id from request
        try:
            working_set = request.data['set_id']
        except KeyError:
            status_message['argError'] = "set_id not supplied"
            return Response(status_message,status=status.HTTP_400_BAD_REQUEST)

        queried = IntegerSet.objects.get(set_id=working_set)

        # check if set exists in database
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
    status_message = {}

    try:
        jwt = request.headers["Authorization"]
        jwt = strip_bearer(jwt)
        decode_jwt = jwt_utils.decode(jwt, 'a-=!v#7apaipy8!pkq$rhyt0he@t%3!+irci7ytp_(t&03z(tt', algorithms=["HS256"])
        token = Token.objects.get(key=decode_jwt['token'])
    except KeyError:
        status_message['authError'] = "JWT not supplied"
        return Response(status_message,status=status.HTTP_401_UNAUTHORIZED)
    except ValueError:
        status_message['authError'] = "device token supplied, need JWT"
        return Response(status_message,status=status.HTTP_400_BAD_REQUEST)
    except Token.DoesNotExist:
        status_message['authError'] = "invalid JWT"
        return Response(status_message,status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':
        # get session_id from header
        try:
            working_session = request.data['session_id']
        except KeyError:
            status_message['argError'] = "session_id not provided"
            return Response(status_message,status=status.HTTP_400_BAD_REQUEST)

        queried = PersistentSession.objects.get(session_id=working_session)

        # check if PersistentSession exists in database
        if not queried:
            status_message["sessionError"] = "session_id does not exist"
            return Response(status_message,status=status.HTTP_400_BAD_REQUEST)
        else:
            session_dict = session_to_dict(queried)
            return Response(session_dict,status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = PersistentSessionSerializer(data = request.data)
        serializer.initial_data['user_id'] = token

        if serializer.is_valid():
            try:
                serializer.save()
            except err:
                status_message["serviceError"] = "unexpected error adding to db"
                return Response(status_message,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            status_message["sessionPosted"] = serializer.validated_data["session_id"]
            return Response(status_message,status=status.HTTP_200_OK)
        else:
            status_message["serializerError"] = serializer.errors
            return Response(status_message,status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            working_session = request.data['session_id']
        except KeyError:
            status_message['argError'] = "session_id not provided"
            return Response(status_message,status=status.HTTP_400_BAD_REQUEST)

        queried = PersistentSession.objects.get(set_id=working_session)

        if not queried:
            status_message["sessionError"] = "session_id does not exist"
            return Response(status_message,status=status.HTTP_400_BAD_REQUEST)
        else:
            queried.delete()
            status_message[working_session] = "deleted"
            return Response(status_message,status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def operationAPIv1(request):
    try:
        jwt = request.headers["Authorization"]
        jwt = strip_bearer(jwt)
        decode_jwt = jwt.decode(jwt, 'a-=!v#7apaipy8!pkq$rhyt0he@t%3!+irci7ytp_(t&03z(tt', algorithms=["HS256"])
        token = Token.objects.get(key=decode_jwt['token'])
    except KeyError:
        status_message['authError'] = "JWT not supplied"
        return Response(status_message,status=status.HTTP_401_UNAUTHORIZED)
    except ValueError:
        status_message['authError'] = "device token supplied, need JWT"
        return Response(status_message,status=status.HTTP_400_BAD_REQUEST)
    except Token.DoesNotExist:
        status_message['authError'] = "invalid JWT"
        return Response(status_message,status=status.HTTP_401_UNAUTHORIZED)

    try:
        session_id = request.COOKIES['sessionid']
    except KeyError:
        status_message['sessionError'] = "session cookie not supplied"
        return Response(status_message,status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'POST':
        try:
            equation = request.data['equation']
        except KeyError:
            status_message['operationError'] = "no equation provided"
            return Response(status_message,status=status.HTTP_400_BAD_REQUEST)

        try:
            parsed = parse_eq(str(equation))
        except err:
            status_message['operationError'] = str(err)
            return Response(status_message,status=status.HTTP_400_BAD_REQUEST)

        try:
            session = PersistentSession.objects.get(session_id=session_id)
        except PersistentSession.DoesNotExist:
            session = PersistentSession.objects.create(session_id=session_id,user_id=token)
            status_message['sessionCreated'] = session_id

        set_obj = IntegerSet.objects.create(set_id=create_set_id(),session_id=session)

        index = 0
        for int_val in parsed:
            Integer.objects.create(set_id=set_obj,index=index,X=int_val)
            index += 1
        status_message['setCreated'] = set_obj.set_id
        return Response(status_message,status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
