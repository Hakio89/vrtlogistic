# Generated by Django 4.0.1 on 2022-09-08 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xiaomi', '0017_xiaomi_creator'),
    ]

    operations = [
        migrations.AddField(
            model_name='xiaomi',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='xiaomi/deliveries/'),
        ),
    ]
