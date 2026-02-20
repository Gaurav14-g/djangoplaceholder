from django.db import models
from django.contrib.auth.models import User
from django.utils.deconstruct import deconstructible
import uuid
import os


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_no = models.BigIntegerField(null=True)

    def __str__(self):
        return self.user.username  
    

#---Remember----#
# if add more fields in this model then update its own serializer as well as user's serializer
    