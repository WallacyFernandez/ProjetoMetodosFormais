"""
Debug personalizado para JWT authentication.
"""

import logging
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

logger = logging.getLogger(__name__)


class DebugJWTAuthentication(JWTAuthentication):
    """
    JWT Authentication com logs de debug.
    """
    
    def authenticate(self, request):
        """Autentica o usuário com logs de debug."""
        logger.info(f"JWT Authentication attempt for {request.path}")
        
        # Log do header de autorização
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header:
            logger.info(f"Authorization header found: {auth_header[:50]}...")
        else:
            logger.warning("No Authorization header found")
        
        try:
            result = super().authenticate(request)
            if result:
                user, token = result
                logger.info(f"JWT Authentication successful for user: {user.email}")
                return result
            else:
                logger.warning("JWT Authentication failed - no result")
                return None
        except InvalidToken as e:
            logger.error(f"JWT Authentication failed - Invalid token: {str(e)}")
            return None
        except TokenError as e:
            logger.error(f"JWT Authentication failed - Token error: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"JWT Authentication failed - Unexpected error: {str(e)}")
            return None
