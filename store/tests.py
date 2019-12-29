from django.test import TestCase

from django.test import TestCase
from django.core.cache import cache
from rest_framework.test import APIClient

from uuid import uuid4


class ValuesAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.keys = [f'key_{i}' for i in range(5)]
        for key in self.keys:
            cache.set(key, uuid4())

    def test_getting_all_values(self):
        response = self.client.get('/values/')
        self.assertEqual(response.status_code, 200)
        for key in self.keys:
            self.assertTrue(key in response.data)

    def test_getting_limited_values(self):
        keys = self.keys[:2]
        params = ','.join(keys)
        url = f'/values/?keys={params}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        for key in keys:
            self.assertTrue(key in response.data)
        self.assertFalse(self.keys[2] in response.data)

    def test_creating_values(self):
        data = {'test_key': 'test_data'}
        response = self.client.post('/values/', data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue('test_key' in response.data)
        cache.delete('test_key')

    def test_updating_values(self):
        data = {}
        for key in self.keys[:2]:
            data[key] = 'updated_data'
        response = self.client.patch('/values/', data)
        self.assertEqual(response.status_code, 200)
        for key in self.keys[:2]:
            self.assertEqual(response.data[key], 'updated_data')

    def tearDown(self):
        cache.delete_many(self.keys)
