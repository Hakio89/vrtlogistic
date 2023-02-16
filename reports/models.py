from django.db import models

# Create your models here.

class Django(models.Model):
    NrNaprawy = models.CharField(max_length=30)
    DataRejestracji = models.DateField(auto_now=False, auto_now_add=False)
    TypZgloszenia =  models.CharField(max_length=255)
    Roszczenie = models.CharField(max_length=255)
    ReklamacjaCCS = models.IntegerField()
    Producent = models.CharField(max_length=255)
    Model= models.CharField(max_length=20)
    Status = models.CharField(max_length=255)
    KodPozycji = models.CharField(max_length=20)
    KodPozycjiNazwa = models.CharField(max_length=90)
    KodPozycjiTypNaprawy = models.CharField(max_length=255)
    StatusWiersza = models.CharField(max_length=255)
    DataUtworzeniaWiersza = models.DateTimeField()
    Ilosc = models.IntegerField()

