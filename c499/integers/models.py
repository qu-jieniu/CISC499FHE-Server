from django.db import models

# Create your models here.
class Integers(models.Model):
    user_id =  models.CharField(max_length=40,default="")
    session_id = models.CharField(max_length=40,default="")
    set_id = models.CharField(max_length=40,default="") # 40 for hash value
    index = models.IntegerField(default=0)
    X = models.IntegerField(default=0)
    q = models.IntegerField(default=0)

    def __str__(self):
        return "%s[%d]" % (self.set_id,self.index)
