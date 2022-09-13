# Generated by Django 4.0.1 on 2022-09-11 13:55

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('xiaomi', '0018_xiaomi_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='XiaomiClaimParts',
            fields=[
                ('claim_part', models.CharField(max_length=50)),
                ('qty', models.IntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='XiaomiPartsCatalog',
            fields=[
                ('parts_catalog', models.CharField(default='Parts Catalog', max_length=50)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='xiaomi/parts-catalog/')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='XiaomiWaitingParts',
            fields=[
                ('waiting_parts', models.CharField(default='Waiting Parts', max_length=50)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='xiaomi/waiting-parts/')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
            ],
        ),
    ]
