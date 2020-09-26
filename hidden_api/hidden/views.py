from django.shortcuts import render
from rest_framework.decorators import api_view

# Create your views here.
from .models import Customer
from .serializers import CustomerSerializer
from rest_framework import generics
from rest_framework.response import Response
class CustomerListCreate( generics.ListCreateAPIView):
  queryset = Customer.objects.all()
  serializer_class = CustomerSerializer

@api_view(['GET', 'POST', 'DELETE'])
def post_peoples( request):
    if request.method == 'POST': 
      for santa in request.data:
        serializer = CustomerSerializer( **santa)
        serializer.is_valid(raise_exception=True)
        Customer.objects.create( **santa )
        
    return Response( status=HTTP_201_CREATED)
        # return self.post( self, santa )

  # def post(self, request, *args, **kwargs):
  #       if (name := request.data.get("name1")) and (
  #           email := request.data.get("email1")
  #       ):

  #           request.data["name"] = name
  #           request.data["email"] = email
  #           return self.create(request, *args, **kwargs)

  #       return self.create(request, *args, **kwargs)