# Generated by Django 5.1.6 on 2025-02-18 00:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tanks', '0003_weeklytanksales'),
    ]

    operations = [
        migrations.AddField(
            model_name='weeklytanksales',
            name='total_sales_count',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
