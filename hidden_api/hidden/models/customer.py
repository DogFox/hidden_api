from django.db import models
from django.apps import apps
# from .secretbox import SecretBox
# Create your models here.
class Customer(models.Model):
  name = models.CharField(max_length=200)
  email = models.EmailField()
  created_at = models.DateTimeField(auto_now_add=True)

  # secret_box_model = apps.get_model('SecretBox')
  box = models.ForeignKey( 'hidden.SecretBox', related_name='members', on_delete=models.CASCADE, blank=True, null=True )