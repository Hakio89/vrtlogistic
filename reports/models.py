from django.db import models

# Create your models here.

class DjangoReport(models.Model):
    DataGenerowania = models.DateTimeField(primary_key=True)
    NrNaprawy = models.CharField(max_length=30)
    DataRejestracji = models.DateField(auto_now=False, auto_now_add=False, null=True)
    TypZgloszenia =  models.CharField(max_length=255, null=True)
    Roszczenie = models.CharField(max_length=255, null=True)
    ReklamacjaCCS = models.IntegerField(null=True)
    Producent = models.CharField(max_length=255, null=True)
    Model= models.CharField(max_length=20, null=True)
    Status = models.CharField(max_length=255, null=True)
    KodPozycji = models.CharField(max_length=20, null=True)
    KodPozycjiNazwa = models.CharField(max_length=90, null=True)
    KodPozycjiTypNaprawy = models.CharField(max_length=255, null=True)
    StatusWiersza = models.CharField(max_length=255, null=True)
    DataUtworzeniaWiersza = models.DateTimeField(null=True)
    Ilosc = models.IntegerField(null=True)

    class Meta:
       managed = False
       db_table = 'django].[vv_Rpt060_LogistykaCzekajace' 