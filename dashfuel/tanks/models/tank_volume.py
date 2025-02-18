from datetime import timedelta
from django.db import models
from django.utils import timezone
from .tank import Tank
from .weekly_tank_sales import WeeklyTankSales


class TankVolume(models.Model):
    tank = models.ForeignKey(Tank, on_delete=models.CASCADE)
    volume = models.FloatField()
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        update = True if self.pk else False
        super().save(*args, **kwargs)
        current_date = self.created_at.date()
        week_start = current_date - timedelta(days=current_date.weekday())
        week_end = week_start + timedelta(days=6)

        weekly_tank_sales, _ = WeeklyTankSales.objects.get_or_create(
            tank=self.tank,
            week_start=week_start,
            week_end=week_end
        )
        if update:
            week_volumes = TankVolume.objects.filter(
                tank=self.tank,
                created_at__date__range=[
                    week_end - timezone.timedelta(days=7),
                    week_end
                ]
            ).order_by('created_at', 'id')

            total_sales = 0
            total_sales_count = 0

            for day_offset, day_field in weekly_tank_sales.day_field_mapping.items():
                daily_sales = 0
                day_date = week_end - timezone.timedelta(days=6-day_offset)
                prev_date = day_date - timezone.timedelta(days=1)
                day_volumes = week_volumes.filter(created_at__date=day_date)
                prev_day_volumes = week_volumes.filter(created_at__date=prev_date)

                if prev_day_volumes.exists() and day_volumes.exists():
                    prev_day_last_volume = prev_day_volumes.last().volume
                    current_volumes = list(day_volumes)
                    for i in range(len(current_volumes)):
                        if i == 0:
                            volume_difference = prev_day_last_volume - current_volumes[i].volume
                        else:
                            volume_difference = current_volumes[i-1].volume - current_volumes[i].volume
                        if volume_difference >= 0:
                            daily_sales += volume_difference
                            total_sales_count += 1
                    total_sales += daily_sales
                    setattr(weekly_tank_sales, day_field, daily_sales)
                elif day_volumes.exists():
                    current_volumes = list(day_volumes)
                    for i in range(len(current_volumes)):
                        volume_difference = current_volumes[i-1].volume - current_volumes[i].volume
                        if volume_difference >= 0:
                            daily_sales += volume_difference
                            total_sales_count += 1
                    total_sales += daily_sales
                    setattr(weekly_tank_sales, day_field, daily_sales)
                else:
                    setattr(weekly_tank_sales, day_field, 0)

            weekly_tank_sales.total_sales = total_sales
            weekly_tank_sales.total_sales_count = total_sales_count
        else:
            previous_day = self.created_at.date() - timedelta(days=1)
            previous_volume = TankVolume.objects.filter(
                tank=self.tank,
                created_at__date=previous_day
            ).order_by('-created_at').first()

            if not previous_volume:
                previous_volume = TankVolume.objects.filter(
                    tank=self.tank,
                    created_at__date=self.created_at.date(),
                    created_at__lt=self.created_at
                ).order_by('-created_at').first()

            volume_difference = previous_volume.volume - self.volume if previous_volume else 0 - self.volume
            if volume_difference <= 0:
                volume_difference = 0

            day_field = weekly_tank_sales.day_field_mapping[current_date.weekday()]
            current_day_sales = getattr(weekly_tank_sales, day_field)
            setattr(weekly_tank_sales, day_field, current_day_sales + volume_difference)

            if volume_difference > 0:
                weekly_tank_sales.total_sales_count += 1

            weekly_tank_sales.total_sales += volume_difference
        weekly_tank_sales.save()
