from django.db import models

# Create your models here.
class InternalVendor(models.Model):
    company_name=models.CharField(max_length=200)
    internal_email=models.CharField(max_length=100)
    internal_phone=models.CharField(max_length=15)
    city=models.CharField(max_length=200)
    state=models.CharField(max_length=200)
    location=models.CharField(max_length=500)
    nature_of_business=models.CharField(max_length=100)
    internal_status=models.CharField(default='Pending',max_length=30)
    group=models.CharField(max_length=100)

    class Meta:
        db_table="InternalVendor"

