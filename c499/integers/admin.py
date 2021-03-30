from django.contrib import admin

# Register your models here.
from .models import IntegerSet,Integer,Session

admin.site.register(Integer)
admin.site.register(IntegerSet)
admin.site.register(Session)