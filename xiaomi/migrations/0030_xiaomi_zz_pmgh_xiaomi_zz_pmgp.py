# Generated by Django 4.0.1 on 2022-09-19 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xiaomi', '0029_alter_xiaomi_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='xiaomi',
            name='zz_pmgh',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='xiaomi',
            name='zz_pmgp',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
