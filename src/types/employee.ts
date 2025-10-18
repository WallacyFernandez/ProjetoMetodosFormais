/**
 * Tipos relacionados a funcionários
 */

export type DepartmentType =
  | "VENDAS"
  | "ESTOQUE"
  | "CAIXA"
  | "GERENCIA"
  | "LIMPEZA"
  | "SEGURANCA"
  | "RH";

export type EmploymentStatus =
  | "ACTIVE"
  | "INACTIVE"
  | "ON_LEAVE"
  | "TERMINATED";

export type PaymentStatus = "PENDING" | "PAID" | "CANCELLED";

export interface EmployeePosition {
  id: string;
  name: string;
  description?: string;
  base_salary: number;
  min_salary: number;
  max_salary: number;
  department: DepartmentType;
  department_display: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Employee {
  id: string;
  name: string;
  cpf: string;
  email?: string;
  phone?: string;
  position: string;
  position_name: string;
  position_department: DepartmentType;
  salary: number;
  salary_formatted: string;
  hire_date: string;
  employment_status: EmploymentStatus;
  employment_status_display: string;
  is_active: boolean;
  termination_date?: string;
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface EmployeeCreate {
  name: string;
  cpf: string;
  email?: string;
  phone?: string;
  position: string;
  salary: number;
  hire_date?: string;
  notes?: string;
}

export interface EmployeeTerminate {
  termination_date?: string;
  notes?: string;
}

export interface Payroll {
  id: string;
  employee: string;
  employee_name: string;
  employee_position: string;
  payment_month: string;
  base_salary: number;
  overtime_hours: number;
  overtime_value: number;
  bonus: number;
  deductions: number;
  total_amount: number;
  total_formatted: string;
  payment_date?: string;
  payment_status: PaymentStatus;
  payment_status_display: string;
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface PayrollCreate {
  employee: string;
  payment_month: string;
  base_salary: number;
  overtime_hours?: number;
  overtime_value?: number;
  bonus?: number;
  deductions?: number;
  notes?: string;
}


export interface PayrollHistory {
  id: string;
  payment_month: string;
  payment_month_display: string;
  total_employees: number;
  total_amount: number;
  total_amount_formatted: string;
  processed_at: string;
}

export interface EmployeeSummary {
  total_employees: number;
  active_employees: number;
  inactive_employees: number;
  total_monthly_payroll: number;
  total_monthly_payroll_formatted: string;
  employees_by_department: Record<string, number>;
  employees_by_position: Record<string, number>;
}

export interface PayrollSummary {
  month: string;
  total_employees: number;
  total_amount: number;
  total_amount_formatted: string;
  average_salary: number;
  average_salary_formatted: string;
  payrolls: Payroll[];
}

