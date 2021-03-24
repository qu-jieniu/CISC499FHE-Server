from rest_framework import serializers 
from .models import Integers

class IntegersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Integers
        fields = '__all__' # do we really want all?


class IntegersSetSerializer(serializers.ModelSerializer):
    integers = IntegersSerializer

    class Meta:
        model = Integers
        fields = ['user_id','session_id','index','X','q'] # set_id is generated

    # def valide(self,attrs) to override validation?