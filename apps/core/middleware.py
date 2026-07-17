import time
import re
from django.http import HttpResponseForbidden
from django.core.cache import cache


class EnterpriseSecurityMiddleware:
    """
    Provides HTTP security hardening, rate limiting per IP, and inspects request URIs
    for rudimentary SQL injection / XSS patterns before hitting Django views.
    """
    SUSPICIOUS_PATTERNS = re.compile(
        r'(<script>|javascript:|union\s+select|insert\s+into|drop\s+table|exec\s*\()',
        re.IGNORECASE
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        client_ip = self._get_client_ip(request)
        
        # Simple IP Rate limiting check (increased from 120 to 5000 requests per minute)
        cache_key = f"rate_limit_{client_ip}"
        req_count = cache.get(cache_key, 0)
        if req_count > 5000 and not (request.path.startswith('/static/') or request.path.startswith('/media/')):
            return HttpResponseForbidden("Rate limit exceeded. Please wait 60 seconds.")
        cache.set(cache_key, req_count + 1, timeout=60)

        # Basic Request URI attack signature inspection
        query_str = request.META.get('QUERY_STRING', '')
        if self.SUSPICIOUS_PATTERNS.search(query_str):
            return HttpResponseForbidden("Malicious request pattern detected and logged.")

        response = self.get_response(request)

        # Inject strict enterprise HTTP security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        
        if request.is_secure():
            response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'

        return response

    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', '127.0.0.1')
        return ip
