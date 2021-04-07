from rest_framework import serializers 
from .models import Integer,IntegerSet,PersistentSession
from django.core import serializers as dserializers


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

def session_to_dict(session_model):
    sets_data = IntegerSet.objects.filter(session_id = session_model)
    
    set_data_list = []

    for set_data in sets_data:
       set_data_list.append(set_to_dict(set_data))

    serialized = {}
    
    serialized['session_id'] = session_model.session_id
    serialized['integer_sets'] = set_data_list

    return serialized

class IntegerSerializer(serializers.ModelSerializer):
    index = serializers.IntegerField(required=True,min_value=0)    
    X = serializers.IntegerField(required=True)
    q = serializers.IntegerField(required=True)
    class Meta:
        model = Integer
        fields = ['index','X','q']

class IntegerSetSerializer(serializers.ModelSerializer):
    session_id = serializers.CharField(required=False,allow_blank=False)
    set_id =  serializers.CharField(required=False,allow_blank=False)  
    integers =  IntegerSerializer(many=True)
    def create(self, validated_data):
        integers_data = validated_data.pop('integers')
        int_set = IntegerSet.objects.create(**validated_data)
        for integer_data in integers_data:
            Integer.objects.create(set_id=int_set,**integer_data)
        return int_set
    class Meta:
        model = IntegerSet
        fields = '__all__'

class PersistentSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersistentSession
        fields = ['user_id','session_id','integer_sets']
    session_id = serializers.CharField(required=True,allow_blank=False)  
    integer_sets = IntegerSetSerializer(many = True)

    def create(self,validated_data):
        sets_data = validated_data.pop('integer_sets')
        session = PersistentSession.objects.create(**validated_data)
        for set_data in sets_data:
            int_set = IntegerSet.objects.create(session_id=session, set_id=set_data['set_id'])
            ints_data = set_data.pop('integers')
            for int_data in ints_data:
                Integer.objects.create(set_id=int_set,**int_data)    
        return session    




























        

class IntegerSetPostSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(required=True,allow_blank=False)
    session_id = serializers.CharField(required=True,allow_blank=False)
    set_id =  serializers.CharField(required=False,allow_blank=False)  
    integers =  IntegerSerializer(many=True)

    def create(self, validated_data):
        integers_data = validated_data.pop('integers')
        int_set = IntegerSet.objects.create(**validated_data)
        for integer_data in integers_data:
            Integer.objects.create(set_id=int_set,**integer_data)
        return int_set

    class Meta:
        model = IntegerSet
        fields = '__all__'


    
class IntegerSetSerializer(serializers.ModelSerializer):
    set_id =  serializers.CharField(required=True,allow_blank=False)  
    integers =  IntegerSerializer(many=True)

    def create(self, validated_data):

        int_set = IntegerSet.objects.get(set_id=validated_data['set_id'])
        
        for integer_data in integers_data:
            Integer.objects.create(set_id=int_set,**integer_data)
        
        return int_set

    class Meta:
        model = IntegerSet
        fields = ['set_id','integers']

class SessionPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersistentSession
        fields = '__all__' 
    
    user_id = serializers.CharField(required=True,allow_blank=False)
    session_id = serializers.CharField(required=True,allow_blank=False)  
    
    integer_sets = IntegerSetSerializer(many=True)

    def create(self,validated_data):
        sets_data = validated_data.pop('integer_sets')
        session = PersistentSession.objects.create(**validated_data)
        for set_data in sets_data:
            int_set = IntegerSet.objects.create(session_id=session, set_id=set_data['set_id'])
            ints_data = set_data.pop('integers')
            for int_data in ints_data:
                Integer.objects.create(set_id=int_set,**int_data)
                
        return session

