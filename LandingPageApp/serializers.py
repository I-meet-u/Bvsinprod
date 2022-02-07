from rest_framework import  serializers

from RegistrationApp.models import SelfRegistration
from .models import CompanyReviewAndRating, Message


class CompanyReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=CompanyReviewAndRating
        fields=('id','user_id','name','company_code','review','rating','company_name')

# class CompanyRatingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=CompanyRating
#         fields=('id','company','user','stars')


class MessageSerializer(serializers.ModelSerializer):
    sender=serializers.SlugRelatedField(many=False,slug_field='username',queryset=SelfRegistration.objects.all())
    receiver=serializers.SlugRelatedField(many=False,slug_field='username',queryset=SelfRegistration.objects.all())

    class Meta:
        model=Message
        fields=['sender','receiver','messages','created_time','company_name_sender','company_name_receiver','sender_files','receiver_files','sender_images','receiver_images','sender_designation','receiver_designation']