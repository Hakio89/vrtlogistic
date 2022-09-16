from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.



class Xiaomi(models.Model):
    
    delivery = models.CharField(max_length=50, unique=True)
    reckoning = models.CharField(max_length=50, blank=True, null=True)
    creator = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    date = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey("Status", on_delete=models.CASCADE)
    file = models.FileField(upload_to="xiaomi/deliveries/", blank=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, 
                          editable=False)
    
    def __str__(self):
        return str(self.delivery)
    
class Status(models.Model):
    
    status = models.CharField(max_length=50)
    
    def __str__(self):
        return str(self.status)
    
class XiaomiPartsCatalog(models.Model):

    parts_catalog = models.CharField(max_length=50, unique=False, default="Parts Catalog")
    date = models.DateTimeField(auto_now_add=True)
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

    
