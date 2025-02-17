from django.test import TestCase
from django.db import IntegrityError
from datetime import datetime, timedelta, UTC
from dashfuel.tanks.models import Tank, WeeklyTankSales, TankVolume


class WeeklyTankSalesTests(TestCase):
    def setUp(self):
        self.tank = Tank.objects.create(name="Test Tank")
        self.base_date = datetime(2023, 11, 15).date()  # Wednesday
        self.week_start = self.base_date - timedelta(days=self.base_date.weekday())
        self.week_end = self.week_start + timedelta(days=6)

    def test_create_weekly_sales(self):
        weekly_sales = WeeklyTankSales.objects.create(
            tank=self.tank,
            week_start=self.week_start,
            week_end=self.week_end,
            monday_sales=100,
            tuesday_sales=200,
            total_sales=300
        )

        self.assertEqual(weekly_sales.tank, self.tank)
        self.assertEqual(weekly_sales.total_sales, 300)
        self.assertEqual(weekly_sales.monday_sales, 100)
        self.assertEqual(weekly_sales.tuesday_sales, 200)

    def test_unique_tank_week_constraint(self):
        WeeklyTankSales.objects.create(
            tank=self.tank,
            week_start=self.week_start,
            week_end=self.week_end
        )

        with self.assertRaises(IntegrityError):
            WeeklyTankSales.objects.create(
                tank=self.tank,
                week_start=self.week_start,
                week_end=self.week_end
            )

    def test_day_field_mapping(self):
        weekly_sales = WeeklyTankSales.objects.create(
            tank=self.tank,
            week_start=self.week_start,
            week_end=self.week_end
        )

        mapping = weekly_sales.day_field_mapping
        self.assertEqual(mapping[0], 'monday_sales')
        self.assertEqual(mapping[1], 'tuesday_sales')
        self.assertEqual(mapping[6], 'sunday_sales')

    def test_auto_update_last_updated(self):
        weekly_sales = WeeklyTankSales.objects.create(
            tank=self.tank,
            week_start=self.week_start,
            week_end=self.week_end
        )

        original_update = weekly_sales.last_updated
        weekly_sales.total_sales = 500
        weekly_sales.save()

        self.assertNotEqual(original_update, weekly_sales.last_updated)

    def test_signal_updates_weekly_sales(self):
        # Create initial volume
        initial_volume = TankVolume.objects.create(
            tank=self.tank,
            volume=1000,
            created_at=datetime.now(UTC) - timedelta(days=1)
        )

        # Create new volume reading (lower than initial)
        new_volume = TankVolume.objects.create(
            tank=self.tank,
            volume=800,
            created_at=datetime.now(UTC)
        )

        # Check if weekly sales record was created and updated
        weekly_sales = WeeklyTankSales.objects.get(
            tank=self.tank,
            week_end__gte=new_volume.created_at.date()
        )

        self.assertEqual(weekly_sales.total_sales, 200)  # 1000 - 800

    def test_signal_ignores_refueling(self):
        # Create initial volume
        initial_volume = TankVolume.objects.create(
            tank=self.tank,
            volume=200,
            created_at=datetime.now(UTC) - timedelta(days=1)
        )

        # Create new volume reading (higher than initial - simulating refueling)
        new_volume = TankVolume.objects.create(
            tank=self.tank,
            volume=1000,
            created_at=datetime.now(UTC)
        )

        # Check if weekly sales record handles refueling correctly
        weekly_sales = WeeklyTankSales.objects.get(
            tank=self.tank,
            week_end__gte=new_volume.created_at.date()
        )

        self.assertEqual(weekly_sales.total_sales, 0)  # No sales recorded for refueling
