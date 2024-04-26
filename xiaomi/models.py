from django.db import models
from django.contrib.auth.models import User
import uuid
from django.shortcuts import redirect
from django.urls import reverse

# Create your models here.



class Xiaomi(models.Model):
    
    delivery = models.CharField(max_length=50, unique=True)
    reckoning = models.CharField(max_length=50, blank=True, null=True)
    creator = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    date = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey("Status", on_delete=models.CASCADE)
    zz_pmgp = models.CharField(max_length=50, blank=True, null=True)
    lpr_pmgp = models.CharField(max_length=100, blank=True, null=True)
    status_pmgp = models.ForeignKey("StatusPmgp", on_delete=models.CASCADE, blank=True, null=True)
    zz_pmgh = models.CharField(max_length=50, blank=True, null=True)
    lpr_pmgh = models.CharField(max_length=100, blank=True, null=True)
    status_pmgh = models.ForeignKey("StatusPmgh", on_delete=models.CASCADE, blank=True, null=True)
    file = models.FileField(upload_to="xiaomi/deliveries/", blank=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, 
                          editable=False)
    
    def __str__(self):
        return str(self.delivery)
    
    def get_absolute_url(self):
        return reverse("xiaomi_deliveries", kwargs={"delivery": self.delivery})
    
    class Meta:
        ordering = ['-date']

class DeliveryDetails(models.Model):

    so_number = models.CharField(max_length=50, db_column='SO Number')
    parts_number = models.CharField(max_length=50, blank=True, null=True, db_column='Parts Number')
    parts_description = models.CharField(max_length=200, blank=True, null=True, db_column='Parts Desciption')
    qty = models.IntegerField(blank=False, null=True, db_column='qty')

    
    def __str__(self):
        return str(self.delivery_number)
    
class Status(models.Model):
    
    status = models.CharField(max_length=50)
    
    def __str__(self):
        return str(self.status)
    
class StatusPmgp(models.Model):
    
    status_pmgp = models.CharField(max_length=50)
    
    def __str__(self):
        return str(self.status_pmgp)
    
class StatusPmgh(models.Model):
    
    status_pmgh = models.CharField(max_length=50)
    
    def __str__(self):
        return str(self.status_pmgh)
    
class XiaomiPartsCatalog(models.Model):

    parts_catalog = models.CharField(max_length=50, unique=False, default="Parts Catalog")
    date = models.DateTimeField(auto_now=True)
    file = models.FileField(upload_to="xiaomi/parts-catalog/", blank=True, null=True,)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, 
                          editable=False)
    
    def __str__(self):
        return str(self.parts_catalog)

class XiaomiWaitingParts(models.Model):
    
    waiting_parts = models.CharField(max_length=50, unique=False, default="Waiting Parts")
    date = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="xiaomi/waiting-parts/", blank=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, 
                          editable=False)
    
    def __str__(self):
        return str(self.waiting_parts)

class XiaomiClaimParts(models.Model):    
    STATUS_TYPE = (
        ('Waiting', 'Waiting'),
        ('Claimed','Claimed'),
    )
        
    claim_part = models.CharField(max_length=50, unique=False, blank=False)
    qty = models.IntegerField(unique=False, blank=False, null=False)
    status = models.CharField(max_length=50, choices=STATUS_TYPE, default='Waiting')
    date = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, 
                          editable=False)
    
    
    
    def __str__(self):
        return str(self.claim_part)
    
    
class MailReportReceivers(models.Model):
    
    email = models.EmailField()
    
    def __str__(self):
        return str(self.email)

    
