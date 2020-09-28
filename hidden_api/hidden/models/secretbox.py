from django.db import models
from django.apps import apps
# from .customer import Customer
class SecretBox(models.Model):
  name = models.CharField(max_length=200)
  
  # customer_model = apps.get_model('Customer')
  admin = models.ForeignKey('hidden.Customer', related_name='admin', on_delete=models.CASCADE)