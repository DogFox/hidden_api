from rest_framework import serializers
from datetime import datetime
from .models import Member, SecretBox, Membership
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
class UserSerializer( serializers.ModelSerializer ):
  class Meta:
    model = User
    fields = ('id', 'email', 'first_name', 'last_name','date_joined', 'password', 'username')
    extra_kwargs = {'password': {'write_only': True}}
    
  def create(self, validated_data):
    user = User(
        email=validated_data['email'],
        username=validated_data['username']
    )
    user.set_password(validated_data['password'])
    user.save()
    # Token.objects.create(user=user)
    return user
  
class ChangePasswordSerializer(serializers.Serializer):
    model = User
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    
class MemberSerializer( serializers.ModelSerializer ):
  class Meta:
    model = Member
    fields = ( 'id', 'name', 'email', 'user', 'wishes')

class MembershipSerializer( serializers.ModelSerializer ):
  member_name = serializers.ReadOnlyField(source='member.name')
  member_email = serializers.ReadOnlyField(source='member.email')
  member_wishes = serializers.ReadOnlyField(source='member.wishes')
  santa_wishes = serializers.ReadOnlyField(source='santa.wishes')
  santa_name = serializers.ReadOnlyField(source='santa.name')
  class Meta:
    model = Membership
    fields = ('id', 'secretbox', 'santa', 'member', 'santa_name', 'member_name', 'member_email', 'member_wishes', 'santa_wishes')

class SecretBoxSerializer( serializers.ModelSerializer ):
  memberships = MembershipSerializer(source='secretboxs', many=True, read_only=True)
  santas = serializers.SerializerMethodField()

  def get_santas(self, obj):
    user = self.context['request'].user
    members = Member.objects.filter(user=user)
    memberships = Membership.objects.filter(santa__in=members, secretbox=obj)
    serializer = MembershipSerializer(memberships, many=True)
    return serializer.data

  class Meta:
    model = SecretBox
    fields = ('id', 'name', 'admin', 'description', 'memberships', 'santas', 'limit', 'limitValue')

  def get_fields(self, *args, **kwargs):
    fields = super().get_fields(*args, **kwargs)
    request = self.context.get('request')
    if request is not None :
      params = request.query_params
      if params.get('admin') == 'false' or not params.get('admin'):
          fields.pop('memberships', None)
    return fields