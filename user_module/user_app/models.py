from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, null=True, blank=True)
    mobile_number = models.CharField(max_length=15, unique=True)

class RoleMaster(models.Model):
    name = models.CharField(max_length=40, unique=True)
    description = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=20)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=20)


class RoleMapping(models.Model):
    role = models.ForeignKey(RoleMaster, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='user_role')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=20)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=20)
