// Tipos para o jogo Supermercado Simulator

export interface GameSession {
  id: string;
  user_name: string;
  game_start_date: string;
  current_game_date: string;
  game_end_date: string;
  status: "NOT_STARTED" | "ACTIVE" | "PAUSED" | "COMPLETED" | "FAILED";
  time_acceleration: number;
  total_score: number;
  days_survived: number;
  game_progress_percentage: number;
  days_remaining: number;
  current_day_sales_count: number;
  last_update_time: string;
  current_game_time: string;
  is_market_open: boolean;
  created_at: string;
  updated_at: string;
}

// Removido: SupermarketBalance e BalanceHistory
// Agora usamos o sistema financeiro existente (UserBalance e Transaction)

export interface ProductCategory {
  id: string;
  name: string;
  description: string;
  icon: string;
  color: string;
  profit_margin_min: number;
  profit_margin_max: number;
  shelf_life_min: number;
  shelf_life_max: number;
  seasonal_demand_multiplier: number;
  created_at: string;
  updated_at: string;
}

export interface Supplier {
  id: string;
  name: string;
  contact_person: string;
  email: string;
  phone: string;
  address: string;
  delivery_time_days: number;
  minimum_order_value: number;
  reliability_score: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Product {
  id: string;
  name: string;
  description: string;
  category: string;
  category_name: string;
  category_icon: string;
  category_color: string;
  supplier: string;
  supplier_name: string;
  purchase_price: number;
  sale_price: number;
  current_price: number;
  profit_margin: number;
  profit_margin_formatted: string;
  current_stock: number;
  min_stock: number;
  max_stock: number;
  shelf_life_days: number;
  is_active: boolean;
  is_promotional: boolean;
  promotional_price?: number;
  promotional_start_date?: string;
  promotional_end_date?: string;
  is_low_stock: boolean;
  is_out_of_stock: boolean;
  stock_status: "NORMAL" | "LOW_STOCK" | "OUT_OF_STOCK";
  stock_percentage: number;
  created_at: string;
  updated_at: string;
}

export interface ProductStockHistory {
  id: string;
  product: string;
  product_name: string;
  operation: "PURCHASE" | "SALE" | "ADJUSTMENT" | "LOSS" | "RETURN";
  operation_display: string;
  quantity: number;
  previous_stock: number;
  new_stock: number;
  unit_price?: number;
  unit_price_formatted?: string;
  total_value?: number;
  total_value_formatted?: string;
  description: string;
  game_date: string;
  created_at: string;
}

export interface RealtimeSale {
  id: string;
  product_name: string;
  product_icon: string;
  quantity: number;
  unit_price: number;
  total_value: number;
  sale_time_formatted: string;
  game_date: string;
  game_date_formatted: string;
  game_time: string;
  game_time_formatted: string;
}

export interface GameDashboardData {
  game_session: GameSession;
  balance: {
    current_balance: number;
    balance_formatted: string;
  };
  products: {
    total: number;
    low_stock: number;
    out_of_stock: number;
  };
  sales: {
    total_sales: number;
    total_revenue: number;
  };
  stock_alerts: {
    low_stock_count: number;
    out_of_stock_count: number;
    has_alerts: boolean;
  };
  realtime_sales: RealtimeSale[];
}

// Removido: BalanceOperation
// Agora usamos o sistema financeiro existente

// Tipos para operações de estoque
export interface ProductStockOperation {
  quantity: number;
  description?: string;
  unit_price?: number;
}

export interface ProductPurchase {
  product_id: string;
  quantity: number;
  unit_price?: number;
  description?: string;
}

// Tipos para vendas
export interface SaleSimulation {
  product_id: string;
  quantity: number;
}

export interface SalesSummary {
  total_sales: number;
  total_revenue: number;
  recent_sales: ProductStockHistory[];
  top_products: Array<{
    product__name: string;
    total_quantity: number;
    total_revenue: number;
  }>;
}

// Tipos para relatórios de vendas
export interface SalesChartData {
  sales_by_period: Array<{
    period: string;
    period_key: string;
    total_quantity: number;
    total_revenue: number;
    revenue_formatted: string;
  }>;
  top_products: Array<{
    product__id: string;
    product__name: string;
    product__category__name: string;
    product__category__color: string;
    total_quantity: number;
    total_revenue: number;
  }>;
  sales_by_category: Array<{
    product__category__name: string;
    product__category__color: string;
    total_quantity: number;
    total_revenue: number;
  }>;
  period: "daily" | "weekly" | "monthly";
  start_date: string;
  end_date: string;
}

export interface DetailedAnalysis {
  general_stats: {
    total_quantity: number;
    total_revenue: number;
    total_revenue_formatted: string;
    avg_unit_price: number;
    avg_unit_price_formatted: string;
    total_transactions: number;
  };
  best_selling_product: {
    product__name: string;
    total_revenue: number;
  } | null;
  most_sold_product: {
    product__name: string;
    total_quantity: number;
  } | null;
  sales_by_weekday: Array<{
    weekday: string;
    total_quantity: number;
    total_revenue: number;
  }>;
  growth_analysis: {
    current_revenue: number;
    previous_revenue: number;
    growth_percentage: number;
    growth_formatted: string;
  };
  period: {
    start_date: string;
    end_date: string;
    days_back: number;
  };
}

// Tipos para configurações do jogo
export interface GameSettings {
  time_acceleration: number;
  difficulty: "EASY" | "NORMAL" | "HARD";
  auto_save: boolean;
  sound_enabled: boolean;
}

// Tipos para eventos do jogo
export interface GameEvent {
  id: string;
  title: string;
  description: string;
  event_type: "POSITIVE" | "NEGATIVE" | "NEUTRAL";
  impact_amount?: number;
  impact_description?: string;
  duration_days?: number;
  game_date: string;
  is_active: boolean;
}

// Tipos para funcionários (futuro)
export interface Employee {
  id: string;
  name: string;
  position: "CASHIER" | "STOCKER" | "MANAGER";
  position_display: string;
  salary: number;
  performance: number;
  satisfaction: number;
  hire_date: string;
  is_active: boolean;
}

// Tipos para relatórios do jogo
export interface GameReport {
  period: "DAILY" | "WEEKLY" | "MONTHLY";
  start_date: string;
  end_date: string;
  total_sales: number;
  total_purchases: number;
  total_expenses: number;
  net_profit: number;
  profit_margin: number;
  customer_satisfaction: number;
  employee_satisfaction: number;
  inventory_turnover: number;
}

// Tipos para objetivos do jogo
export interface GameObjective {
  id: string;
  title: string;
  description: string;
  objective_type: "SURVIVAL" | "PROFIT" | "GROWTH" | "EFFICIENCY";
  target_value: number;
  current_value: number;
  progress_percentage: number;
  deadline: string;
  reward_points: number;
  is_completed: boolean;
  is_failed: boolean;
}

// Tipos para estatísticas do jogo
export interface GameStats {
  total_play_time: number;
  games_completed: number;
  games_failed: number;
  best_score: number;
  average_score: number;
  total_profit_earned: number;
  total_customers_served: number;
  achievements_unlocked: number;
}
