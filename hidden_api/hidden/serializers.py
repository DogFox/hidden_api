from rest_framework import serializers
from datetime import datetime
from .models import User,SecretBox, Membership

class UserSerializer( serializers.ModelSerializer ):
  class Meta:
    model = User
    fields = ( 'id', 'name', 'email' )

class MembershipSerializer( serializers.ModelSerializer ):
  member_name = serializers.ReadOnlyField(source='member.name')
  member_email = serializers.ReadOnlyField(source='member.email')
  santa_name = serializers.ReadOnlyField(source='santa.name')
  class Meta:
    model = Membership
    fields = ('id', 'secretbox', 'santa', 'member', 'santa_name', 'member_name', 'member_email')

class SecretBoxSerializer( serializers.ModelSerializer ):
  memberships = MembershipSerializer(source='secretboxs', many=True, read_only=True)
  class Meta:
    model = SecretBox
    fields = ('id', 'name', 'admin', 'description', 'memberships')