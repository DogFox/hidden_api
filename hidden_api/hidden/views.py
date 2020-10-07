import random
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate

from .models import Member
from .models import SecretBox
from .models import Membership
from django.contrib.auth.models import User

from .serializers import UserSerializer
from .serializers import MemberSerializer
from .serializers import SecretBoxSerializer
from .serializers import MembershipSerializer

from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.fields import empty
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

class UserCreate(generics.CreateAPIView):
  permission_classes = ()
  authentication_classes = ()
  serializer_class = UserSerializer

class UserLogin(APIView): 
  permission_classes = ()
  authentication_classes = ()

  def post(self, request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(username=username, password=password)
    if user:
        return Response({"token": user.auth_token.key})
    else:
        return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)


class MemberListCreate( generics.ListCreateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class SecretBoxListView( generics.ListAPIView):
    queryset = SecretBox.objects.all()
    serializer_class = SecretBoxSerializer
  
class draft_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SecretBox.objects.all()
    serializer_class = SecretBoxSerializer
    # friends = SecretboxMembersSerializer(source='secretboxmembers_set', many=True)
class membership_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer

@api_view(['GET', 'POST', 'DELETE'])
def post_peoples( request):
    if request.method == 'POST': 
      box_name = {'name': request.data['box']}
      box_serializer = SecretBoxSerializer(data=box_name)
      if not box_serializer.is_valid():
        return Response(data=box_serializer.errors, status=401)

      if request.data['items']:
        for santa in request.data['items']:
          santa.pop('id')
          serializer = MemberSerializer(data=santa)
          if not serializer.is_valid():
            return Response(data=serializer.errors, status=401)

        new_box = box_serializer.save()
        for santa in request.data['items']:
          try:
            new_user = User.objects.get(email=santa['email'])
          except:
            new_user_serializer = UserSerializer(data={'firstname': santa['name'], 'username': santa['email'], 'email': santa['email'], 'password': santa['email']})
            if not new_user_serializer.is_valid():
              return Response(data=new_user_serializer.errors, status=401)
            new_user = new_user_serializer.save()
          
          santa['user'] = new_user.id
          serializer = MemberSerializer(data=santa)
          serializer.is_valid()
          new_member = serializer.save()
          member = {'secretbox': new_box.id, 'member': new_member.id}
          membership_serializer = MembershipSerializer(data=member)
          if not membership_serializer.is_valid():
            return Response(data=membership_serializer.errors, status=401)
          membership_serializer.save()
      else:
        return Response(data='Массив участников пустой', status=401)
    
    draft(new_box.id)
    return Response( status=status.HTTP_201_CREATED)

@api_view(['GET', 'POST', 'DELETE'])
def swop_peoples( request):
  if request.method == 'POST': 
    draft(request.data['id'])
  return Response(data='Перемешано успешно', status=201)
    
# @api_view(['GET'])
# @authentication_classes(())
# @permission_classes(())
# def check_system( request):
#   API_key = request.META.get('HTTP_AUTHORIZATION')[6:]
  
#   test = 1
#   return Response(data='Проверено', status=201)

def draft(draft_id):
  members = []
  memberships_set = Membership.objects.filter(secretbox=draft_id)
  for membership in memberships_set:
    members.append(membership.member_id)
  
  santas = members.copy()
  used_members = []
  for membership in memberships_set:
    ind_old = members.index(membership.member_id)
    while santas[ind_old] == membership.member_id or santas[ind_old] in used_members:
      random.shuffle(santas)

    used_members.append(santas[ind_old])
    membership.santa = Member.objects.get(pk=santas[ind_old])
    membership.save()

