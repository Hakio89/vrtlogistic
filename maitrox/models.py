from django.db import models
from django.contrib.auth.models import User
import uuid
from django.shortcuts import redirect
from django.urls import reverse


# Create your models here.



class Maitrox(models.Model):
    
    delivery = models.CharField(max_length=50, unique=True)
    reckoning = models.CharField(max_length=50, blank=True, null=True)
    creator = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    date = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey("Status", on_delete=models.CASCADE)
    business = models.ForeignKey("Business", on_delete=models.CASCADE, blank=True, null=True)
    file = models.FileField(upload_to="maitrox/deliveries/", blank=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, 
                          editable=False)
    
    def __str__(self):
        return str(self.delivery)
    
    def get_absolute_url(self):
        return reverse("maitrox_deliveries", kwargs={"delivery": self.delivery})
    
    class Meta:
        ordering = ['-date']
        
class PartsDetails(models.Model):
    
    parts_number = models.CharField(max_length=50, blank=True, null=True,db_column='Kod pozycji')
    parts_description = models.CharField(max_length=200, blank=True, null=True,db_column='Opis dla serwisu')
    warehouse = models.CharField(max_length=50, blank=True, null=True,db_column='Domyślny magazyn serwisu')
    id = models.IntegerField(unique=True, primary_key=True)

class DeliveryDetails(models.Model):

    so_number = models.CharField(max_length=50, db_column='SO Number')
    parts_number = models.CharField(max_length=50, blank=True, null=True, db_column='Parts Number')
    parts_description = models.CharField(max_length=200, blank=True, null=True, db_column='Parts Desciption')
    qty = models.IntegerField(blank=False, null=True, db_column='qty')
    
    def warehouse_type(self):
        return PartsDetails.objects.get(parts_number=self.parts_number).warehouse

    warehouse = property(warehouse_type)
    
    
    def __str__(self):
        return str(self.so_number)
    
    class Meta:
        ordering = ['-qty']
    
class Status(models.Model):
    
    status = models.CharField(max_length=50)
    
    def __str__(self):
        return str(self.status)
    
class Business(models.Model):
    
    business = models.CharField(max_length=50)
    
    def __str__(self):
        return str(self.business)
    
class PartsCatalog(models.Model):

    parts_catalog = models.CharField(max_length=50, unique=False, default="Parts Catalog")
    date = models.DateTimeField(auto_now=True)
    file = models.FileField(upload_to="maitrox/parts-catalog/", blank=True, null=True,)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, 
                          editable=False)
    
    def __str__(self):
        return str(self.parts_catalog)
    


class WaitingParts(models.Model):
    
    waiting_parts = models.CharField(max_length=50, unique=False, default="Waiting Parts")
    date = models.DateTimeField(auto_now=True)
    file = models.FileField(upload_to="maitrox/waiting-parts/", blank=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, 
                          editable=False)
    
    def __str__(self):
        return str(self.waiting_parts)
    
class WaitingsDetails(models.Model):
    
    parts_number = models.CharField(max_length=50, blank=True, null=True,db_column='Parts Number')
    qty = models.IntegerField(blank=False, null=True, db_column='Waiting')
    id = models.IntegerField(unique=True, primary_key=True)

    
    def __str__(self):
        return str(self.parts_number)
    
    class Meta:
        ordering = ['-qty']

class ClaimParts(models.Model):    
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
    
    def get_absolute_url(self):
        return reverse("maitrox_claims", kwargs={"claim_part": self.claim_part})
    
    def __str__(self):
        return str(self.claim_part)
    
    
class MailReportReceivers(models.Model):
    
    email = models.EmailField()
    
    def __str__(self):
        return str(self.email)

    
