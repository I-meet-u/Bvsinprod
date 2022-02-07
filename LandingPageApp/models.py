from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.
from simple_history.models import HistoricalRecords

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


class Message(models.Model):
    sender=models.ForeignKey(SelfRegistration,on_delete=models.CASCADE,related_name='sender')
    receiver = models.ForeignKey(SelfRegistration, on_delete=models.CASCADE, related_name='receiver')
    messages=models.TextField(null=True,blank=True)
    company_name_sender=models.CharField(max_length=500,null=True,blank=True)
    company_name_receiver=models.CharField(max_length=500,null=True,blank=True)
    sender_files=models.FileField(upload_to='MessagesAttachment',null=True,blank=True)
    receiver_files = models.FileField(upload_to='MessagesAttachment', null=True, blank=True)
    sender_images=models.FileField(upload_to='MessageImages',null=True,blank=True)
    receiver_images = models.FileField(upload_to='MessageImages', null=True, blank=True)
    # sender_address=models.TextField(null=True,blank=True)
    # receiver_address = models.TextField(null=True, blank=True)
    sender_designation=models.CharField(max_length=200,null=True,blank=True)
    receiver_designation = models.CharField(max_length=200, null=True, blank=True)
    created_time=models.DateTimeField(auto_now_add=True)
    is_read=models.BooleanField(default=False)
    history=HistoricalRecords()

    def __str__(self):
        return self.messages

    class Meta:
        db_table="Message"
        ordering=('created_time',)
