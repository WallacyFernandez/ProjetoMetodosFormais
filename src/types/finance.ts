// Tipos para o sistema financeiro baseados nos modelos do backend

export interface UserBalance {
  id: string;
  current_balance: number;
  balance_formatted: string;
  user_name: string;
  last_updated: string;
  created_at: string;
  updated_at: string;
}

export interface BalanceHistory {
  id: string;
  operation: 'ADD' | 'SUBTRACT' | 'SET' | 'RESET';
  operation_display: string;
  amount: number;
  previous_balance: number;
  new_balance: number;
  description: string;
  user_name: string;
  created_at: string;
}

export interface Category {
  id: string;
  name: string;
  description: string;
  icon: string;
  color: string;
  category_type: 'INCOME' | 'EXPENSE' | 'BOTH';
  is_default: boolean;
  created_at: string;
  updated_at: string;
}

export interface Transaction {
  id: string;
  amount: number;
  amount_formatted: string;
  transaction_type: 'INCOME' | 'EXPENSE';
  category: string; // ID da categoria
  category_name: string;
  category_icon: string;
  category_color: string;
  subcategory: string;
  description: string;
  transaction_date: string;
  receipt?: string;
  is_recurring: boolean;
  recurrence_type: 'NONE' | 'DAILY' | 'WEEKLY' | 'MONTHLY' | 'YEARLY';
  recurrence_end_date?: string;
  parent_transaction?: string;
  created_at: string;
  updated_at: string;
}

export interface MonthlySummary {
  year: number;
  month: number;
  income_total: number;
  expense_total: number;
  balance: number;
  transaction_count: number;
  income_total_formatted: string;
  expense_total_formatted: string;
  balance_formatted: string;
}

export interface CategorySummary {
  category__name: string;
  category__icon: string;
  category__color: string;
  transaction_type: 'INCOME' | 'EXPENSE';
  total: number;
  count: number;
  total_formatted: string;
  percentage: number;
}

export interface DashboardData {
  current_balance: number;
  current_balance_formatted: string;
  monthly_summary: MonthlySummary;
  category_summary: CategorySummary[];
  recent_transactions: Transaction[];
  total_transactions_count: number;
  avg_monthly_income: number;
  avg_monthly_expense: number;
}

// Tipos para operações de saldo
export interface BalanceOperation {
  amount: number;
  description?: string;
}

export interface BalanceSet {
  amount: number;
  description?: string;
}

// Tipos para criação/edição de transações
export interface TransactionCreate {
  amount: number;
  transaction_type: 'INCOME' | 'EXPENSE';
  category: string;
  subcategory?: string;
  description: string;
  transaction_date: string;
  receipt?: File;
  is_recurring?: boolean;
  recurrence_type?: 'NONE' | 'DAILY' | 'WEEKLY' | 'MONTHLY' | 'YEARLY';
  recurrence_end_date?: string;
}

// Tipos para criação/edição de categorias
export interface CategoryCreate {
  name: string;
  description?: string;
  icon: string;
  color: string;
  category_type: 'INCOME' | 'EXPENSE' | 'BOTH';
}

// Tipos para filtros de transações
export interface TransactionFilters {
  transaction_type?: 'INCOME' | 'EXPENSE';
  category?: string;
  year?: number;
  month?: number;
  date_from?: string;
  date_to?: string;
  amount_min?: number;
  amount_max?: number;
  is_recurring?: boolean;
}

// Tipos para relatórios
export interface MonthlyReport {
  year: number;
  month: number;
}
