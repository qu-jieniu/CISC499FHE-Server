from rest_framework.authtoken.models import Token 
from utils.utils import strip_token
# BEARER -> JWT
# AUTH -> Device Token


class DeviceTokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        try:
            user = Token.objects.get(key=strip_token(request.headers["Authorization"]))
        except Token.DoesNotExist:
            raise AuthenticationFailed('Invalid Device Token')

        return (user, None)