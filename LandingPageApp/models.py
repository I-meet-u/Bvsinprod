from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.
from RegistrationApp.models import SelfRegistration


class CompanyReview(models.Model):
    company_name=models.CharField(max_length=50,null=True,blank=True)
    company_review=models.TextField(max_length=500,null=True,blank=True)
    user=models.ForeignKey(SelfRegistration,on_delete=models.CASCADE)

    def no_of_ratings(self):
        ratings=CompanyRating.objects.filter(company=self)
        return len(ratings)

    def avg_rating(self):
        sum = 0
        ratings = CompanyRating.objects.filter(company=self)
        for rating in ratings:
            sum+=rating.stars
        if len(ratings)>0:
            return  sum/len(ratings)
        else:
            return  0


    class Meta:
        db_table="CompanyReview"

class CompanyRating(models.Model):
    company=models.ForeignKey(CompanyReview,on_delete=models.CASCADE)
    user=models.ForeignKey(SelfRegistration,on_delete=models.CASCADE)
    stars=models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])

    class Meta:
        db_table = "CompanyRating"

        unique_together=(('user','company'))
        index_together=(('user','company'))
