from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Profile(models.Model):
    nickname = models.CharField(max_length=64)
    user = models.OneToOneField(User,on_delete=models.CASCADE)