from django.test import TestCase
from django.urls import reverse
from rest_framework import status


class AverageSalesTests(TestCase):

    def test_get_average_sales_invalid_date(self):
        url = f"{reverse('average-sales')}?date=invalid-date"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_average_sales_missing_date(self):
        url = reverse('average-sales')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
