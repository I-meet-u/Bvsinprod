from rest_framework import  serializers
from .models import CompanyReviewAndRating

class CompanyReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=CompanyReviewAndRating
        fields=('id','user_id','name','company_code','review','rating','company_name')

# class CompanyRatingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=CompanyRating
#         fields=('id','company','user','stars')