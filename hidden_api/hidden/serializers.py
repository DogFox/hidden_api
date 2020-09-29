from rest_framework import serializers
from datetime import datetime
from .models import Customer,SecretBox

class CustomerSerializer( serializers.ModelSerializer ):
  class Meta:
    model = Customer
    fields = ( 'id', 'name', 'email')

  # def __init__(self, customer, **kwargs):
  #   super(CustomerSerializer, self).__init__({customer['name'], customer['email']}, **kwargs)
    # self.random_id = randint(1, 5)
  
  # def __init__( self, customer, **kwargs):
  #   self.name = customer.name
  #   self.email = customer.email

class SecretBoxSerializer( serializers.ModelSerializer ):
  members = CustomerSerializer(many=True, read_only=True)
  class Meta:
    model = SecretBox
    fields = ('id', 'name', 'admin', 'members')