from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import *
from .serializers import *
import razorpay

class RazorpayModelViewset(viewsets.ModelViewSet):
    queryset = RazorpayModel.objects.all()
    serializer_class = RazorpayModelSerializer