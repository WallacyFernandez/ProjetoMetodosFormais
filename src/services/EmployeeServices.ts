import { http } from "./httpClient";
import type {
  Employee,
  EmployeeCreate,
  EmployeeTerminate,
  EmployeePosition,
  Payroll,
  PayrollCreate,
  PayrollHistory,
  EmployeeSummary,
  PayrollSummary,
} from "@/types/employee";

class EmployeeServices {
  // ==================== CARGOS ====================

  /**
   * Listar todos os cargos
   */
  async getPositions(): Promise<EmployeePosition[]> {
    const response = await http.get<any>("/api/v1/employees/positions/");
    return response.results || response;
  }

  /**
   * Buscar um cargo específico
   */
  async getPosition(id: string): Promise<EmployeePosition> {
    return await http.get<EmployeePosition>(
      `/api/v1/employees/positions/${id}/`,
    );
  }

  /**
   * Criar um novo cargo
   */
  async createPosition(
    data: Omit<
      EmployeePosition,
      "id" | "created_at" | "updated_at" | "department_display"
    >,
  ): Promise<EmployeePosition> {
    return await http.post<EmployeePosition>(
      "/api/v1/employees/positions/",
      data,
    );
  }

  /**
   * Atualizar um cargo
   */
  async updatePosition(
    id: string,
    data: Partial<
      Omit<
        EmployeePosition,
        "id" | "created_at" | "updated_at" | "department_display"
      >
    >,
  ): Promise<EmployeePosition> {
    return await http.patch<EmployeePosition>(
      `/api/v1/employees/positions/${id}/`,
      data,
    );
  }

  /**
   * Deletar um cargo
   */
  async deletePosition(id: string): Promise<void> {
    await http.del(`/api/v1/employees/positions/${id}/`);
  }

  /**
   * Criar cargos padrão
   */
  async createDefaultPositions(): Promise<{
    message: string;
    positions: EmployeePosition[];
  }> {
    return await http.post<{ message: string; positions: EmployeePosition[] }>(
      "/api/v1/employees/positions/create_default_positions/",
    );
  }

  // ==================== FUNCIONÁRIOS ====================

  /**
   * Listar todos os funcionários
   */
  async getEmployees(): Promise<Employee[]> {
    const response = await http.get<any>("/api/v1/employees/employees/");
    return response.results || response;
  }

  /**
   * Buscar um funcionário específico
   */
  async getEmployee(id: string): Promise<Employee> {
    return await http.get<Employee>(`/api/v1/employees/employees/${id}/`);
  }

  /**
   * Criar um novo funcionário
   */
  async createEmployee(data: EmployeeCreate): Promise<Employee> {
    return await http.post<Employee>("/api/v1/employees/employees/", data);
  }

  /**
   * Atualizar um funcionário
   */
  async updateEmployee(
    id: string,
    data: Partial<EmployeeCreate>,
  ): Promise<Employee> {
    return await http.patch<Employee>(
      `/api/v1/employees/employees/${id}/`,
      data,
    );
  }

  /**
   * Deletar um funcionário
   */
  async deleteEmployee(id: string): Promise<void> {
    await http.del(`/api/v1/employees/employees/${id}/`);
  }

  /**
   * Demitir um funcionário
   */
  async terminateEmployee(
    id: string,
    data?: EmployeeTerminate,
  ): Promise<{ message: string; employee: Employee }> {
    return await http.post<{ message: string; employee: Employee }>(
      `/api/v1/employees/employees/${id}/terminate/`,
      data,
    );
  }

  /**
   * Reativar um funcionário
   */
  async reactivateEmployee(
    id: string,
  ): Promise<{ message: string; employee: Employee }> {
    return await http.post<{ message: string; employee: Employee }>(
      `/api/v1/employees/employees/${id}/reactivate/`,
    );
  }

  /**
   * Obter resumo dos funcionários
   */
  async getEmployeesSummary(): Promise<EmployeeSummary> {
    return await http.get<EmployeeSummary>(
      "/api/v1/employees/employees/summary/",
    );
  }

  // ==================== FOLHA DE PAGAMENTO ====================

  /**
   * Listar todas as folhas de pagamento
   */
  async getPayrolls(): Promise<Payroll[]> {
    const response = await http.get<any>("/api/v1/employees/payrolls/");
    return response.results || response;
  }

  /**
   * Buscar uma folha de pagamento específica
   */
  async getPayroll(id: string): Promise<Payroll> {
    return await http.get<Payroll>(`/api/v1/employees/payrolls/${id}/`);
  }

  /**
   * Criar uma nova folha de pagamento
   */
  async createPayroll(data: PayrollCreate): Promise<Payroll> {
    return await http.post<Payroll>("/api/v1/employees/payrolls/", data);
  }

  /**
   * Atualizar uma folha de pagamento
   */
  async updatePayroll(
    id: string,
    data: Partial<PayrollCreate>,
  ): Promise<Payroll> {
    return await http.patch<Payroll>(`/api/v1/employees/payrolls/${id}/`, data);
  }

  /**
   * Deletar uma folha de pagamento
   */
  async deletePayroll(id: string): Promise<void> {
    await http.del(`/api/v1/employees/payrolls/${id}/`);
  }


  /**
   * Obter folhas de pagamento por mês
   */
  async getPayrollsByMonth(month: string): Promise<PayrollSummary> {
    return await http.get<PayrollSummary>(
      `/api/v1/employees/payrolls/by_month/?month=${month}`,
    );
  }

  /**
   * Marcar folha como paga
   */
  async markPayrollAsPaid(
    id: string,
  ): Promise<{ message: string; payroll: Payroll }> {
    return await http.post<{ message: string; payroll: Payroll }>(
      `/api/v1/employees/payrolls/${id}/mark_as_paid/`,
    );
  }

  // ==================== HISTÓRICO DE PAGAMENTOS ====================

  /**
   * Listar histórico de pagamentos
   */
  async getPayrollHistory(): Promise<PayrollHistory[]> {
    const response = await http.get<any>("/api/v1/employees/payroll-history/");
    return response.results || response;
  }

  /**
   * Buscar um histórico específico
   */
  async getPayrollHistoryItem(id: string): Promise<PayrollHistory> {
    return await http.get<PayrollHistory>(
      `/api/v1/employees/payroll-history/${id}/`,
    );
  }
}

export default new EmployeeServices();
