from django.shortcuts import render
from rest_framework.decorators import api_view

# Create your views here.
from .models import Customer
from .serializers import CustomerSerializer
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
      for santa in request.data:
        santa.pop('id')

        serializer = CustomerSerializer(data=santa)
        if not serializer.is_valid():
          return Response(data=serializer.errors, status=401)
          
        Customer.objects.create( **santa )
        
    return Response( status=status.HTTP_201_CREATED)
        # return self.post( self, santa )

  # def post(self, request, *args, **kwargs):
  #       if (name := request.data.get("name1")) and (
  #           email := request.data.get("email1")
  #       ):

  #           request.data["name"] = name
  #           request.data["email"] = email
  #           return self.create(request, *args, **kwargs)

  #       return self.create(request, *args, **kwargs)