from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import city, doctor
from .serializers import cityserializer, doctorserializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.authentication import SessionAuthentication

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return request.user.is_staff
        
from django.http import HttpResponse
from .models import doctor

def my_view(request):
    # get the Arabic text from your model
    arabic_text = doctor.objects.get(id=1).dr_adress
    
    # create an HTTP response with the Arabic text encoded as UTF-8
    response = HttpResponse(arabic_text, content_type='text/plain; charset=utf-8')
    
    return response

class citydetailView(generics.RetrieveAPIView):
    queryset = city.objects.all()
    serializer_class = cityserializer
    permission_classes = [IsAdminOrReadOnly]
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        if instance:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'Message': 'No city Found'}, status=status.HTTP_404_NOT_FOUND)
        
