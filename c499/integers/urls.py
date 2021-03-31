from django.urls import path
from . import views

app_name = 'integers'
urlpatterns = [
    path('set/',views.setAPIv1,name="setAPIv1"),
    path('session/',views.sessionAPIv1,name="sessionAPIv1"),
    path('operation/',views.operationAPIv1,name="operationAPIv1")
]




