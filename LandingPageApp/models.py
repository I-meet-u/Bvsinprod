from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.
from RegistrationApp.models import SelfRegistration, BasicCompanyDetails




class CompanyReviewAndRating(models.Model):
    user_id=models.ForeignKey(SelfRegistration,on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=200,null=True,blank=True)
    company_code=models.ForeignKey(BasicCompanyDetails,on_delete=models.CASCADE,null=True,blank=True)
    company_name = models.CharField(max_length=200, null=True, blank=True)
    review=models.TextField(null=True,blank=True)
    rating=models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    created_on = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_on = models.DateTimeField(auto_now=True,null=True,blank=True)

    class Meta:
        db_table = "CompanyReviewAndRating"

