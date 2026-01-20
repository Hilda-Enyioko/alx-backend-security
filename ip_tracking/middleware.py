from django.utils.deprecation import MiddlewareMixin
from .utils import get_client_ip

# A middleware to track IP addresses of incoming requests and log them.
from .models import RequestLog
class IPTrackingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ip_address = get_client_ip(request)
        path = request.path
        # Log the request
        RequestLog.objects.create(ip_address=ip_address, path=path)
        
    

# A middleware to block requests from all IP addresses in the BlockedIP model
# and return 403 Forbidden.
from .models import BlockedIP
from django.http import HttpResponseForbidden

class IPBlockMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ip_address = get_client_ip(request)
        # Check if the IP is blocked
        if BlockedIP.objects.filter(ip_address=ip_address).exists():
            return HttpResponseForbidden("Your IP address has been blocked.")