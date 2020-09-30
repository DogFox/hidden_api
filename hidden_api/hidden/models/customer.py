from django.db import models
from django.apps import apps
# from .secretbox import SecretBox
# Create your models here.
class User(models.Model):
  name = models.CharField(max_length=200)
  email = models.EmailField()
  created_at = models.DateTimeField(auto_now_add=True)

class SecretBox(models.Model):
  name = models.CharField(max_length=200)
  description = models.CharField(max_length=800, null=True, blank=True)
  
  # customer_model = apps.get_model('Customer')
  admin = models.ForeignKey('hidden.User', related_name='admin', on_delete=models.CASCADE, null=True, blank=True)
  members = models.ManyToManyField('hidden.User', through='SecretboxMembers', through_fields=('secretbox', 'user'))

class SecretboxMembers(models.Model):
  secretbox = models.ForeignKey('hidden.SecretBox', models.DO_NOTHING, related_name='secretbox')
  user = models.ForeignKey('hidden.User', models.DO_NOTHING, related_name='user')
  friend = models.ForeignKey('hidden.User', models.DO_NOTHING, related_name='friend', null=True, blank=True)

  class Meta:
      db_table = 'hidden_secretbox_members'
      unique_together = (('secretbox', 'user'),)

  # secret_box_model = apps.get_model('SecretBox')
  # box = models.ForeignKey( 'hidden.SecretBox', related_name='members', on_delete=models.CASCADE, blank=True, null=True )

  
# class Membership(models.Model):
#   # secret_box_model = apps.get_model('SecretBox')
#   box = models.ForeignKey( 'hidden.SecretBox' , on_delete=models.CASCADE)
#   user = models.ForeignKey( 'hidden.Customer' , on_delete=models.CASCADE)