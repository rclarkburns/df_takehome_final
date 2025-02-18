from dashfuel.tanks.models import Tank, TankVolume, WeeklyTankSales
from django.test import TestCase
from datetime import datetime


class WeeklyTankSalesSampleDataTests(TestCase):
    def setUp(self):
        self.tank = Tank.objects.create(name="Test Tank")

        # Create test data with correct timestamps
        self.test_data = [
            ("2023-01-01 10:00:00+00:00", 30),
            ("2023-01-01 11:00:00+00:00", 10),
            ("2023-01-08 09:00:00+00:00", 20),
            ("2023-01-08 13:00:00+00:00", 45),
            ("2023-01-14 23:00:00+00:00", 60),
            ("2023-01-15 14:00:00+00:00", 30),
            ("2023-01-22 10:00:00+00:00", 70),
            ("2023-01-22 15:00:00+00:00", 50),
            ("2023-01-22 20:00:00+00:00", 25),
            ("2023-01-29 10:30:00+00:00", 49),
            ("2023-01-29 12:30:00+00:00", 12),
            ("2023-02-05 10:00:00+00:00", 12),
            ("2023-02-05 12:00:00+00:00", 25),
            ("2023-02-05 15:00:00+00:00", 42),
            ("2023-02-05 18:00:00+00:00", 20),
        ]

        for created_at, volume in self.test_data:
            TankVolume.objects.create(
                tank=self.tank,
                volume=volume,
                created_at=datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S%z")
            )

    def test_january_first_sales(self):
        weekly_sales = WeeklyTankSales.objects.get(
            tank=self.tank,
            week_end=datetime(2023, 1, 1).date()
        )
        self.assertEqual(weekly_sales.sunday_sales, 20)  # 30-10=20

    def test_january_eighth_sales(self):
        weekly_sales = WeeklyTankSales.objects.get(
            tank=self.tank,
            week_end=datetime(2023, 1, 8).date()
        )
        self.assertEqual(weekly_sales.sunday_sales, 0)  # No sales since 20 < 45

    def test_january_fifteenth_sales(self):
        weekly_sales = WeeklyTankSales.objects.get(
            tank=self.tank,
            week_end=datetime(2023, 1, 15).date()
        )
        self.assertEqual(weekly_sales.sunday_sales, 30)  # 60-30=30

    def test_january_twentysecond_sales(self):
        weekly_sales = WeeklyTankSales.objects.get(
            tank=self.tank,
            week_end=datetime(2023, 1, 22).date()
        )
        self.assertEqual(weekly_sales.sunday_sales, 45)  # 25 + 20 = 45 (two sales: 70 - 50 = 20 and  50-25=25)

    def test_january_twentyninth_sales(self):
        weekly_sales = WeeklyTankSales.objects.get(
            tank=self.tank,
            week_end=datetime(2023, 1, 29).date()
        )
        self.assertEqual(weekly_sales.sunday_sales, 37)  # 25 + 20 = 45 (two sales: 70 - 50 = 20 and  50-25=25)

    def test_february_fifth_sales(self):
        weekly_sales = WeeklyTankSales.objects.get(
            tank=self.tank,
            week_end=datetime(2023, 2, 5).date()
        )
        self.assertEqual(weekly_sales.sunday_sales, 22)
