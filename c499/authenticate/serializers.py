from rest_framework import serializers
from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token 

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','password1', 'password2',] 


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].required = False

    def validate(self, attrs):
        attrs.update({'password': ''})
        return super(TokenObtainPairWithoutPasswordSerializer, self).validate(attrs)    


    def get_token(cls, user):
        token = super().get_token(user)
        
        device = Token.objects.get(user=user)

        token['device'] = device.key
    
        return token
