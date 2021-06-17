from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import *
from .serializers import  *

class InternalVendorView(viewsets.ModelViewSet):
    queryset = InternalVendor.objects.all()
    serializer_class = InternalVendorSerializer

