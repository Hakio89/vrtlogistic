# Generated by Django 4.0.1 on 2022-09-07 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_profile_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, default='media/users/profile/images/user-default.png', null=True, upload_to='media/users/profile/images'),
        ),
    ]
