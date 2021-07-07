from rest_framework import  serializers

from .models import *


class InviteVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model=InviteVendor
        fields="__all__"
