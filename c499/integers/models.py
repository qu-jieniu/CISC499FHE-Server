# Django
from django.db import models

# DRF
from rest_framework.authtoken.models import Token 

class PersistentSession(models.Model):
    session_id = models.CharField(max_length=40,primary_key=True)
    user_id = models.ForeignKey(Token,on_delete=models.CASCADE,related_name="sessions")

    def __str__(self):
        return "%s (%s)" % (self.session_id,self.user_id.key[:5])

class IntegerSet(models.Model):
    set_id = models.CharField(max_length=40,primary_key=True)
    session_id = models.ForeignKey(PersistentSession,on_delete=models.CASCADE,related_name="integer_sets")

    def __str__(self):
        return self.set_id

class Integer(models.Model):
    class Meta:
        unique_together = (("set_id","index"),) 
        ordering = ['set_id','index']
        # Django/DRF offer no multi-field PK, so
        # will use autogenerated PK, then ensure
        # uniqueness 

    set_id = models.ForeignKey(IntegerSet,related_name="integers",on_delete=models.CASCADE)
    index = models.IntegerField(default=0)
    X = models.IntegerField(default=0)
    q = models.IntegerField(default=0)

    def __str__(self):
        return "%s[%d]" % (self.set_id.set_id,self.index)



