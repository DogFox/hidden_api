from django.db import models
from django.apps import apps
# from .secretbox import SecretBox
class User(models.Model):
  name = models.CharField(max_length=200)
  email = models.EmailField()
  created_at = models.DateTimeField(auto_now_add=True)

class SecretBox(models.Model):
  name = models.CharField(max_length=200)
  description = models.CharField(max_length=800, null=True, blank=True)
  admin = models.ForeignKey('hidden.User', related_name='admin', on_delete=models.CASCADE, null=True, blank=True)
  
class Membership(models.Model):
  secretbox = models.ForeignKey('hidden.SecretBox', models.DO_NOTHING, related_name='secretboxs')
  santa = models.ForeignKey('hidden.User', models.DO_NOTHING, related_name='santas', null=True, blank=True)
  member = models.ForeignKey('hidden.User', models.DO_NOTHING, related_name='members')
