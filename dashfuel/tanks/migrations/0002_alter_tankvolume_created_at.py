# Generated by Django 5.1.6 on 2025-02-17 00:03

from django.db import migrations, models
from django.utils import timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tanks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tankvolume',
            name='created_at',
            field=models.DateTimeField(default=timezone.now()),
        ),
    ]
