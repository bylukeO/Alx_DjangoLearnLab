"""
Custom security middleware for implementing additional security headers.
This middleware adds Content Security Policy headers to enhance security.
"""

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Middleware to add security headers to HTTP responses.
    Implements Content Security Policy (CSP) and other security headers.
    """
    
    def process_response(self, request, response):
        """
        Add security headers to the response.
        
        Args:
            request: The HTTP request object
            response: The HTTP response object
            
        Returns:
            The modified response object with security headers
        """
        # Build Content Security Policy header
        csp_directives = []
        
        # Add each CSP directive if configured in settings
        if hasattr(settings, 'CSP_DEFAULT_SRC'):
            csp_directives.append(f"default-src {settings.CSP_DEFAULT_SRC}")
            
        if hasattr(settings, 'CSP_SCRIPT_SRC'):
            csp_directives.append(f"script-src {settings.CSP_SCRIPT_SRC}")
            
        if hasattr(settings, 'CSP_STYLE_SRC'):
            csp_directives.append(f"style-src {settings.CSP_STYLE_SRC}")
            
        if hasattr(settings, 'CSP_IMG_SRC'):
            csp_directives.append(f"img-src {settings.CSP_IMG_SRC}")
            
        if hasattr(settings, 'CSP_FONT_SRC'):
            csp_directives.append(f"font-src {settings.CSP_FONT_SRC}")
            
        if hasattr(settings, 'CSP_CONNECT_SRC'):
            csp_directives.append(f"connect-src {settings.CSP_CONNECT_SRC}")
            
        if hasattr(settings, 'CSP_FRAME_ANCESTORS'):
            csp_directives.append(f"frame-ancestors {settings.CSP_FRAME_ANCESTORS}")
        
        # Set the CSP header if we have directives
        if csp_directives:
            csp_header_value = "; ".join(csp_directives)
            response['Content-Security-Policy'] = csp_header_value
        
        # Add additional security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = getattr(settings, 'SECURE_REFERRER_POLICY', 'strict-origin-when-cross-origin')
        
        return response