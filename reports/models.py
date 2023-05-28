from django.db import models
from django.db import connection, connections


# Create your models here.

class LogisticWaiting(models.Model):
    DataGenerowania = models.DateField()
    NrNaprawy = models.CharField(max_length=30, primary_key=True)
    DataRejestracji = models.DateField(auto_now=False, auto_now_add=False, null=True)
    TypZgloszenia =  models.CharField(max_length=255, null=True)
    Roszczenie = models.CharField(max_length=255, null=True)
    ReklamacjaCCS = models.IntegerField(null=True)
    Producent = models.CharField(max_length=255, null=True)
    Model= models.CharField(max_length=20, null=True)
    Status = models.CharField(max_length=255, null=True)
    KodPozycji = models.CharField(max_length=20, null=True,)
    KodPozycjiNazwa = models.CharField(max_length=90, null=True)
    KodPozycjiTypNaprawy = models.CharField(max_length=255, null=True)
    StatusWiersza = models.CharField(max_length=255, null=True)
    DataUtworzeniaWiersza = models.DateTimeField(null=True)
    Ilosc = models.IntegerField(null=True)

    class Meta:
       managed = False
       db_table = 'django].[vv_Rpt060_LogistykaCzekajace' 

class BuyingOrder(models.Model):
    ZamowienieZakupu = models.CharField(max_length=25)
    Oddzial = models.CharField(max_length=10)
    Magazyn = models.CharField(max_length=25)
    OdwolanieDoDostawcy = models.CharField(max_length=120)
    Stan = models.CharField(max_length=255, null=True)
    Status = models.CharField(max_length=255, null=True)
    KontoDostawcy = models.CharField(max_length=20)
    NazwaDostawcy = models.CharField(max_length=120)
    DataUtworzeniaG = models.DateTimeField(null=True)
    KodPozycji = models.CharField(max_length=20, primary_key=True)
    KodPozycjiNazwa = models.CharField(max_length=90, null=True)
    Ilosc = models.IntegerField(null=True)

    class Meta:
       managed = False
       db_table = 'django].[vv_ZamowieniaZakupu' 
       
class Replacements(models.Model):
    KodPozycji = models.CharField(max_length=20, primary_key=True)
    Zamiennik = models.CharField(max_length=20)
    Glowny = models.IntegerField()


    class Meta:
        managed = False
        db_table = 'django].[vv_Pozycje'    