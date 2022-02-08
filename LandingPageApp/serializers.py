from rest_framework import  serializers
from django.utils import timezone

from RegistrationApp.models import SelfRegistration
from RegistrationApp.serializers import SelfRegistrationSerializer
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
    reguser=SelfRegistrationSerializer(required=False)
    class Meta:
        model=Message
        fields=['sender','receiver','messages','created_time','company_name_sender','company_name_receiver','sender_files','receiver_files','sender_images','receiver_images','sender_designation','receiver_designation','sender_name','receiver_name','reguser']

    def create(self, validated_data):
        print(validated_data['sender_files'])
        try:
            if validated_data['sender_files'] == None:
                pass
            if validated_data['receiver_files'] == None:
                pass
            if validated_data['sender_images'] == None:
                pass
            if validated_data['receiver_images'] == None:
                pass
            regobj=SelfRegistration.objects.filter(username=validated_data['sender']).values()
            if len(regobj)==0:
                raise serializers.ValidationError('Sender Register id is not present')
            regobj1 = SelfRegistration.objects.filter(username=validated_data['receiver']).values()
            if len(regobj) == 0:
                raise serializers.ValidationError('Receiver Register id is not present')


            msgobj=Message.objects.create(
                    sender=validated_data['sender'],
                    receiver=validated_data['receiver'],
                    messages=validated_data['messages'],
                    company_name_sender=validated_data['company_name_sender'],
                    company_name_receiver=validated_data['company_name_receiver'],
                    sender_files=validated_data['sender_files'],
                    receiver_files=validated_data['receiver_files'],
                    sender_images=validated_data['sender_images'],
                    receiver_images=validated_data['receiver_images'],
                    sender_designation=validated_data['sender_designation'],
                    receiver_designation=validated_data['receiver_designation'],
                    created_time=timezone.now(),
                    sender_name=regobj[0].get('contact_person'),
                    receiver_name=regobj1[0].get('contact_person'),
                )
            return msgobj
        except(AssertionError):
            raise serializers.ValidationError("Error!")



