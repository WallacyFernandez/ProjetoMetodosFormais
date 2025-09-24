"""
Middleware personalizado para debug de autenticação.
"""

import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class AuthenticationDebugMiddleware(MiddlewareMixin):
    """
    Middleware para debug de autenticação.
    """
    
    def process_request(self, request):
        """Processa a requisição e adiciona logs de debug."""
        if request.path.startswith('/api/'):
            logger.info(f"API Request: {request.method} {request.path}")
            logger.info(f"Headers: {dict(request.headers)}")
            logger.info(f"User: {request.user if hasattr(request, 'user') else 'Not set'}")
            logger.info(f"Authenticated: {request.user.is_authenticated if hasattr(request, 'user') else False}")
            
            # Log do token de autorização
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            if auth_header:
                logger.info(f"Authorization header: {auth_header[:50]}...")
            else:
                logger.warning("No Authorization header found")
    
    def process_response(self, request, response):
        """Processa a resposta e adiciona logs de debug."""
        if request.path.startswith('/api/'):
            logger.info(f"API Response: {request.method} {request.path} - {response.status_code}")
            if response.status_code >= 400:
                logger.warning(f"Error response: {response.status_code} - {response.content[:200]}")
        
        return response
