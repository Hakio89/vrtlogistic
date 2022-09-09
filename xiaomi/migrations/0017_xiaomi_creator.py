# Generated by Django 4.0.1 on 2022-09-08 05:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('xiaomi', '0016_rename_delivery_id_xiaomi_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='xiaomi',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
