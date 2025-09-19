import { toast } from "react-toastify";
import type { HttpError } from "@/services/httpClient";

function resolveMessage(error: HttpError): string {
  const status = error.status;

  if (status === 0) return "Falha de rede. Verifique sua conexão.";
  if (status === 401) return "Não autorizado. Faça login novamente.";
  if (status === 403) return "Acesso negado.";
  if (status === 404) return "Recurso não encontrado.";
  if (status === 422) return "Dados inválidos. Verifique os campos informados.";
  if (status && status >= 500) return "Erro no servidor. Tente novamente mais tarde.";

  return error.message || "Ocorreu um erro ao processar sua solicitação.";
}

export function showHttpErrorToast(error: HttpError, context?: string) {
  const baseMessage = resolveMessage(error);
  const message = context ? `${context}: ${baseMessage}` : baseMessage;
  toast.error(message);
}

