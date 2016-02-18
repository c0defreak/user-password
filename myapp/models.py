from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class PasswordLog(models.Model):
    user = models.ForeignKey(User)
    password = models.CharField(max_length=16)
