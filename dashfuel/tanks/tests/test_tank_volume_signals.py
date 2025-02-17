from datetime import datetime, date, time, timedelta
from django.test import TestCase
from django.utils import timezone
from dashfuel.tanks.models import Tank, TankVolume, WeeklyTankSales


class TankVolumeSignalTests(TestCase):
    def setUp(self):
        self.tank = Tank.objects.create(name="Test Tank")
        self.today = timezone.now().date()
        self.week_end = self.today + timedelta(days=(6 - self.today.weekday()))

        # Create initial volumes for a day
        self.morning_volume = TankVolume.objects.create(
            tank=self.tank,
            volume=1000,
            created_at=timezone.make_aware(datetime.combine(self.today, time(6, 0)))
        )

        self.evening_volume = TankVolume.objects.create(
            tank=self.tank,
            volume=900,
            created_at=timezone.make_aware(datetime.combine(self.today, time(22, 0)))
        )

    def test_weekly_sales_updates_on_volume_change(self):
        # Verify initial weekly sales
        initial_weekly_sales = WeeklyTankSales.objects.get(
            tank=self.tank,
            week_end=self.week_end
        )
        self.assertEqual(initial_weekly_sales.total_sales, 100)

        # Update evening volume
        self.evening_volume.volume = 800
        self.evening_volume.save()

        # Verify weekly sales were recalculated
        updated_weekly_sales = WeeklyTankSales.objects.get(
            tank=self.tank,
            week_end=self.week_end
        )
        self.assertEqual(updated_weekly_sales.total_sales, 200)
