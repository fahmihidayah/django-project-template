from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.conf import settings
import uuid
# IGNORE-GENERATE
# Create your models here.

UserModel = get_user_model()


class EmailBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):

        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None


class Profile(models.Model):
    user: models.OneToOneField = models.OneToOneField(to=UserModel, on_delete=models.CASCADE, primary_key=True)

    phone_number: models.CharField = models.CharField(max_length=50, default='', null=True)

    image: models.ImageField = models.ImageField(upload_to='profile/', null=True)

