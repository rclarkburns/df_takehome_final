from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from dashfuel.tanks.models import Tank


class TankTests(APITestCase):
    def setUp(self):
        self.tank_data = {'name': 'Test Tank'}
        self.tank = Tank.objects.create(name='Existing Tank')

    def test_create_tank(self):
        url = reverse('tank-list')
        response = self.client.post(url, self.tank_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tank.objects.count(), 2)
        self.assertEqual(Tank.objects.get(id=response.data['id']).name, 'Test Tank')

    def test_list_tanks(self):
        url = reverse('tank-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_tank(self):
        url = reverse('tank-detail', args=[self.tank.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Existing Tank')

    def test_update_tank(self):
        url = reverse('tank-detail', args=[self.tank.id])
        updated_data = {'name': 'Updated Tank'}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Tank.objects.get(id=self.tank.id).name, 'Updated Tank')

    def test_delete_tank(self):
        url = reverse('tank-detail', args=[self.tank.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Tank.objects.count(), 0)
