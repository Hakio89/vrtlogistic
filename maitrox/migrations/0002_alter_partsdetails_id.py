# Generated by Django 5.0.6 on 2024-06-12 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maitrox', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partsdetails',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False, unique=True),
        ),
    ]
