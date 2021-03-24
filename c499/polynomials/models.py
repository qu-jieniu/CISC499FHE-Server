from django.db import models

# Create your models here.
class Integer(models.Model):
    integer_value = models.IntegerField(default=0)

