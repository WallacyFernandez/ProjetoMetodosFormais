import { http } from "./httpClient";
import {
  GameSession,
  ProductCategory,
  GameDashboardData,
  Supplier,
  Product,
  ProductStockHistory,
  ProductStockOperation,
  ProductPurchase,
  SaleSimulation,
  SalesSummary,
  SalesChartData,
  DetailedAnalysis,
} from "@/types/game";
import { UserBalance } from "@/types/finance";

// Serviços para sessão de jogo
export async function getCurrentGameSession(): Promise<GameSession> {
  const response = await http.get<GameSession>(
    "/api/v1/game/sessions/current/",
  );
  return response;
}

export async function pauseGame(): Promise<GameSession> {
  const response = await http.post<GameSession>("/api/v1/game/sessions/pause/");
  return response;
}

export async function resumeGame(): Promise<GameSession> {
  const response = await http.post<GameSession>(
    "/api/v1/game/sessions/resume/",
  );
  return response;
}

export async function startGame(): Promise<GameSession> {
  const response = await http.post<GameSession>("/api/v1/game/sessions/start/");
  return response;
}

export async function resetGame(): Promise<GameSession> {
  const response = await http.post<GameSession>("/api/v1/game/sessions/reset/");
  return response;
}

export async function updateGameTime(): Promise<{
  game_session: GameSession;
  days_passed: number;
}> {
  const response = await http.post<{
    game_session: GameSession;
    days_passed: number;
  }>("/api/v1/game/sessions/update_time/");
  return response;
}

// Serviços para saldo (agora usa o sistema financeiro)
export async function getUserBalance(): Promise<UserBalance> {
  const response = await http.get<UserBalance>("/api/v1/finance/balance/");
  return response;
}

export async function addToBalance(
  amount: number,
  description: string,
): Promise<UserBalance> {
  const response = await http.post<UserBalance>(
    "/api/v1/finance/balance/add/",
    {
      amount,
      description,
    },
  );
  return response;
}

export async function subtractFromBalance(
  amount: number,
  description: string,
): Promise<UserBalance> {
  const response = await http.post<UserBalance>(
    "/api/v1/finance/balance/subtract/",
    {
      amount,
      description,
    },
  );
  return response;
}

// Serviços para categorias de produtos
export async function getProductCategories(): Promise<ProductCategory[]> {
  const response = await http.get<any>("/api/v1/game/categories/");
  return Array.isArray(response) ? response : response.results || [];
}

// Serviços para dashboard do jogo
export async function getGameDashboardData(): Promise<GameDashboardData> {
  const response = await http.get<GameDashboardData>(
    "/api/v1/game/dashboard/data/",
  );
  return response;
}

// Utilitários para o jogo
export function formatGameDate(dateString: string): string {
  // Trata a data como local para evitar problemas de timezone
  const [year, month, day] = dateString.split("-");
  const date = new Date(parseInt(year), parseInt(month) - 1, parseInt(day));
  return date.toLocaleDateString("pt-BR", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
  });
}

export function formatGameTime(dateString: string): string {
  const date = new Date(dateString);
  return date.toLocaleTimeString("pt-BR", {
    hour: "2-digit",
    minute: "2-digit",
  });
}

export function calculateGameProgress(
  currentDate: string,
  startDate: string,
  endDate: string,
): number {
  const current = new Date(currentDate);
  const start = new Date(startDate);
  const end = new Date(endDate);

  const totalDays = (end.getTime() - start.getTime()) / (1000 * 60 * 60 * 24);
  const passedDays =
    (current.getTime() - start.getTime()) / (1000 * 60 * 60 * 24);

  return Math.min(100, Math.max(0, (passedDays / totalDays) * 100));
}

export function getGameStatusColor(status: string): string {
  switch (status) {
    case "NOT_STARTED":
      return "#6B7280"; // Cinza
    case "ACTIVE":
      return "#10B981"; // Verde
    case "PAUSED":
      return "#F59E0B"; // Amarelo
    case "COMPLETED":
      return "#3B82F6"; // Azul
    case "FAILED":
      return "#EF4444"; // Vermelho
    default:
      return "#6B7280"; // Cinza
  }
}

