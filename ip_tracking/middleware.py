# A middleware to track IP addresses of incoming requests and log them.
from django.utils.deprecation import MiddlewareMixin
from .models import RequestLog

class IPTrackingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ip_address = self.get_client_ip(request)
        path = request.path
        # Log the request
        RequestLog.objects.create(ip_address=ip_address, path=path)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip