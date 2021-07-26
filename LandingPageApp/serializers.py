from rest_framework import  serializers
from .models import CompanyReview,CompanyRating

class CompanyReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=CompanyReview
        fields=('id','company_name','company_review','no_of_ratings','avg_rating','user')

class CompanyRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model=CompanyRating
        fields=('id','company','user','stars')