export function getGameStatusText(status: string): string {
  switch (status) {
    case "NOT_STARTED":
      return "Não Iniciado";
    case "ACTIVE":
      return "Ativo";
    case "PAUSED":
      return "Pausado";
    case "COMPLETED":
      return "Completado";
    case "FAILED":
      return "Falhou";
    default:
      return "Desconhecido";
  }
}

export function getOperationIcon(operation: string): string {
  switch (operation) {
    case "ADD":
    case "SALE":
      return "↗️";
    case "SUBTRACT":
    case "PURCHASE":
    case "SALARY":
    case "RENT":
    case "UTILITY":
      return "↘️";
    case "SET":
      return "⚡";
    case "RESET":
      return "🔄";
    default:
      return "💰";
  }
}

export function getOperationColor(operation: string): string {
  switch (operation) {
    case "ADD":
    case "SALE":
      return "#10B981"; // Verde
    case "SUBTRACT":
    case "PURCHASE":
    case "SALARY":
    case "RENT":
    case "UTILITY":
      return "#EF4444"; // Vermelho
    case "SET":
      return "#3B82F6"; // Azul
    case "RESET":
      return "#8B5CF6"; // Roxo
    default:
      return "#6B7280"; // Cinza
  }
}

// Serviços para fornecedores
export async function getSuppliers(): Promise<Supplier[]> {
  const response = await http.get<Supplier[] | { results: Supplier[] }>(
    "/api/v1/game/suppliers/",
  );
  return Array.isArray(response) ? response : response.results || [];
}

// Serviços para produtos
export async function getProducts(): Promise<Product[]> {
  const response = await http.get<Product[] | { results: Product[] }>(
    "/api/v1/game/products/",
  );
  return Array.isArray(response) ? response : response.results || [];
}

export async function getProductsByCategory(
  categoryId: string,
): Promise<Product[]> {
  const response = await http.get<Product[] | { results: Product[] }>(
    `/api/v1/game/products/?category=${categoryId}`,
  );
  return Array.isArray(response) ? response : response.results || [];
}

export async function getLowStockProducts(): Promise<Product[]> {
  const response = await http.get<Product[] | { results: Product[] }>(
    "/api/v1/game/products/low_stock/",
  );
  return Array.isArray(response) ? response : response.results || [];
}

export async function getOutOfStockProducts(): Promise<Product[]> {
  const response = await http.get<Product[] | { results: Product[] }>(
    "/api/v1/game/products/out_of_stock/",
  );
  return Array.isArray(response) ? response : response.results || [];
}

export async function purchaseProduct(
  productId: string,
  purchaseData: ProductPurchase,
): Promise<any> {
  const response = await http.post(
    `/api/v1/game/products/${productId}/purchase/`,
    purchaseData,
  );
  return response;
}

// Serviços para histórico de estoque
export async function getProductStockHistory(): Promise<ProductStockHistory[]> {
  const response = await http.get<
    ProductStockHistory[] | { results: ProductStockHistory[] }
  >("/api/v1/game/stock-history/");
  return Array.isArray(response) ? response : response.results || [];
}

export async function getProductStockHistoryByProduct(
  productId: string,
): Promise<ProductStockHistory[]> {
  const response = await http.get<
    ProductStockHistory[] | { results: ProductStockHistory[] }
  >(`/api/v1/game/stock-history/?product=${productId}`);
  return Array.isArray(response) ? response : response.results || [];
}

// Serviços para vendas
export async function simulateSale(saleData: SaleSimulation): Promise<any> {
  const response = await http.post(
    "/api/v1/game/sales/simulate_sale/",
    saleData,
  );
  return response;
}

export async function getSalesSummary(): Promise<SalesSummary> {
  const response = await http.get<SalesSummary>(
    "/api/v1/game/sales/sales_summary/",
  );
  return response;
}

