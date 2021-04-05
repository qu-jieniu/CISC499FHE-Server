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
    if request.method == 'GET':
        status_message = {}
        status_message["django"] = "ok"

        # check database
        try: 
            _ = len(Token.objects.all()) # forces evaluation
            status_message["database"] = "ok"
            return Response(status_message, status=status.HTTP_200_OK)
        except err:
            status_message["database"] = "error: " + str(err)
            return Response(status_message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)