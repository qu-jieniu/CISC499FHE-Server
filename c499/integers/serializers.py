from rest_framework import serializers 
from .models import Integer,IntegerSet,Session


class IntegerSerializer(serializers.ModelSerializer):
    index = serializers.IntegerField(required=True,min_value=0)    
    X = serializers.IntegerField(required=True)
    q = serializers.IntegerField(required=True)
    
    class Meta:
        model = Integer
        fields = ['index','X','q']

class IntegerSetGetSerializer(serializers.ModelSerializer):    
    user_id = serializers.CharField(required=False,allow_blank=False)
    session_id = serializers.CharField(required=False,allow_blank=False)
    set_id =  serializers.CharField(required=False,allow_blank=False) 
    
    integers = IntegerSerializer(many=True,read_only=True)
    class Meta:
        model = IntegerSet
        fields = '__all__'

class IntegerSetRequestSerializer(serializers.Serializer):
    user_id = serializers.CharField(required=False,allow_blank=False)
    session_id = serializers.CharField(required=False,allow_blank=False)
    set_id =  serializers.CharField(required=False,allow_blank=False)  


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
        model = Session
        fields = '__all__' 
    
    user_id = serializers.CharField(required=True,allow_blank=False)
    session_id = serializers.CharField(required=True,allow_blank=False)  
    
    integer_sets = IntegerSetSerializer(many=True)

    def create(self,validated_data):
        sets_data = validated_data.pop('integer_sets')
        session = Session.objects.create(**validated_data)
        for set_data in sets_data:
            int_set = IntegerSet.objects.create(session_id=session, set_id=set_data['set_id'])
            ints_data = set_data.pop('integers')
            for int_data in ints_data:
                Integer.objects.create(set_id=int_set,**int_data)
                
        return session

