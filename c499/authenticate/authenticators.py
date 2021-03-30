from rest_framework.authtoken.models import Token 

# BEARER -> JWT
# AUTH -> Device Token


class DeviceTokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        try:
            user = Token.objects.get(key=request.headers["auth"])
        except:
            raise AuthenticationFailed('Invalid Device Token')

        return (user, None)