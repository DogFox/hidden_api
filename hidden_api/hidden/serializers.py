from rest_framework import serializers
from datetime import datetime
from .models import Member, SecretBox, Membership
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
class UserSerializer( serializers.ModelSerializer ):
  class Meta:
    model = User
    fields = ('username', 'email', 'password')
    extra_kwargs = {'password': {'write_only': True}}
    
  def create(self, validated_data):
    user = User(
        email=validated_data['email'],
        username=validated_data['username']
    )
    user.set_password(validated_data['password'])
    user.save()
    Token.objects.create(user=user)
    return user
    
class MemberSerializer( serializers.ModelSerializer ):
  class Meta:
    model = Member
    fields = ( 'id', 'name', 'email', 'user')

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