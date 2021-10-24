from django.db import models
from django.contrib.auth.models import User

class CreateUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    userfirstname=models.CharField(max_length=100)
    userlastname=models.CharField(max_length=100)
    userverification=models.CharField(max_length=255, blank=True, null=True)
    useractivationcode=models.CharField(max_length=20, blank=True, null=True)
    userresetpassword=models.CharField(max_length=20, blank=True, null=True)
    userphone=models.CharField(max_length=20)
    user_role=models.CharField(max_length=100)
