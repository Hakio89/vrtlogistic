# Generated by Django 4.0.1 on 2022-08-29 05:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('xiaomi', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='status',
            name='delivery',
        ),
        migrations.AddField(
            model_name='xiaomi',
            name='status',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='xiaomi.status'),
            preserve_default=False,
        ),
    ]
