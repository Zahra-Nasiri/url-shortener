from django.conf import settings
from django.core.cache import cache
from django.shortcuts import redirect
import string
import random
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class ShortenURLView(APIView):
    """
    API endpoint for shortening URLs.
    """
    def post(self, request, format=None):
        """
        Shorten a URL and store it in cache.

        Parameters:
        - original_url (str): The original URL to be shortened.

        Returns:
        - Response: A JSON response containing the short URL.
        """
        original_url = request.data.get('original_url')
        if not original_url:
            return Response({'error': 'original_url is required'}, status=status.HTTP_400_BAD_REQUEST)

        random_code = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(4))
        base_url = settings.BASE_URL

        # Set short URL in Redis with a TTL of 2 days (172800 seconds)
        cache.set(random_code, original_url, timeout=172800)

        short_url = f'{base_url}{random_code}'
        return Response({'short_url': short_url}, status=status.HTTP_201_CREATED)


class RedirectOriginalURLView(APIView):
    """
    API endpoint for redirecting to the original URL.
    """
    def get(self, request, short_code, format=None):
        """
        Redirect to the original URL associated with the short code.

        Parameters:
        - short_code (str): The short code representing the URL.

        Returns:
        - Response: A redirect response or a 404 if the URL is not found.
        """
        original_url = cache.get(short_code)

        if original_url:
            # If the short URL exists, update the TTL to 2 days
            cache.touch(short_code, timeout=172800)
            return redirect(original_url)

        # If the short URL doesn't exist, return 404
        return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
