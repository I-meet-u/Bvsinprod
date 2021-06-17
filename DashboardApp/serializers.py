from rest_framework import  serializers

from DashboardApp.models import InternalVendor


class InternalVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model=InternalVendor
        fields="__all__"
