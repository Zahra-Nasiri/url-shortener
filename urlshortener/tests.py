from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.core.cache import cache

class ShortenURLViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_shorten_url_success(self):
        url = reverse('shorten_url')
        data = {'original_url': 'http://example.com/'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('short_url', response.data)

    def test_shorten_url_missing_original_url(self):
        url = reverse('shorten_url')
        data = {}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

class RedirectOriginalURLViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_redirect_original_url_success(self):
        # Assume a short code has been previously stored in the cache
        short_code = 'abcd'
        cache.set(short_code, 'http://example.com/', timeout=172800)

        url = reverse('redirect_original_url', args=[short_code])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, 'http://example.com/')

    def test_redirect_original_url_not_found(self):
        url = reverse('redirect_original_url', args=['nonexistentcode'])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)
