import random
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.conf import settings

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
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework_jwt.utils import jwt_payload_handler
from rest_framework_jwt.utils import jwt

from .email import send

class UserCreate(generics.CreateAPIView):
  permission_classes = ()
  authentication_classes = ()
  serializer_class = UserSerializer

class UserLogin(APIView): 
  permission_classes = ()
  authentication_classes = ()

  def post(self, request):
    try:
        username = request.data['username']
        password = request.data['password']
 
        user = authenticate(username=username, password=password)
        if user:
            try:
                payload = jwt_payload_handler(user)
                token = jwt.encode(payload, settings.SECRET_KEY)
                user_details = {}
                user_details['name'] = "%s %s" % (
                    user.first_name, user.last_name)
                user_details['token'] = token
                # user_logged_in.send(sender=user.__class__,request=request, user=user)
                return Response(user_details, status=status.HTTP_200_OK)
 
            except Exception as e:
                raise e
        else:
            res = {
                'error': 'can not authenticate with the given credentials or the account has been deactivated'}
            return Response(res, status=status.HTTP_403_FORBIDDEN)
    except KeyError:
        res = {'error': 'please provide a email and a password'}
        return Response(res)


    # username = request.data.get("username")
    # password = request.data.get("password")
    # user = authenticate(username=username, password=password)
    # if user:
    #     return Response({"token": user.auth_token.key})
    # else:
    #     return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)


class MemberListCreate( generics.ListCreateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class MemberPartialUpdate(GenericAPIView, UpdateModelMixin):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    def put(self, request, *args, **kwargs):
      return self.partial_update(request, *args, **kwargs)

class SecretPartialUpdate(GenericAPIView, UpdateModelMixin):
    queryset = SecretBox.objects.all()
    serializer_class = SecretBoxSerializer

    def put(self, request, *args, **kwargs):
      return self.partial_update(request, *args, **kwargs)
      
class SecretBoxListView( generics.ListAPIView):
    queryset = SecretBox.objects.all()
    serializer_class = SecretBoxSerializer

    def get_queryset(self):
      user = self.request.user
      members = Member.objects.filter(user=user)
      memberships = Membership.objects.filter(member__in=members)

      return SecretBox.objects.filter(secretboxs__in=memberships)

  
class draft_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SecretBox.objects.all()
    serializer_class = SecretBoxSerializer

    # friends = SecretboxMembersSerializer(source='secretboxmembers_set', many=True)

    
@api_view(['GET'])
def draft_permission( request, pk):
  user = request.user
  box = SecretBox.objects.get(pk=pk)
  if box.admin == user:
    return Response(data={'admin': True}, status=200)
  return Response(data={'admin': False}, status=200)

class membership_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer
    

@api_view(['GET', 'POST', 'DELETE'])
def post_peoples( request):
    if request.method == 'POST': 
      box = request.data['box']
      box['admin'] = request.user.id
      box_serializer = SecretBoxSerializer(data=box)
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

@api_view(['GET', 'POST', 'DELETE'])
def send_emails( request):
  if request.method == 'POST': 
    send()
    # draft(request.data['id'])
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

