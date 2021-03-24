"""c499 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

from django.contrib.auth import authenticate

from rest_framework_simplejwt import views as jwt_views
from rest_framework.authtoken import views

from authenticate import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('integers/', include('integers.urls')),
    path('polynomials/',include('polynomials.urls')),
    

    # Device Token
    path('signup/',auth_views.signup,name='signup'), # returns device token after user creation
    path('api/auth/',views.obtain_auth_token,name='token_obtain'), # returns device token existing user

    # JWT 
    path('api/jwt/',auth_views.my_jwt,name="token_obtain_pair"),
    path('api/jwt/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/jwt/verify/', jwt_views.TokenVerifyView.as_view(), name='token_verify'),
]
