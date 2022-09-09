from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.



class Xiaomi(models.Model):
    
    delivery = models.CharField(max_length=50, unique=True)
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
    
