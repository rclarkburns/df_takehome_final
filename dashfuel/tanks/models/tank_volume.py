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
        is_update = bool(self.pk)
        super().save(*args, **kwargs)

        weekly_tank_sales = self._get_weekly_sales_record()

        if is_update:
            self._update_existing_record(weekly_tank_sales)
        else:
            self._handle_new_record(weekly_tank_sales)

        weekly_tank_sales.save()

    def _get_weekly_sales_record(self):
        current_date = self.created_at.date()
        week_start = current_date - timedelta(days=current_date.weekday())
        week_end = week_start + timedelta(days=6)
        return WeeklyTankSales.objects.get_or_create(
            tank=self.tank,
            week_start=week_start,
            week_end=week_end
        )[0]

    def _calculate_daily_sales(self, day_volumes, prev_day_volumes):
        daily_sales = 0
        sales_count = 0

        if not day_volumes.exists():
            return daily_sales, sales_count

        current_volumes = list(day_volumes)
        reference_volume = prev_day_volumes.last().volume if prev_day_volumes.exists() else current_volumes[0].volume

        for current_volume in current_volumes:
            volume_difference = reference_volume - current_volume.volume
            if volume_difference >= 0:
                daily_sales += volume_difference
                sales_count += 1
            reference_volume = current_volume.volume

        return daily_sales, sales_count

    def _update_existing_record(self, weekly_tank_sales):
        week_volumes = TankVolume.objects.filter(
            tank=self.tank,
            created_at__date__range=[
                weekly_tank_sales.week_end - timezone.timedelta(days=7),
                weekly_tank_sales.week_end
            ]
        ).order_by('created_at', 'id')

        total_sales = 0
        total_sales_count = 0

        for day_offset, day_field in weekly_tank_sales.day_field_mapping.items():
            day_date = weekly_tank_sales.week_end - timezone.timedelta(days=6-day_offset)
            prev_date = day_date - timezone.timedelta(days=1)

            day_volumes = week_volumes.filter(created_at__date=day_date)
            prev_day_volumes = week_volumes.filter(created_at__date=prev_date)

            daily_sales, sales_count = self._calculate_daily_sales(day_volumes, prev_day_volumes)
            total_sales += daily_sales
            total_sales_count += sales_count
            setattr(weekly_tank_sales, day_field, daily_sales)

        weekly_tank_sales.total_sales = total_sales
        weekly_tank_sales.total_sales_count = total_sales_count

    def _get_previous_volume(self):
        previous_day = self.created_at.date() - timedelta(days=1)
        return (
            TankVolume.objects.filter(
                tank=self.tank,
                created_at__date=previous_day
            ).order_by('-created_at').first()
            or
            TankVolume.objects.filter(
                tank=self.tank,
                created_at__date=self.created_at.date(),
                created_at__lt=self.created_at
            ).order_by('-created_at').first()
        )

    def _handle_new_record(self, weekly_tank_sales):
        previous_volume = self._get_previous_volume()
        volume_difference = max(0, (previous_volume.volume if previous_volume else 0) - self.volume)

        current_date = self.created_at.date()
        day_field = weekly_tank_sales.day_field_mapping[current_date.weekday()]
        current_day_sales = getattr(weekly_tank_sales, day_field)
        setattr(weekly_tank_sales, day_field, current_day_sales + volume_difference)

        if volume_difference > 0:
            weekly_tank_sales.total_sales_count += 1
            weekly_tank_sales.total_sales += volume_difference
