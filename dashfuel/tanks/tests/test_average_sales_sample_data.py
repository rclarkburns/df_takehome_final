from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from datetime import datetime
from dashfuel.tanks.models import Tank, TankVolume


class AverageSalesSampleDataTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.tank = Tank.objects.create(name="Test Tank")

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

        # Create TankVolume entries
        for timestamp, volume in self.test_data:
            TankVolume.objects.create(
                tank=self.tank,
                volume=volume,
                created_at=datetime.fromisoformat(timestamp)
            )

    def test_average_sales_january_29(self):
        url = reverse('average-sales')
        response = self.client.get(f"{url}?date=2023-01-29")

        self.assertEqual(response.status_code, 200)
        # Weekly sales should be calculated from the volume differences:
        # Week 1 (Jan 1): 20 (30-10)
        # Week 2 (Jan 8): 0 (20-45)
        # Week 3 (Jan 15): 30 (60-30)
        # Week 4 (Jan 22): 45 (70-25) (25, 20)
        # Week 5 (Jan 29): 37 (49-12)
        expected_average = (20 + 30 + 25 + 20 + 37) / 5 # 26.4
        self.assertAlmostEqual(response.data['average_sales'], expected_average, places=2)

    def test_average_sales_february_5(self):
        url = reverse('average-sales')
        response = self.client.get(f"{url}?date=2023-02-05")

        self.assertEqual(response.status_code, 200)
        # Weekly sales calculations for Feb 5:
        # Week 1 (Jan 8): 0 (20-45)
        # Week 2 (Jan 15): 30 (60-30)
        # Week 3 (Jan 22): 45 (70-25) (25, 20)
        # Week 4 (Jan 29): 37 (49-12)
        # Week 5 (Feb 5): 22 (42-20)
        expected_average = (30 + 25 + 20 + 37 + 22) / 5 # 26.8
        self.assertAlmostEqual(response.data['average_sales'], expected_average, places=2)
