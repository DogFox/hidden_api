from rest_framework import serializers
from datetime import datetime
from .models import User,SecretBox, Membership

class UserSerializer( serializers.ModelSerializer ):
  class Meta:
    model = User
    fields = ( 'id', 'name', 'email' )

class MembershipSerializer( serializers.ModelSerializer ):
  class Meta:
    model = Membership
    fields = ('id', 'secretbox', 'santa', 'member')

class SecretBoxSerializer( serializers.ModelSerializer ):
  memberships = MembershipSerializer(source='secretboxs', many=True, read_only=True)
  class Meta:
    model = SecretBox
    fields = ('id', 'name', 'admin', 'description', 'memberships')