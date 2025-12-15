"""
Validadores customizados para o sistema.
"""

import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class StrongPasswordValidator:
    """
    Validador de senha forte que exige:
    - Mínimo 8 caracteres
    - Pelo menos uma letra maiúscula
    - Pelo menos uma letra minúscula
    - Pelo menos um número
    - Pelo menos um caractere especial
    - Não pode conter sequências repetidas simples (ex: aaa, 111, rurururru)
    """

    def validate(self, password, user=None):
        errors = []
        
        # Verifica comprimento mínimo
        if len(password) < 8:
            errors.append(
                ValidationError(
                    _("A senha deve ter pelo menos 8 caracteres."),
                    code="password_too_short",
                )
            )
        
        # Verifica se tem letra maiúscula
        if not re.search(r"[A-Z]", password):
            errors.append(
                ValidationError(
                    _("A senha deve conter pelo menos uma letra maiúscula."),
                    code="password_no_upper",
                )
            )
        
        # Verifica se tem letra minúscula
        if not re.search(r"[a-z]", password):
            errors.append(
                ValidationError(
                    _("A senha deve conter pelo menos uma letra minúscula."),
                    code="password_no_lower",
                )
            )
        
        # Verifica se tem número
        if not re.search(r"\d", password):
            errors.append(
                ValidationError(
                    _("A senha deve conter pelo menos um número."),
                    code="password_no_digit",
                )
            )
        
        # Verifica se tem caractere especial
        if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]", password):
            errors.append(
                ValidationError(
                    _("A senha deve conter pelo menos um caractere especial (!@#$%^&*()_+-=[]{}|;:,.<>/?)."),
                    code="password_no_special",
                )
            )
        
        # Verifica sequências repetidas simples (ex: aaa, 111, rurururru)
        if self._has_simple_repetition(password):
            errors.append(
                ValidationError(
                    _("A senha não pode conter sequências repetidas simples (ex: aaa, 111, rurururru)."),
                    code="password_simple_repetition",
                )
            )
        
        # Verifica sequências comuns do teclado (ex: qwerty, asdf)
        if self._has_keyboard_sequence(password):
            errors.append(
                ValidationError(
                    _("A senha não pode conter sequências comuns do teclado (ex: qwerty, asdf)."),
                    code="password_keyboard_sequence",
                )
            )
        
        if errors:
            raise ValidationError(errors)
    
    def get_help_text(self):
        return _(
            "Sua senha deve conter:\n"
            "- Mínimo de 8 caracteres\n"
            "- Pelo menos uma letra maiúscula\n"
            "- Pelo menos uma letra minúscula\n"
            "- Pelo menos um número\n"
            "- Pelo menos um caractere especial (!@#$%^&*()_+-=[]{}|;:,.<>/?)\n"
            "- Não pode conter sequências repetidas simples\n"
            "- Não pode conter sequências comuns do teclado"
        )
    
    def _has_simple_repetition(self, password):
        """
        Verifica se a senha contém sequências repetidas simples.
        Exemplos: aaa, 111, rurururru, abcabc
        """
        # Verifica repetição de caracteres (ex: aaa, 111)
        if re.search(r"(.)\1{2,}", password.lower()):
            return True
        
        # Verifica padrões repetitivos simples (ex: rurururru, abcabc)
        for i in range(2, len(password) // 2 + 1):
            pattern = password.lower()[:i]
            if password.lower().count(pattern) >= 2:
                # Verifica se o padrão se repete consecutivamente
                if pattern * 2 in password.lower():
                    return True
        
        return False
    
    def _has_keyboard_sequence(self, password):
        """
        Verifica se a senha contém sequências comuns do teclado.
        """
        keyboard_sequences = [
            "qwerty", "asdf", "zxcv", "1234", "abcd",
            "qwer", "asdf", "zxcv", "hjkl", "uiop",
            "qaz", "wsx", "edc", "rfv", "tgb",
            "yhn", "ujm", "ik", "ol", "p",
        ]
        
        password_lower = password.lower()
        for sequence in keyboard_sequences:
            if sequence in password_lower or sequence[::-1] in password_lower:
                return True
        
        return False
