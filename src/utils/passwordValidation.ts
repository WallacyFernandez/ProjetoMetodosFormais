/**
 * Utilitários para validação de senha forte no frontend.
 */

export interface PasswordValidationResult {
  isValid: boolean;
  errors: string[];
  strength: "weak" | "medium" | "strong";
}

/**
 * Valida se a senha atende aos critérios de senha forte.
 */
export function validateStrongPassword(
  password: string,
): PasswordValidationResult {
  const errors: string[] = [];

  // Verifica comprimento mínimo
  if (password.length < 8) {
    errors.push("A senha deve ter pelo menos 8 caracteres");
  }

  // Verifica se tem letra maiúscula
  if (!/[A-Z]/.test(password)) {
    errors.push("A senha deve conter pelo menos uma letra maiúscula");
  }

  // Verifica se tem letra minúscula
  if (!/[a-z]/.test(password)) {
    errors.push("A senha deve conter pelo menos uma letra minúscula");
  }

  // Verifica se tem número
  if (!/\d/.test(password)) {
    errors.push("A senha deve conter pelo menos um número");
  }

  // Verifica se tem caractere especial
  if (!/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password)) {
    errors.push(
      "A senha deve conter pelo menos um caractere especial (!@#$%^&*()_+-=[]{}|;:,.<>/?)",
    );
  }

  // Verifica sequências repetidas simples
  if (hasSimpleRepetition(password)) {
    errors.push(
      "A senha não pode conter sequências repetidas simples (ex: aaa, 111, rurururru)",
    );
  }

  // Verifica sequências comuns do teclado
  if (hasKeyboardSequence(password)) {
    errors.push(
      "A senha não pode conter sequências comuns do teclado (ex: qwerty, asdf)",
    );
  }

  // Calcula força da senha
  const strength = calculatePasswordStrength(password, errors.length);

  return {
    isValid: errors.length === 0,
    errors,
    strength,
  };
}

/**
 * Verifica se a senha contém sequências repetidas simples.
 */
function hasSimpleRepetition(password: string): boolean {
  const passwordLower = password.toLowerCase();

  // Verifica repetição de caracteres (ex: aaa, 111)
  if (/(.)\1{2,}/.test(passwordLower)) {
    return true;
  }

  // Verifica padrões repetitivos simples (ex: rurururru, abcabc)
  for (let i = 2; i <= passwordLower.length / 2; i++) {
    const pattern = passwordLower.substring(0, i);
    const count = (passwordLower.match(new RegExp(pattern, "g")) || []).length;

    if (count >= 2) {
      // Verifica se o padrão se repete consecutivamente
      if (passwordLower.includes(pattern + pattern)) {
        return true;
      }
    }
  }

  return false;
}

/**
 * Verifica se a senha contém sequências comuns do teclado.
 */
function hasKeyboardSequence(password: string): boolean {
  const keyboardSequences = [
    "qwerty",
    "asdf",
    "zxcv",
    "1234",
    "abcd",
    "qwer",
    "hjkl",
    "uiop",
    "qaz",
    "wsx",
    "edc",
    "rfv",
    "tgb",
    "yhn",
    "ujm",
  ];

  const passwordLower = password.toLowerCase();

  for (const sequence of keyboardSequences) {
    if (
      passwordLower.includes(sequence) ||
      passwordLower.includes(sequence.split("").reverse().join(""))
    ) {
      return true;
    }
  }

  return false;
}

/**
 * Calcula a força da senha baseado nos critérios atendidos.
 */
function calculatePasswordStrength(
  password: string,
  errorCount: number,
): "weak" | "medium" | "strong" {
  if (errorCount > 0) {
    return "weak";
  }

  let score = 0;

  // Comprimento
  if (password.length >= 12) score += 2;
  else if (password.length >= 8) score += 1;

  // Variedade de caracteres
  const hasUpper = /[A-Z]/.test(password);
  const hasLower = /[a-z]/.test(password);
  const hasNumber = /\d/.test(password);
  const hasSpecial = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password);

  const varietyCount = [hasUpper, hasLower, hasNumber, hasSpecial].filter(
    Boolean,
  ).length;
  score += varietyCount;

  if (score >= 6) return "strong";
  if (score >= 4) return "medium";
  return "weak";
}

/**
 * Retorna mensagem de ajuda sobre os requisitos da senha.
 */
export function getPasswordRequirements(): string[] {
  return [
    "Mínimo de 8 caracteres",
    "Pelo menos uma letra maiúscula",
    "Pelo menos uma letra minúscula",
    "Pelo menos um número",
    "Pelo menos um caractere especial (!@#$%^&*()_+-=[]{}|;:,.<>/?)",
    "Não pode conter sequências repetidas simples",
    "Não pode conter sequências comuns do teclado",
  ];
}
