# Generated by Django 5.0.6 on 2024-08-02 04:20

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ClaimParts',
            fields=[
                ('claim_part', models.CharField(max_length=50)),
                ('qty', models.IntegerField()),
                ('status', models.CharField(choices=[('Waiting', 'Waiting'), ('Claimed', 'Claimed')], default='Waiting', max_length=50)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='DeliveryDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('so_number', models.CharField(db_column='SO Number', max_length=50)),
                ('parts_number', models.CharField(blank=True, db_column='Parts Number', max_length=50, null=True)),
                ('parts_description', models.CharField(blank=True, db_column='Parts Desciption', max_length=200, null=True)),
                ('qty', models.IntegerField(db_column='qty', null=True)),
            ],
            options={
                'ordering': ['-qty'],
            },
        ),
        migrations.CreateModel(
            name='MailReportReceivers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='PartsCatalog',
            fields=[
                ('parts_catalog', models.CharField(default='Parts Catalog', max_length=50)),
                ('date', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='maitrox/parts-catalog/')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='PartsDetails',
            fields=[
                ('parts_number', models.CharField(blank=True, db_column='Kod pozycji', max_length=50, null=True)),
                ('parts_description', models.CharField(blank=True, db_column='Opis dla serwisu', max_length=200, null=True)),
                ('warehouse', models.CharField(blank=True, db_column='Domyślny magazyn serwisu', max_length=50, null=True)),
                ('id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='WaitingParts',
            fields=[
                ('waiting_parts', models.CharField(default='Waiting Parts', max_length=50)),
                ('date', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='maitrox/waiting-parts/')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='WaitingsDetails',
            fields=[
                ('parts_number', models.CharField(blank=True, db_column='Parts Number', max_length=50, null=True)),
                ('qty', models.IntegerField(db_column='Waiting', null=True)),
                ('id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
            ],
            options={
                'ordering': ['-qty'],
            },
        ),
        migrations.CreateModel(
            name='Maitrox',
            fields=[
                ('delivery', models.CharField(max_length=50, unique=True)),
                ('reckoning', models.CharField(blank=True, max_length=50, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='maitrox/deliveries/')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('business', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='maitrox.business')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maitrox.status')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]
