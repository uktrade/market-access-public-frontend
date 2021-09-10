import time

from django.utils.decorators import decorator_from_middleware
from django.utils.deprecation import MiddlewareMixin


class StatsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        """Start time at request coming in"""
        request.start_time = time.time()

    def process_response(self, request, response):
        """End of request, take time"""
        total = time.time() - request.start_time

        # Add the header.
        response["X-Response-Time-Duration-ms"] = int(total * 1000)
        return response


stats = decorator_from_middleware(StatsMiddleware)
