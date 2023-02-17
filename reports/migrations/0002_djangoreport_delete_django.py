# Generated by Django 4.1.6 on 2023-02-16 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DjangoReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DataGenerowania', models.DateTimeField(null=True)),
                ('NrNaprawy', models.CharField(max_length=30)),
                ('DataRejestracji', models.DateField(null=True)),
                ('TypZgloszenia', models.CharField(max_length=255, null=True)),
                ('Roszczenie', models.CharField(max_length=255, null=True)),
                ('ReklamacjaCCS', models.IntegerField(null=True)),
                ('Producent', models.CharField(max_length=255, null=True)),
                ('Model', models.CharField(max_length=20, null=True)),
                ('Status', models.CharField(max_length=255, null=True)),
                ('KodPozycji', models.CharField(max_length=20, null=True)),
                ('KodPozycjiNazwa', models.CharField(max_length=90, null=True)),
                ('KodPozycjiTypNaprawy', models.CharField(max_length=255, null=True)),
                ('StatusWiersza', models.CharField(max_length=255, null=True)),
                ('DataUtworzeniaWiersza', models.DateTimeField(null=True)),
                ('Ilosc', models.IntegerField(null=True)),
            ],
            options={
                'db_table': 'vv_Rpt060_LogistykaCzekajace',
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='Django',
        ),
    ]
