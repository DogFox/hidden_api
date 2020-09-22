from django.db import models

# Create your models here.
class Customer(models.Model):
  name = models.CharField(max_length=200)
  email = models.EmailField()
  created_at = models.DateTimeField(auto_now_add=True)