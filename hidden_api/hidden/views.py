from django.shortcuts import render
from rest_framework.decorators import api_view

# Create your views here.
from .models import Customer
from .models import SecretBox
from .serializers import CustomerSerializer
from .serializers import SecretBoxSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.fields import empty
class CustomerListCreate( generics.ListCreateAPIView):
  queryset = Customer.objects.all()
  serializer_class = CustomerSerializer


@api_view(['GET', 'POST', 'DELETE'])
def post_peoples( request):
    if request.method == 'POST': 
      box_name = {'name': request.data['box']}
      box_serializer = SecretBoxSerializer(data=box_name)
      if not box_serializer.is_valid():
        return Response(data=box_serializer.errors, status=401)
        
      for santa in request.data['items']:
        santa.pop('id')
        serializer = CustomerSerializer(data=santa)
        if not serializer.is_valid():
          return Response(data=serializer.errors, status=401)

      new_box = box_serializer.save()
      for santa in request.data['items']:
        santa['box_id'] = new_box.id
        Customer.objects.create( **santa )

        
    return Response( status=status.HTTP_201_CREATED)

    
class SecretBoxListView( generics.ListAPIView):
  queryset = SecretBox.objects.all()
  serializer_class = SecretBoxSerializer