export async function getSalesChartsData(
  period: "daily" | "weekly" | "monthly" = "monthly",
  daysBack: number = 30,
): Promise<SalesChartData> {
  const response = await http.get<SalesChartData>(
    `/api/v1/game/sales/sales_charts_data/?period=${period}&days_back=${daysBack}`,
  );
  return response;
}

export async function getDetailedAnalysis(
  daysBack: number = 30,
): Promise<DetailedAnalysis> {
  const response = await http.get<DetailedAnalysis>(
    `/api/v1/game/sales/detailed_analysis/?days_back=${daysBack}`,
  );
  return response;
}

// Funções utilitárias para produtos
export function getStockStatusColor(status: string): string {
  const colors: Record<string, string> = {
    NORMAL: "#10B981", // green-500
    LOW_STOCK: "#F59E0B", // amber-500
    OUT_OF_STOCK: "#EF4444", // red-500
  };
  return colors[status] || "#6B7280"; // gray-500
}

export function getStockStatusText(status: string): string {
  const texts: Record<string, string> = {
    NORMAL: "Estoque Normal",
    LOW_STOCK: "Estoque Baixo",
    OUT_OF_STOCK: "Fora de Estoque",
  };
  return texts[status] || "Desconhecido";
}

export function getStockStatusIcon(status: string): string {
  const icons: Record<string, string> = {
    NORMAL: "✅",
    LOW_STOCK: "⚠️",
    OUT_OF_STOCK: "❌",
  };
  return icons[status] || "❓";
}

export function formatCurrency(value: number): string {
  return new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
  }).format(value);
}

export function formatNumber(value: number): string {
  return new Intl.NumberFormat("pt-BR").format(value);
}

export function calculateProfitMargin(
  purchasePrice: number,
  salePrice: number,
): number {
  if (salePrice <= 0) return 0;
  return ((salePrice - purchasePrice) / salePrice) * 100;
}

export function calculateTotalValue(
  unitPrice: number,
  quantity: number,
): number {
  return unitPrice * quantity;
}

export function isLowStock(currentStock: number, minStock: number): boolean {
  return currentStock <= minStock;
}

export function isOutOfStock(currentStock: number): boolean {
  return currentStock <= 0;
}

export function getStockStatus(
  currentStock: number,
  minStock: number,
): "NORMAL" | "LOW_STOCK" | "OUT_OF_STOCK" {
  if (isOutOfStock(currentStock)) return "OUT_OF_STOCK";
  if (isLowStock(currentStock, minStock)) return "LOW_STOCK";
  return "NORMAL";
}

// Tipos para reposição de estoque
export interface RestockCostResponse {
  total_cost: number;
  products_count: number;
  products_needing_restock: Array<{
    id: string;
    name: string;
    current_stock: number;
    max_stock: number;
    quantity_needed: number;
    unit_price: number;
    total_cost: number;
  }>;
}

export interface RestockAllResponse {
  success: boolean;
  message: string;
  total_cost: number;
  restocked_products: Array<{
    id: string;
    name: string;
    quantity_added: number;
    new_stock: number;
    cost: number;
  }>;
  new_balance: number;
}

// Serviços para reposição de estoque
export async function getRestockCost(): Promise<RestockCostResponse> {
  const response = await http.get<RestockCostResponse>(
    "/api/v1/game/products/restock_cost/",
  );
  return response;
}

export async function restockAllProducts(): Promise<RestockAllResponse> {
  const response = await http.post<RestockAllResponse>(
    "/api/v1/game/products/restock_all/",
  );
  return response;
}

// Tipos para lucros mensais
export interface MonthlyProfit {
  month: string;
  month_key: string;
  revenue: number;
  expenses: number;
  profit: number;
  profit_formatted: string;
  revenue_formatted: string;
  expenses_formatted: string;
}

export interface MonthlyProfitsResponse {
  monthly_profits: MonthlyProfit[];
  total_profit: number;
  total_profit_formatted: string;
  months_count: number;
}

// Serviço para buscar lucros mensais
export async function getMonthlyProfits(): Promise<MonthlyProfitsResponse> {
  const response = await http.get<MonthlyProfitsResponse>(
    "/api/v1/game/dashboard/monthly_profits/",
  );
  return response;
}
