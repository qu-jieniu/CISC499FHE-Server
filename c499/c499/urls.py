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

# Django
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

# DRF_simplejwt
from rest_framework_simplejwt import views as jwt_views
from rest_framework.authtoken import views as token_views

# Project
from authenticate import views as auth_views
from .views import statusAPIv1

urlpatterns = [
    # utilities
    path('admin/', admin.site.urls),
    path('status/',statusAPIv1, name='status'),
    
    # FHE
    path('integers/', include('integers.urls')),
    path('polynomials/',include('polynomials.urls')),
    
    # Device Token
    path('api/auth/obtain/', token_views.obtain_auth_token,name='token_obtain'),
    path('api/auth/signup/',auth_views.signup,name='signup'), 
    path('api/auth/login/', auth_views.login,name='login'),
    path('api/auth/logout/',auth_views.logout,name='logout'),
    path('api/auth/del-logout/',auth_views.del_logout,name='del_logout'),

    # JWT 
    path('api/jwt/',auth_views.obtain_jwt_pair,name="jwt_obtain_pair"),
    path('api/jwt/refresh/', jwt_views.TokenRefreshView.as_view(), name='jwt_refresh'),
    path('api/jwt/verify/', jwt_views.TokenVerifyView.as_view(), name='jwt_verify'),
]
