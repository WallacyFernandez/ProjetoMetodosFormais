"""
Utilitários compartilhados do projeto.
"""

import os
import uuid
from datetime import datetime
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.text import slugify
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


def generate_unique_filename(instance, filename):
    """
    Gera um nome único para arquivos uploadados.
    """
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('uploads', filename)


def validate_file_extension(value, allowed_extensions):
    """
    Valida a extensão de um arquivo.
    """
    ext = os.path.splitext(value.name)[1]
    if ext.lower() not in allowed_extensions:
        raise ValidationError(
            f'Extensão de arquivo não permitida. Extensões permitidas: {", ".join(allowed_extensions)}'
        )


def validate_file_size(value, max_size_mb=5):
    """
    Valida o tamanho de um arquivo.
    """
    max_size = max_size_mb * 1024 * 1024  # Convert MB to bytes
    if value.size > max_size:
        raise ValidationError(f'Arquivo muito grande. Tamanho máximo: {max_size_mb}MB')


def create_slug(text, max_length=50):
    """
    Cria um slug a partir de um texto.
    """
    return slugify(text)[:max_length]


def format_cpf(cpf):
    """
    Formata um CPF para exibição.
    """
    if len(cpf) == 11:
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    return cpf


def format_cnpj(cnpj):
    """
    Formata um CNPJ para exibição.
    """
    if len(cnpj) == 14:
        return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
    return cnpj


def format_phone(phone):
    """
    Formata um telefone para exibição.
    """
    phone = ''.join(filter(str.isdigit, phone))
    if len(phone) == 11:
        return f"({phone[:2]}) {phone[2:7]}-{phone[7:]}"
    elif len(phone) == 10:
        return f"({phone[:2]}) {phone[2:6]}-{phone[6:]}"
    return phone


def validate_email_address(email):
    """
    Valida um endereço de email.
    """
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def success_response(data=None, message='Operação realizada com sucesso', status_code=status.HTTP_200_OK):
    """
    Cria uma resposta de sucesso padronizada.
    """
    response_data = {
        'success': True,
        'message': message,
        'timestamp': datetime.now().isoformat()
    }
    if data is not None:
        response_data['data'] = data
    
    return Response(response_data, status=status_code)


def error_response(message='Erro interno do servidor', errors=None, status_code=status.HTTP_400_BAD_REQUEST):
    """
    Cria uma resposta de erro padronizada.
    """
    response_data = {
        'success': False,
        'message': message,
        'timestamp': datetime.now().isoformat()
    }
    if errors:
        response_data['errors'] = errors
    
    logger.error(f"Error response: {message}, Status: {status_code}")
    return Response(response_data, status=status_code)


def paginated_response(queryset, serializer_class, request, message='Dados carregados com sucesso'):
    """
    Cria uma resposta paginada padronizada.
    """
    from rest_framework.pagination import PageNumberPagination
    
    paginator = PageNumberPagination()
    paginator.page_size = 20
    paginated_queryset = paginator.paginate_queryset(queryset, request)
    
    serializer = serializer_class(paginated_queryset, many=True, context={'request': request})
    
    return Response({
        'success': True,
        'message': message,
        'count': paginator.page.paginator.count,
        'next': paginator.get_next_link(),
        'previous': paginator.get_previous_link(),
        'results': serializer.data,
        'timestamp': datetime.now().isoformat()
    })


class APIException(Exception):
    """
    Exceção customizada para a API.
    """
    def __init__(self, message, status_code=status.HTTP_400_BAD_REQUEST, errors=None):
        self.message = message
        self.status_code = status_code
        self.errors = errors
        super().__init__(message)


def handle_api_exception(func):
    """
    Decorator para tratar exceções da API.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except APIException as e:
            return error_response(e.message, e.errors, e.status_code)
        except Exception as e:
            logger.exception(f"Unexpected error in {func.__name__}: {str(e)}")
            return error_response('Erro interno do servidor', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return wrapper
