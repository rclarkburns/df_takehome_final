# Generated by Django 5.1.6 on 2025-02-17 23:11

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tanks', '0002_alter_tankvolume_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeeklyTankSales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week_start', models.DateField()),
                ('week_end', models.DateField()),
                ('monday_sales', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('tuesday_sales', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('wednesday_sales', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('thursday_sales', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('friday_sales', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('saturday_sales', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('sunday_sales', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('total_sales', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('tank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tanks.tank')),
            ],
            options={
                'indexes': [models.Index(fields=['tank', 'week_end'], name='tanks_weekl_tank_id_705ee7_idx')],
                'unique_together': {('tank', 'week_end')},
            },
        ),
    ]
