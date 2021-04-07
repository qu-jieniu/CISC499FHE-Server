from django.contrib import admin
from django.contrib.sessions.models import Session as AuthSession
# Register your models here.
from .models import IntegerSet,Integer,PersistentSession


class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']


admin.site.register(AuthSession, SessionAdmin)
admin.site.register(Integer)
admin.site.register(IntegerSet)
admin.site.register(PersistentSession)