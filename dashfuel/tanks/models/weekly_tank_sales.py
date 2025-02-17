from django.db import models
from django.core.validators import MinValueValidator
from datetime import timedelta
from .tank import Tank


class WeeklyTankSales(models.Model):
    tank = models.ForeignKey(Tank, on_delete=models.CASCADE)
    week_start = models.DateField()
    week_end = models.DateField()
    monday_sales = models.FloatField(default=0, validators=[MinValueValidator(0)])
    tuesday_sales = models.FloatField(default=0, validators=[MinValueValidator(0)])
    wednesday_sales = models.FloatField(default=0, validators=[MinValueValidator(0)])
    thursday_sales = models.FloatField(default=0, validators=[MinValueValidator(0)])
    friday_sales = models.FloatField(default=0, validators=[MinValueValidator(0)])
    saturday_sales = models.FloatField(default=0, validators=[MinValueValidator(0)])
    sunday_sales = models.FloatField(default=0, validators=[MinValueValidator(0)])
    total_sales = models.FloatField(default=0, validators=[MinValueValidator(0)])
    total_sales_count = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['tank', 'week_end']
        indexes = [
            models.Index(fields=['tank', 'week_end']),
        ]

    @property
    def day_field_mapping(self):
        return {
            0: 'monday_sales',
            1: 'tuesday_sales',
            2: 'wednesday_sales',
            3: 'thursday_sales',
            4: 'friday_sales',
            5: 'saturday_sales',
            6: 'sunday_sales',
        }

    @classmethod
    def get_average_sales(cls, target_date):
        week_start = target_date - timedelta(days=target_date.weekday())
        week_end = week_start + timedelta(days=6)
        start_date = week_end - timedelta(weeks=4)

        sales = cls.objects.filter(
            week_end__gte=start_date,
            week_end__lte=week_end
        ).values('total_sales', 'total_sales_count')

        total_sales = sum(sale['total_sales'] for sale in sales)
        total_count = sum(sale['total_sales_count'] for sale in sales)

        return total_sales / total_count if total_count > 0 else 0
