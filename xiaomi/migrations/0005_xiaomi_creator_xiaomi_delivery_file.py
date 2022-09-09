# Generated by Django 4.0.1 on 2022-09-08 04:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('xiaomi', '0004_alter_status_status_alter_xiaomi_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='xiaomi',
            name='creator',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='xiaomi',
            name='delivery_file',
            field=models.FileField(default=0, unique=True, upload_to='xiaomi/deliveries'),
            preserve_default=False,
        ),
    ]
