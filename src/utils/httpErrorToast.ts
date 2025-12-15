import { toast } from "react-toastify";
import type { HttpError } from "@/services/httpClient";

function resolveMessage(error: HttpError): string {
  const status = error.status;

  if (status === 0) return "Falha de rede. Verifique sua conexão.";
  if (status === 401) return "Não autorizado. Faça login novamente.";
  if (status === 403) return "Acesso negado.";
  if (status === 404) return "Recurso não encontrado.";
  if (status === 422) return "Dados inválidos. Verifique os campos informados.";
  if (status && status >= 500)
    return "Erro no servidor. Tente novamente mais tarde.";

  return error.message || "Ocorreu um erro ao processar sua solicitação.";
}

export function showHttpErrorToast(error: HttpError, context?: string) {
  const baseMessage = resolveMessage(error);
  const message = context ? `${context}: ${baseMessage}` : baseMessage;
  toast.error(message);
}

/**
 * Campos que não devem ser tratados como erros de formulário
 */
const NON_FORM_FIELDS = [
  "success",
  "message",
  "errors",
  "timestamp",
  "error_code",
  "detail",
  "non_field_errors",
];

/**
 * Extrai mensagens de erro específicas do backend.
 * O backend retorna erros no formato:
 * {
 *   "success": false,
 *   "message": "Dados inválidos",
 *   "errors": {
 *     "password": ["Este campo é obrigatório."],
 *     "email": ["Este email já está em uso."]
 *   }
 * }
 */
export function extractFieldErrors(error: HttpError): Record<string, string[]> {
  const errors: Record<string, string[]> = {};

  if (error.body && typeof error.body === "object") {
    const body = error.body as any;

    // Verifica se há erros no formato do Django REST Framework
    if (body.errors && typeof body.errors === "object") {
      Object.keys(body.errors).forEach((field) => {
        // Ignora campos que não são do formulário
        if (NON_FORM_FIELDS.includes(field.toLowerCase())) {
          return;
        }

        const fieldErrors = body.errors[field];
        if (Array.isArray(fieldErrors)) {
          errors[field] = fieldErrors;
        } else if (typeof fieldErrors === "string") {
          errors[field] = [fieldErrors];
        } else if (Array.isArray(fieldErrors) && fieldErrors.length > 0) {
          // Caso seja um array de objetos com mensagens
          errors[field] = fieldErrors.map((err: any) =>
            typeof err === "string" ? err : err.message || JSON.stringify(err),
          );
        }
      });
    }

    // Também verifica erros diretos nos campos (formato alternativo)
    Object.keys(body).forEach((key) => {
      // Ignora campos que não são do formulário
      if (NON_FORM_FIELDS.includes(key.toLowerCase())) {
        return;
      }

      const value = body[key];
      if (Array.isArray(value)) {
        errors[key] = value;
      } else if (typeof value === "string") {
        errors[key] = [value];
      }
    });
  }

  return errors;
}

/**
 * Retorna a primeira mensagem de erro de um campo específico.
 */
export function getFieldError(
  error: HttpError,
  fieldName: string,
): string | null {
  const fieldErrors = extractFieldErrors(error);
  const errors = fieldErrors[fieldName];
  return errors && errors.length > 0 ? errors[0] : null;
}

/**
 * Retorna todas as mensagens de erro formatadas em uma string.
 * Útil para exibir múltiplos erros de validação.
 */
export function getAllErrorMessages(error: HttpError): string[] {
  const fieldErrors = extractFieldErrors(error);
  const messages: string[] = [];

  Object.keys(fieldErrors).forEach((field) => {
    const fieldName = getFieldDisplayName(field);
    fieldErrors[field].forEach((msg) => {
      messages.push(`${fieldName}: ${msg}`);
    });
  });

  return messages;
}

/**
 * Converte o nome do campo da API para um nome amigável em português.
 */
function getFieldDisplayName(field: string): string {
  const fieldMap: Record<string, string> = {
    password: "Senha",
    password_confirm: "Confirmação de senha",
    new_password: "Nova senha",
    new_password_confirm: "Confirmação da nova senha",
    old_password: "Senha atual",
    email: "Email",
    username: "Nome de usuário",
    first_name: "Nome",
    last_name: "Sobrenome",
    name: "Nome",
    cpf: "CPF",
    phone: "Telefone",
    position: "Cargo",
    salary: "Salário",
    hire_date: "Data de contratação",
    amount: "Valor",
    category: "Categoria",
    description: "Descrição",
    transaction_type: "Tipo de transação",
    transaction_date: "Data da transação",
    category_type: "Tipo de categoria",
    icon: "Ícone",
    color: "Cor",
    department: "Departamento",
    base_salary: "Salário base",
    min_salary: "Salário mínimo",
    max_salary: "Salário máximo",
  };

  return (
    fieldMap[field] ||
    field.replace(/_/g, " ").replace(/\b\w/g, (l) => l.toUpperCase())
  );
}

/**
 * Retorna uma mensagem de erro formatada para exibição ao usuário.
 * Prioriza mensagens específicas de campos sobre mensagens genéricas.
 */
export function getErrorMessage(
  error: HttpError,
  defaultMessage?: string,
): string {
  const fieldErrors = extractFieldErrors(error);
  const errorKeys = Object.keys(fieldErrors);

  // Se houver erros específicos de campos, retorna a primeira mensagem
  if (errorKeys.length > 0) {
    const firstField = errorKeys[0];
    const firstError = fieldErrors[firstField][0];
    const fieldName = getFieldDisplayName(firstField);
    return `${fieldName}: ${firstError}`;
  }

  // Se não houver erros específicos, tenta usar a mensagem do erro
  if (error.body && typeof error.body === "object") {
    const body = error.body as any;
    if (body.message && typeof body.message === "string") {
      return body.message;
    }
  }

  // Usa mensagem padrão ou genérica
  return defaultMessage || resolveMessage(error);
}
