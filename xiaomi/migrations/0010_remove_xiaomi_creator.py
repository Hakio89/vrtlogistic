# Generated by Django 4.0.1 on 2022-09-08 04:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('xiaomi', '0009_alter_xiaomi_creator'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='xiaomi',
            name='creator',
        ),
    ]
