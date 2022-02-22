import datetime

from django.conf import settings
from django.core.cache import cache
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.
from simple_history.models import HistoricalRecords

from MaterialApp.models import VendorProduct_BasicDetails
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


class UserProfile(models.Model):
    user = models.OneToOneField(SelfRegistration, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    def last_seen(self):
        return cache.get('last_seen_%s' % self.user.username)

    def online(self):
        if self.last_seen():
            now = datetime.datetime.now()
            if now > (self.last_seen() + datetime.timedelta(seconds=settings.USER_ONLINE_TIMEOUT)):
                return False
            else:
                return True
        else:
            return False



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
    sender_name=models.CharField(max_length=100,null=True,blank=True)
    receiver_name=models.CharField(max_length=100,null=True,blank=True)
    is_read=models.BooleanField(default=False)
    vendor_product_pk=models.ForeignKey(VendorProduct_BasicDetails,on_delete=models.CASCADE,null=True,blank=True)
    history=HistoricalRecords()

    def __str__(self):
        return self.messages

    class Meta:
        db_table="Message"
        ordering=('created_time',)
