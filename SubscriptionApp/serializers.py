from rest_framework import serializers

from .models import *

class RazorpayModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = RazorpayModel
        fields = '__all__'
        depth = 2