# Django
from django.core import serializers as dserializers

# DRF
from rest_framework import serializers

# Project
from .models import Integer,IntegerSet,PersistentSession
from utils.utils import *

# Misc
import base64

# serialize to dict which JSON can automatically handle
def set_to_dict(set_model):
    ints_data = Integer.objects.filter(set_id = set_model)

    int_data_list = []

    for int_data in ints_data:
        int_values = {}
        int_values["index"] = int_data.index
        int_values["X"] = int_data.X
        int_values["q"] = int_data.q
        int_data_list.append(int_values)

    serialized = {}

    serialized['set_id'] = set_model.set_id
    serialized['integers'] = int_data_list

    return serialized


# serialize to dict which JSON can handle
def session_to_dict(session_model):
    sets_data = IntegerSet.objects.filter(session_id = session_model)

    set_data_list = []

    for set_data in sets_data:
       set_data_list.append(set_to_dict(set_data))

    serialized = {}

    serialized['session_id'] = session_model.session_id
    serialized['integer_sets'] = set_data_list

    return serialized


def deserializeBinaryInt(data,set_instance):
    # create integer instance 
    return Integer.objects.create(set_id=set_instance,index=int(data['index']),X=bytes(data['X'],'raw_unicode_escape'),q=bytes(data['q'],'raw_unicode_escape'))
   

def deserializeSet(data,session_instance): 
    # create set instance 
    return IntegerSet.objects.create(set_id=data['set_id'],session_id=set_instance)



