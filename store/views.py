from rest_framework import views, status
from rest_framework.response import Response
from django.conf import settings
from django.shortcuts import render
from django.core.cache import cache, caches

# Default Timeout of 5 minutes
DEFAULT_TIMEOUT = 5 * 60


class ValuesAPIView(views.APIView):
    def get(self, request):
        get_params = request.GET.get('keys')
        if get_params is None:
            # Get all available keys
            keys = cache.keys('*')
        else:
            keys = get_params.split(',')
            # Reset TTL if get params are passed
            for key in keys:
                cache.touch(key, DEFAULT_TIMEOUT)
        return Response(cache.get_many(keys), status=status.HTTP_200_OK)

    def post(self, request):
        # Reset TTL
        cache.set_many(request.data, DEFAULT_TIMEOUT)
        return Response(cache.get_many(request.data.keys()), status=status.HTTP_201_CREATED)

    def patch(self, request):
        # Similar implementation to post for fault-tolerance
        # Reset TTL
        cache.set_many(request.data, DEFAULT_TIMEOUT)
        return Response(cache.get_many(request.data.keys()), status=status.HTTP_200_OK)
