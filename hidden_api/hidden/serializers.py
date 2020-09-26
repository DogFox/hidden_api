from rest_framework import serializers
from datetime import datetime
from .models import Customer

class CustomerSerializer( serializers.ModelSerializer ):
  class Meta:
    model = Customer
    fields = ( 'id', 'name', 'email')
