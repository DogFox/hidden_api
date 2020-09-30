from django.db import models
from django.apps import apps
# # from .customer import Customer
# class SecretBox(models.Model):
#   name = models.CharField(max_length=200)
#   description = models.CharField(max_length=800, null=True, blank=True)
  
#   # customer_model = apps.get_model('Customer')
#   admin = models.ForeignKey('hidden.User', related_name='admin', on_delete=models.CASCADE, null=True, blank=True)
#   members = models.ManyToManyField('hidden.User', through='SecretboxMembers', through_fields=('user', 'secretbox'))