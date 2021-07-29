from rest_framework import serializers

from .models import *

class PlanModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlanModel
        fields = '__all__'
        depth = 2