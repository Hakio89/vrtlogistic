# Generated by Django 4.0.1 on 2022-09-08 04:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_profile_profile_image'),
        ('xiaomi', '0008_xiaomi_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='xiaomi',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.profile'),
        ),
    ]
