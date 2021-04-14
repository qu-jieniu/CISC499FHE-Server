# DRF 
from rest_framework import status
from rest_framework.authtoken.models import Token 
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# misc
from datetime import datetime
import logging

# create logger instance if needed, named c499.logger
logger = logging.getLogger('c499.logger') 

# return status of django server
# evaluates arbitrary database call to check
# status of db
@api_view(['GET'])
def statusAPIv1(request):
    status_message = {}
    
    if request.method == 'GET':
        # at this point django is definitely working
        status_message["django"] = "ok"

        # check database
        try: 
            _ = len(Token.objects.all()) # forces evaluation
            status_message["database"] = "ok"
            return Response(status_message, status=status.HTTP_200_OK)
        except Exception as err:
            logger.critical("database: "+str(err))
            status_message["database_error"] = str(err)
            return Response(status_message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
