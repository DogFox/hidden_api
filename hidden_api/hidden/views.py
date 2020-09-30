from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import User
from .models import SecretBox
from .serializers import UserSerializer
from .serializers import SecretBoxSerializer
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.fields import empty
from rest_framework.decorators import api_view
class UserListCreate( generics.ListCreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer


@api_view(['GET', 'POST', 'DELETE'])
def post_peoples( request):
    if request.method == 'POST': 
      box_name = {'name': request.data['box']}
      box_serializer = SecretBoxSerializer(data=box_name)
      if not box_serializer.is_valid():
        return Response(data=box_serializer.errors, status=401)
        
      for santa in request.data['items']:
        santa.pop('id')
        serializer = UserSerializer(data=santa)
        if not serializer.is_valid():
          return Response(data=serializer.errors, status=401)

      new_box = box_serializer.save()
      for santa in request.data['items']:
        santa['box_id'] = new_box.id
        User.objects.create( **santa )

        
    return Response( status=status.HTTP_201_CREATED)

    
class SecretBoxListView( generics.ListAPIView):
  queryset = SecretBox.objects.all()
  serializer_class = SecretBoxSerializer
  
  # def get(self, request, pk, *args, **kwargs):
  #     items = get_object_or_404(SecretBox, id=self.kwargs.get('pk'))
  #     serializer = SecretBoxSerializer(items)
  #     return Response(serializer.data)
  
class draft_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SecretBox.objects.all()
    serializer_class = SecretBoxSerializer