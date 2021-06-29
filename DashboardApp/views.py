from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from .models import *
from .serializers import  *


class InternalVendorView(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = InternalVendor.objects.all()
    serializer_class = InternalVendorSerializer

