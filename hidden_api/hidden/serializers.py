from rest_framework import serializers
from datetime import datetime
from .models import User,SecretBox,SecretboxMembers

class UserSerializer( serializers.ModelSerializer ):
  class Meta:
    model = User
    fields = ( 'id', 'name', 'email')

  # def __init__(self, customer, **kwargs):
  #   super(CustomerSerializer, self).__init__({customer['name'], customer['email']}, **kwargs)
    # self.random_id = randint(1, 5)
  
  # def __init__( self, customer, **kwargs):
  #   self.name = customer.name
  #   self.email = customer.email

class SecretBoxSerializer( serializers.ModelSerializer ):
  members = UserSerializer(many=True, read_only=True)
  class Meta:
    model = SecretBox
    fields = ('id', 'name', 'admin', 'description', 'members')

class SecretboxMembersSerializer( serializers.ModelSerializer ):
  class Meta:
    model = SecretboxMembers
    fields = ('id', 'secretbox', 'user')