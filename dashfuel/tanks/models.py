from django.db import models
from django.core.validators import MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta


class Tank(models.Model):
    name = models.CharField(max_length=255)


class TankVolume(models.Model):
    tank = models.ForeignKey(Tank, on_delete=models.CASCADE)
    volume = models.FloatField()
    created_at = models.DateTimeField(default=timezone.now)


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


@receiver(post_save, sender=TankVolume)
def update_weekly_sales(sender, instance, created, **kwargs):
    if not created:
        weekly_sales = WeeklyTankSales.objects.filter(tank=instance.tank)
        updates = []

        for sales_record in weekly_sales:
            week_end = sales_record.week_end

            week_volumes = TankVolume.objects.filter(
                tank=instance.tank,
                created_at__date__range=[
                    week_end - timezone.timedelta(days=7),
                    week_end
                ]
            ).order_by('created_at', 'id')

            total_sales = 0
            total_sales_count = 0

            for day_offset, day_field in sales_record.day_field_mapping.items():
                day_date = week_end - timezone.timedelta(days=6-day_offset)
                prev_date = day_date - timezone.timedelta(days=1)

                day_volumes = week_volumes.filter(created_at__date=day_date)
                prev_day_volumes = week_volumes.filter(created_at__date=prev_date)

                daily_sales = 0
                if prev_day_volumes.exists() and day_volumes.exists():
                    prev_day_last_volume = prev_day_volumes.last().volume


                    current_volumes = list(day_volumes)
                    for i in range(len(current_volumes)):
                        if i == 0:
                            if current_volumes[i].volume != prev_day_last_volume:
                                volume_difference = prev_day_last_volume - current_volumes[i].volume
                                if volume_difference >= 0:
                                    daily_sales += volume_difference
                                    total_sales_count += 1
                                    total_sales += daily_sales
                        else:
                            volume_difference = current_volumes[i-1].volume - current_volumes[i].volume
                            if volume_difference >= 0:
                                daily_sales += volume_difference
                                total_sales_count += 1
                                total_sales += daily_sales

                    setattr(sales_record, day_field, daily_sales)
                elif day_volumes.exists():
                    daily_sales = 0
                    current_volumes = list(day_volumes)
                    for i in range(len(current_volumes)):
                        volume_difference = current_volumes[i-1].volume - current_volumes[i].volume
                        if volume_difference >= 0:
                            daily_sales += volume_difference
                            total_sales_count += 1
                            total_sales += daily_sales
                    setattr(sales_record, day_field, daily_sales)
                else:
                    setattr(sales_record, day_field, 0)

            sales_record.total_sales = total_sales
            sales_record.total_sales_count = total_sales_count
            updates.append(sales_record)

        WeeklyTankSales.objects.bulk_update(
            updates,
            ['monday_sales', 'tuesday_sales', 'wednesday_sales', 'thursday_sales', 'friday_sales', 'saturday_sales', 'sunday_sales', 'total_sales', 'total_sales_count']
        )

    else:
        previous_day = instance.created_at.date() - timedelta(days=1)
        previous_volume = TankVolume.objects.filter(
            tank=instance.tank,
            created_at__date=previous_day
        ).order_by('-created_at').first()

        if not previous_volume:
            previous_volume = TankVolume.objects.filter(
                tank=instance.tank,
                created_at__date=instance.created_at.date(),
                created_at__lt=instance.created_at
            ).order_by('-created_at').first()

        volume_difference = previous_volume.volume - instance.volume if previous_volume else 0 - instance.volume
        if volume_difference <= 0:
            volume_difference = 0

        current_date = instance.created_at.date()
        week_start = current_date - timedelta(days=current_date.weekday())
        week_end = week_start + timedelta(days=6)

        weekly_sales, _ = WeeklyTankSales.objects.get_or_create(
            tank=instance.tank,
            week_start=week_start,
            week_end=week_end
        )

        day_field = weekly_sales.day_field_mapping[current_date.weekday()]
        current_day_sales = getattr(weekly_sales, day_field)
        setattr(weekly_sales, day_field, current_day_sales + volume_difference)

        if volume_difference > 0:
            weekly_sales.total_sales_count += 1

        weekly_sales.total_sales += volume_difference
        weekly_sales.save()
