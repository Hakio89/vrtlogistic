# Generated by Django 4.0.1 on 2022-09-07 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_rename_user_profile_owner_alter_profile_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, default='media/users/profile/images/user-default.png', null=True, upload_to='users/profile/images'),
        ),
    ]