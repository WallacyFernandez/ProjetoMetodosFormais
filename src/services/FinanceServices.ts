import { http } from "@/services/httpClient";
import type {
  UserBalance,
  BalanceHistory,
  Category,
  Transaction,
  DashboardData,
  MonthlySummary,
  CategorySummary,
  BalanceOperation,
  BalanceSet,
  TransactionCreate,
  CategoryCreate,
  TransactionFilters,
  MonthlyReport,
} from "@/types/finance";

// Serviços para Saldo
export async function GetUserBalance(): Promise<UserBalance> {
  const response = await http.get<UserBalance>("/api/v1/finance/balance/", {
    context: "Carregar saldo do usuário",
  });
  return response;
}

export async function AddToBalance(
  operation: BalanceOperation,
): Promise<UserBalance> {
  const response = await http.post<UserBalance>(
    "/api/v1/finance/balance/add_amount/",
    operation,
    { context: "Adicionar ao saldo" },
  );
  return response;
}

export async function SubtractFromBalance(
  operation: BalanceOperation,
): Promise<UserBalance> {
  const response = await http.post<UserBalance>(
    "/api/v1/finance/balance/subtract_amount/",
    operation,
    { context: "Subtrair do saldo" },
  );
  return response;
}

export async function SetBalance(operation: BalanceSet): Promise<UserBalance> {
  const response = await http.post<UserBalance>(
    "/api/v1/finance/balance/set_balance/",
    operation,
    { context: "Definir saldo" },
  );
  return response;
}

export async function ResetBalance(): Promise<UserBalance> {
  const response = await http.post<UserBalance>(
    "/api/v1/finance/balance/reset_balance/",
    {},
    { context: "Resetar saldo" },
  );
  return response;
}

export async function GetBalanceHistory(): Promise<BalanceHistory[]> {
  const response = await http.get<BalanceHistory[]>(
    "/api/v1/finance/balance/history/",
    {
      context: "Carregar histórico de saldo",
    },
  );
  return response;
}

// Serviços para Categorias
export async function GetCategories(): Promise<Category[]> {
  const response = await http.get<any>("/api/v1/finance/categories/", {
    context: "Carregar categorias",
  });

  console.log("GetCategories response:", {
    response,
    type: typeof response,
    isArray: Array.isArray(response),
    hasResults:
      response && typeof response === "object" && "results" in response,
  });

  // Extrair categorias da estrutura de paginação ou array direto
  let categories: Category[] = [];

  if (response && typeof response === "object" && "results" in response) {
    console.log("Extracting categories from pagination structure");
    categories = response.results || [];
  } else if (Array.isArray(response)) {
    console.log("Using direct array response");
    categories = response;
  } else {
    console.warn("Unexpected response structure:", response);
    categories = [];
  }

  console.log(`Extracted ${categories.length} categories`);
  return categories;
}

export async function GetDefaultCategories(): Promise<Category[]> {
  const response = await http.get<Category[]>(
    "/api/v1/finance/categories/defaults/",
    {
      context: "Carregar categorias padrão",
    },
  );
  return response;
}

export async function GetCustomCategories(): Promise<Category[]> {
  const response = await http.get<Category[]>(
    "/api/v1/finance/categories/custom/",
    {
      context: "Carregar categorias personalizadas",
    },
  );
  return response;
}

export async function CreateCategory(
  category: CategoryCreate,
): Promise<Category> {
  const response = await http.post<Category>(
    "/api/v1/finance/categories/",
    category,
    {
      context: "Criar categoria",
    },
  );
  return response;
}

export async function UpdateCategory(
  id: string,
  category: Partial<CategoryCreate>,
): Promise<Category> {
  const response = await http.put<{ success: boolean; data: Category }>(
    `/api/v1/finance/categories/${id}/`,
    category,
    {
      context: "Atualizar categoria",
    },
  );
  return response.data;
}

export async function DeleteCategory(id: string): Promise<void> {
  await http.del(`/api/v1/finance/categories/${id}/`, {
    context: "Deletar categoria",
  });
}

// Serviços para Transações
export async function GetTransactions(
  filters?: TransactionFilters,
): Promise<Transaction[]> {
  const query = filters
    ? {
        transaction_type: filters.transaction_type,
        category: filters.category,
        year: filters.year,
        month: filters.month,
        date_from: filters.date_from,
        date_to: filters.date_to,
        amount_min: filters.amount_min,
        amount_max: filters.amount_max,
        is_recurring: filters.is_recurring,
      }
    : {};

  const response = await http.get<any>(
    "/api/v1/finance/transactions/",
    {
      query,
      context: "Carregar transações",
    },
  );


  let transactions: Transaction[] = [];
  
  if (response && typeof response === "object" && "results" in response) {
    transactions = response.results || [];
    console.log("Using paginated results:", transactions.length);
  } else if (Array.isArray(response)) {
    transactions = response;
    console.log("Using direct array:", transactions.length);
  } else {
    console.warn("Unexpected response structure:", response);
    transactions = [];
  }

  console.log("Final transactions:", transactions);
  return transactions;
}

export async function GetTransaction(id: string): Promise<Transaction> {
  const response = await http.get<Transaction>(
    `/api/v1/finance/transactions/${id}/`,
    {
      context: "Carregar transação",
    },
  );
  return response;
}

export async function CreateTransaction(
  transaction: TransactionCreate,
): Promise<Transaction> {
  const response = await http.post<Transaction>(
    "/api/v1/finance/transactions/",
    transaction,
    {
      context: "Criar transação",
    },
  );
  return response;
}

export async function UpdateTransaction(
  id: string,
  transaction: Partial<TransactionCreate>,
): Promise<Transaction> {
  const response = await http.put<Transaction>(
    `/api/v1/finance/transactions/${id}/`,
    transaction,
    {
      context: "Atualizar transação",
    },
  );
  return response;
}

export async function DeleteTransaction(id: string): Promise<void> {
  await http.del(`/api/v1/finance/transactions/${id}/`, {
    context: "Deletar transação",
  });
}

export async function GetRecentTransactions(
  limit: number = 10,
): Promise<Transaction[]> {
  const response = await http.get<Transaction[]>(
    `/api/v1/finance/transactions/recent/?limit=${limit}`,
    {
      context: "Carregar transações recentes",
    },
  );
  return response;
}

// Serviços para Relatórios
export async function GetMonthlySummary(
  report: MonthlyReport,
): Promise<MonthlySummary> {
  const response = await http.get<MonthlySummary>(
    `/api/v1/finance/transactions/monthly_summary/?year=${report.year}&month=${report.month}`,
    {
      context: "Carregar resumo mensal",
    },
  );
  return response;
}

export async function GetCategorySummary(
  report: MonthlyReport,
): Promise<CategorySummary[]> {
  const response = await http.get<CategorySummary[]>(
    `/api/v1/finance/transactions/category_summary/?year=${report.year}&month=${report.month}`,
    {
      context: "Carregar resumo por categoria",
    },
  );
  return response;
}

// Serviço para Dashboard completo
export async function GetDashboardData(): Promise<DashboardData> {
  console.log("[FinanceServices] Iniciando requisição para dashboard_data");
  const response = await http.get<DashboardData>(
    "/api/v1/finance/transactions/dashboard_data/",
    {
      context: "Carregar dados do dashboard",
    },
  );
  console.log("[FinanceServices] Resposta recebida:", response);
  console.log("[FinanceServices] Dados extraídos:", response);
  return response;
}
