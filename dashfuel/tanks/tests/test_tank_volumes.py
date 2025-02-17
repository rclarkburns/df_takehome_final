from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from dashfuel.tanks.models import Tank, TankVolume


class TankVolumeTests(APITestCase):
    def setUp(self):
        self.tank = Tank.objects.create(name='Test Tank')
        self.tank_volume_data = {
            'tank': self.tank.id,
            'volume': 100.5
        }
        self.tank_volume = TankVolume.objects.create(
            tank=self.tank,
            volume=50.5
        )

    def test_create_tank_volume(self):
        url = reverse('tankvolume-list')
        response = self.client.post(url, self.tank_volume_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TankVolume.objects.count(), 2)
        self.assertEqual(TankVolume.objects.get(id=response.data['id']).volume, 100.5)

    def test_list_tank_volumes(self):
        url = reverse('tankvolume-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_tank_volume(self):
        url = reverse('tankvolume-detail', args=[self.tank_volume.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['volume'], 50.5)

    def test_update_tank_volume(self):
        url = reverse('tankvolume-detail', args=[self.tank_volume.id])
        updated_data = {
            'tank': self.tank.id,
            'volume': 75.5
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(TankVolume.objects.get(id=self.tank_volume.id).volume, 75.5)

    def test_delete_tank_volume(self):
        url = reverse('tankvolume-detail', args=[self.tank_volume.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(TankVolume.objects.count(), 0)
