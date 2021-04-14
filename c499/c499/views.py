# DRF 
from rest_framework import status
from rest_framework.authtoken.models import Token 
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# misc
from datetime import datetime

@api_view(['GET'])
def statusAPIv1(request):
    status_message = {}
    
    if request.method == 'GET':

        status_message["django"] = "ok"

        # check database
        try: 
            _ = len(Token.objects.all()) # forces evaluation
            status_message["database"] = "ok"
            return Response(status_message, status=status.HTTP_200_OK)
        except Exception as err:
            status_message["database"] = "error: " + str(err)
            return Response(status_message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

'''
# create PersistentSession when BaseSession is created
@receiver(post_save,sender=SessionBase)
def create_auth_token(sender,instance=None,created=False,**kwargs):
    if created:
        PersistentSession.objects.create(session_id=instance.get('sessionid'),user_id=)
'''