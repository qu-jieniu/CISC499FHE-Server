from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from hashlib import sha1
from datetime import datetime

from binascii import hexlify

from lark import Lark,Transformer

from .serializers import IntegersSerializer,IntegersSetSerializer

from .models import Integers
import base64


# Create your views here.

server_secret = "cisc499"
 
@api_view(['GET'])
def index(request):
    # list out url paths available to user
    api_urls = {
        'integers':'/session/'    
    }
    return Response(api_urls)

@api_view(['GET'])
#@authentication_classes([TokenAuthentication])
#@permission_classes([IsAuthenticated])
def integerList(request):
    integers = Integers.objects.all()
    serializer = IntegersSerializer(integers,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def integerBySet(request,set_id):
    integers = Integers.objects.filter(set_id=set_id)
    serializer = IntegersSerializer(integers,many=True)
    return Response(serializer.data)


@api_view(['POST']) # currently only works with JSON list [{..}] 
def post_setV2(request):
    set_id = hash(str(datetime.utcnow())+server_secret)
        
    set_utf = str(set_id).encode("utf-8")

    hexed = hexlify(set_utf).decode('utf-8')

    for index in request.data:
        serializer = IntegersSerializer(data=index)    

        if serializer.is_valid():
            
            serializer.validated_data["set_id"] = hexed
        
            serializer.save()

    return Response(hexed)

def post_set(request):
    # user_id
    # session_id
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    
    user_id = body['user_id']
    session_id = body['session_id']
    
    # generate set ID
    set_id = sha1(server_secret + str(datetime.now))

    # input all elements of set to database under set id
    elements = [] # [(X0,q0),(X1,q1),...]
    for key in body: # key -> (X,q)
        if key != 'user_id' or key != 'session_id':
            elements[int(key)] = body[key]

    temp = None
    index = 0
    for elem in elements:
        temp = models.Integers(user_id = user_id, session_id=session_id, set_id = set_id, index=index, X=elem[0],q=elem[1])
        temp.save()
        index += 1

    # return set id
    return HttpResponse(set_id)

def post_session(request):
    # iterate over all sets in session
    # check existence
    test = models.Integers.objects.all()
    # post any sets in session that do not exists

    # return successfully posted
    return HttpResponse("this is a value: " + str(test[0].X))

def post_operation(request):
    # run_parser

    # run_transformer

    # generate new set ID and store under set ID

    # return new set ID
    return HttpResponse("this is ID of the new set:")


def get_set(request):
    # encode in form
    # { user_id
    #   session_id
    #   set_id
    #   0 : (X0,q0)
    #   ...
    # }

    return HttpResponse("these are the values of your sets")

def get_session(request):
    # same encoding form but multiple sets under the session
    return HttpResponse("These are the sets and their values of your session")



