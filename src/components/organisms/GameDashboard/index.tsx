"use client";

import React, { useState, useEffect, useContext } from "react";
import styled from "styled-components";
import { motion, AnimatePresence } from "framer-motion";
import { toast } from "react-hot-toast";
import { IsSidebarOnContext } from "@/context/IsSidebarOnContext";
import {
  getGameDashboardData,
  startGame,
  pauseGame,
  resumeGame,
  resetGame,
  updateGameTime,
  formatGameDate,
  getGameStatusColor,
  getGameStatusText,
  calculateGameProgress,
  getRestockCost,
  restockAllProducts,
} from "@/services/GameServices";
import { GameDashboardData, RealtimeSale } from "@/types/game";
import theme from "@/app/styles/theme";
import {
  MdPlayArrow,
  MdPause,
  MdRefresh,
  MdShoppingCart,
  MdTrendingUp,
  MdAccessTime,
  MdAttachMoney,
  MdInventory,
  MdWarning,
  MdAddShoppingCart,
  MdInfo,
} from "react-icons/md";

// Styled Components
const Container = styled.div<{ $isCollapsed: boolean }>`
  margin-left: ${({ $isCollapsed }) => ($isCollapsed ? "0rem" : "16rem")};
  padding: 2rem;
  min-height: 100vh;
  background: ${theme.colors.backgroundSecondary};
  transition: margin-left 0.3s ease;
`;

const Header = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
`;

const Title = styled.h1`
  font-size: 2.5rem;
  font-weight: 800;
  color: ${theme.colors.textPrimary};
`;

const GameControls = styled.div`
  display: flex;
  gap: 1rem;
`;

const ControlButton = styled(motion.button)<{
  $variant: "primary" | "secondary" | "danger";
}>`
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s ease;

  ${({ $variant }) => {
    switch ($variant) {
      case "primary":
        return `
          background: ${theme.colors.primaryGreen};
          color: white;
          &:hover { background: ${theme.colors.secondaryGreen}; }
        `;
      case "secondary":
        return `
          background: ${theme.colors.white};
          color: ${theme.colors.textPrimary};
          border: 1px solid ${theme.colors.border};
          &:hover { background: ${theme.colors.backgroundTertiary}; }
        `;
      case "danger":
        return `
          background: ${theme.colors.error};
          color: white;
          &:hover { background: ${theme.colors.crimsonRed}; }
        `;
    }
  }}

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
`;

const MainContent = styled.div`
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 2rem;
  height: calc(100vh - 200px);
`;

const LeftPanel = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
`;

const RightPanel = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
`;

const Card = styled(motion.div)<{ $color?: string }>`
  background: ${theme.colors.white};
  border-radius: ${theme.borderRadius.lg};
  padding: ${theme.spacing.lg};
  box-shadow: ${theme.shadows.md};
  border: 1px solid ${theme.colors.border};
`;

const CardTitle = styled.h3`
  font-size: ${theme.fontSizes.sm};
  font-weight: 600;
  color: ${theme.colors.textSecondary};
  margin-bottom: ${theme.spacing.sm};
`;

const CardValue = styled.div`
  font-size: 2rem;
  font-weight: 800;
  color: ${theme.colors.textPrimary};
`;

const StatusBadge = styled.div<{ $color: string }>`
  display: inline-flex;
  align-items: center;
  padding: 0.5rem 1rem;
  border-radius: 2rem;
  background: ${({ $color }) => $color}20;
  color: ${({ $color }) => $color};
  font-weight: 600;
  font-size: 0.875rem;
`;

const SalesWindow = styled(Card)`
  background: ${theme.colors.white};
  color: ${theme.colors.textPrimary};
  height: 400px;
  overflow: hidden;
  border: 1px solid ${theme.colors.border};
`;

const SalesHeader = styled.div`
  display: flex;
  align-items: center;
  gap: ${theme.spacing.sm};
  margin-bottom: ${theme.spacing.md};
  color: ${theme.colors.textPrimary};
  font-weight: 600;
`;

const SalesList = styled.div`
  height: 320px;
  overflow-y: auto;
  overflow-x: hidden;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
`;

const SaleItem = styled(motion.div)`
  display: flex;
  align-items: center;
  gap: ${theme.spacing.md};
  padding: ${theme.spacing.md};
  background: ${theme.colors.backgroundTertiary};
  border-radius: ${theme.borderRadius.lg};
  border-left: 3px solid ${theme.colors.primaryGreen};
  margin-bottom: ${theme.spacing.sm};
  min-width: 0;
  overflow: hidden;
`;

const SaleIcon = styled.div`
  font-size: 1.25rem;
`;

const SaleInfo = styled.div`
  flex: 1;
  min-width: 0;
  overflow: hidden;
`;

const SaleProduct = styled.div`
  font-weight: 600;
  color: ${theme.colors.textPrimary};
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
`;

const SaleDetails = styled.div`
  font-size: ${theme.fontSizes.xs};
  color: ${theme.colors.textSecondary};
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
`;

const DayProgressCard = styled(Card)`
  background: ${theme.colors.white};
  color: ${theme.colors.textPrimary};
  border: 1px solid ${theme.colors.border};
`;

const ProgressBar = styled.div`
  width: 100%;
  height: 8px;
  background: ${theme.colors.backgroundTertiary};
  border-radius: ${theme.borderRadius.sm};
  overflow: hidden;
  margin: ${theme.spacing.md} 0;
`;

const ProgressFill = styled(motion.div)`
  height: 100%;
  background: linear-gradient(
    90deg,
    ${theme.colors.primaryGreen},
    ${theme.colors.lightGreen}
  );
  border-radius: ${theme.borderRadius.sm};
`;

const LoadingContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 50vh;
  color: ${theme.colors.textPrimary};
  font-size: ${theme.fontSizes.xl};
`;

const ErrorContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 50vh;
  color: ${theme.colors.error};
  font-size: ${theme.fontSizes.xl};
`;

const RestockButton = styled(motion.button)<{ $disabled?: boolean }>`
  background: ${({ $disabled }) => 
    $disabled ? theme.colors.mediumGrey : theme.colors.primaryGreen};
  color: white;
  border: none;
  border-radius: ${theme.borderRadius.md};
  padding: 0.5rem 1rem;
  font-size: ${theme.fontSizes.sm};
  font-weight: 600;
  cursor: ${({ $disabled }) => $disabled ? 'not-allowed' : 'pointer'};
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s ease;
  margin-top: ${theme.spacing.sm};

  &:hover {
    background: ${({ $disabled }) => 
      $disabled ? theme.colors.mediumGrey : theme.colors.secondaryGreen};
  }

  &:disabled {
    opacity: 0.5;
  }
`;

const RestockInfo = styled.div`
  background: ${theme.colors.backgroundTertiary};
  border-radius: ${theme.borderRadius.sm};
  padding: ${theme.spacing.sm};
  margin-top: ${theme.spacing.sm};
  font-size: ${theme.fontSizes.xs};
  color: ${theme.colors.textSecondary};
`;

export default function GameDashboard() {
  const { isCollapsed } = useContext(IsSidebarOnContext);
  const [dashboardData, setDashboardData] = useState<GameDashboardData | null>(
    null,
  );
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isUpdating, setIsUpdating] = useState(false);
  const [isGameControlUpdating, setIsGameControlUpdating] = useState(false);
  const [dayProgress, setDayProgress] = useState(0);
  const [restockCost, setRestockCost] = useState<number | null>(null);
  const [isLoadingRestockCost, setIsLoadingRestockCost] = useState(false);
  const [isRestocking, setIsRestocking] = useState(false);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getGameDashboardData();
      console.log("Dados carregados:", data);
      setDashboardData(data);
    } catch (err) {
      console.error("Erro ao carregar dados do jogo:", err);
      setError("Erro ao carregar dados do jogo");
      toast.error("Erro ao carregar dados do jogo");
    } finally {
      setLoading(false);
    }
  };

  const loadRestockCost = async () => {
    try {
      setIsLoadingRestockCost(true);
      const costData = await getRestockCost();
      setRestockCost(costData.total_cost);
    } catch (err) {
      console.error("Erro ao carregar custo de reposição:", err);
      toast.error("Erro ao carregar custo de reposição");
    } finally {
      setIsLoadingRestockCost(false);
    }
  };

  const loadRestockCostSilently = async () => {
    try {
      const costData = await getRestockCost();
      setRestockCost(costData.total_cost);
    } catch (err) {
      console.error("Erro ao carregar custo de reposição silenciosamente:", err);
    }
  };

  const handleRestockAll = async () => {
    if (!restockCost) {
      toast.error("Não foi possível calcular o custo de reposição");
      return;
    }

    const confirmMessage = `Deseja repor todo o estoque por R$ ${restockCost.toLocaleString('pt-BR', {
      minimumFractionDigits: 2,
    })}?`;
    
    if (!window.confirm(confirmMessage)) {
      return;
    }

    try {
      setIsRestocking(true);
      const result = await restockAllProducts();
      
      // Atualizar apenas os dados necessários ao invés de recarregar tudo
      setDashboardData((prev) => {
        if (!prev) return prev;
        return {
          ...prev,
          balance: {
            ...prev.balance,
            current_balance: result.new_balance,
            balance_formatted: `R$ ${result.new_balance.toLocaleString('pt-BR', {
              minimumFractionDigits: 2,
            })}`
          }
        };
      });
      
      // Atualizar custo de reposição (deve ser 0 agora)
      await loadRestockCost();
      
      toast.success(result.message);
    } catch (err: any) {
      console.error("Erro ao repor estoque:", err);
      
      if (err.response?.data?.error === 'Saldo insuficiente') {
        const data = err.response.data;
        toast.error(
          `Saldo insuficiente! Necessário: R$ ${data.required_amount.toLocaleString('pt-BR', {
            minimumFractionDigits: 2,
          })} | Disponível: R$ ${data.current_balance.toLocaleString('pt-BR', {
            minimumFractionDigits: 2,
          })}`
        );
      } else {
        toast.error("Erro ao repor estoque");
      }
    } finally {
      setIsRestocking(false);
    }
  };

  const updateSalesData = async () => {
    try {
      const data = await getGameDashboardData();
      console.log("Dados atualizados:", {
        total_sales: data.sales?.total_sales,
        realtime_sales_count: data.realtime_sales?.length,
        current_day_sales: data.game_session?.current_day_sales_count,
      });
      setDashboardData((prev) => {
        if (!prev) return data;

        return {
          ...prev,
          game_session: {
            ...prev.game_session,
            ...data.game_session,
          },
          balance: data.balance,
          products: data.products,
          sales: data.sales,
          stock_alerts: data.stock_alerts,
          realtime_sales: data.realtime_sales,
        };
      });
    } catch (err) {
      console.error("Erro ao atualizar dados de vendas:", err);
    }
  };

  const handleStartGame = async () => {
    try {
      setIsGameControlUpdating(true);
      console.log("Iniciando jogo...");
      const result = await startGame();
      console.log("Jogo iniciado:", result);

      setDashboardData((prev) => {
        if (!prev) return prev;

        return {
          ...prev,
          game_session: {
            ...prev.game_session,
            status: result.status,
          },
        };
      });

      toast.success("Jogo iniciado! Os dias começaram a passar.");
    } catch (err) {
      console.error("Erro ao iniciar jogo:", err);
      toast.error("Erro ao iniciar jogo");
    } finally {
      setIsGameControlUpdating(false);
    }
  };

  const handlePauseGame = async () => {
    try {
      setIsGameControlUpdating(true);
      const result = await pauseGame();

      setDashboardData((prev) => {
        if (!prev) return prev;

        return {
          ...prev,
          game_session: {
            ...prev.game_session,
            status: result.status,
            last_update_time: result.last_update_time,
          },
        };
      });

      // Para a barra de progresso imediatamente quando pausa
      setDayProgress(0);
      toast.success("Jogo pausado");
    } catch (err) {
      console.error("Erro ao pausar jogo:", err);
      toast.error("Erro ao pausar jogo");
    } finally {
      setIsGameControlUpdating(false);
    }
  };

  const handleResumeGame = async () => {
    try {
      setIsGameControlUpdating(true);
      const result = await resumeGame();

      setDashboardData((prev) => {
        if (!prev) return prev;

        return {
          ...prev,
          game_session: {
            ...prev.game_session,
            status: result.status,
            last_update_time: result.last_update_time,
          },
        };
      });

      // Reseta a barra de progresso para começar do zero quando retoma
      setDayProgress(0);
      toast.success("Jogo retomado");
    } catch (err) {
      console.error("Erro ao retomar jogo:", err);
      toast.error("Erro ao retomar jogo");
    } finally {
      setIsGameControlUpdating(false);
    }
  };

  const handleResetGame = async () => {
    if (
      window.confirm(
        "Tem certeza que deseja reiniciar o jogo? Todos os progressos serão perdidos.",
      )
    ) {
      try {
        setIsGameControlUpdating(true);
        await resetGame();
        await loadDashboardData();
        toast.success("Jogo reiniciado");
      } catch (err) {
        console.error("Erro ao reiniciar jogo:", err);
        toast.error("Erro ao reiniciar jogo");
      } finally {
        setIsGameControlUpdating(false);
      }
    }
  };

  const handleUpdateTime = async () => {
    // Evita consultas simultâneas
    if (isUpdating) return;

    try {
      setIsUpdating(true);
      console.log("Atualizando tempo do jogo...");
      const result = await updateGameTime();
      console.log("Resultado da atualização:", result);

      // Sempre atualiza os dados da sessão, mesmo sem dias completos
      setDashboardData((prev) => {
        if (!prev) return prev;

        return {
          ...prev,
          game_session: {
            ...prev.game_session,
            current_game_date: result.game_session.current_game_date,
            days_survived: result.game_session.days_survived,
            days_remaining: result.game_session.days_remaining,
            game_progress_percentage:
              result.game_session.game_progress_percentage,
            status: result.game_session.status,
            last_update_time: result.game_session.last_update_time,
          },
        };
      });

      // Atualiza dados de vendas e produtos sempre
      updateSalesData();

      // Se passou um dia completo, reseta a barra de progresso
      if (result.days_passed > 0) {
        setDayProgress(0); // Reset progress bar
        toast.success(`${result.days_passed} dia(s) passaram no jogo!`);
      }
    } catch (err) {
      console.error("Erro ao atualizar tempo:", err);
      toast.error("Erro ao atualizar tempo");
    } finally {
      setIsUpdating(false);
    }
  };

  const handleManualUpdateTime = async () => {
    try {
      setIsGameControlUpdating(true);
      console.log("Atualizando tempo do jogo manualmente...");
      const result = await updateGameTime();
      console.log("Resultado da atualização manual:", result);

      // Sempre atualiza os dados da sessão, mesmo sem dias completos
      setDashboardData((prev) => {
        if (!prev) return prev;

        return {
          ...prev,
          game_session: {
            ...prev.game_session,
            current_game_date: result.game_session.current_game_date,
            days_survived: result.game_session.days_survived,
            days_remaining: result.game_session.days_remaining,
            game_progress_percentage:
              result.game_session.game_progress_percentage,
            status: result.game_session.status,
            last_update_time: result.game_session.last_update_time,
          },
        };
      });

      // Atualiza dados de vendas e produtos sempre
      updateSalesData();

      // Se passou um dia completo, reseta a barra de progresso
      if (result.days_passed > 0) {
        setDayProgress(0); // Reset progress bar
        toast.success(`${result.days_passed} dia(s) passaram no jogo!`);
      } else {
        toast.success("Tempo atualizado com sucesso!");
      }
    } catch (err) {
      console.error("Erro ao atualizar tempo manualmente:", err);
      toast.error("Erro ao atualizar tempo");
    } finally {
      setIsGameControlUpdating(false);
    }
  };

  // Atualiza progresso do dia em tempo real
  useEffect(() => {
    if (dashboardData?.game_session.status === "ACTIVE") {
      const interval = setInterval(() => {
        // Calcula o progresso baseado no tempo real decorrido
        const now = new Date();
        const lastUpdate = new Date(
          dashboardData.game_session.last_update_time,
        );
        const timeDiff = (now.getTime() - lastUpdate.getTime()) / 1000; // em segundos
        const timeAcceleration = dashboardData.game_session.time_acceleration;

        // Calcula o progresso do dia atual (0-100%)
        // Usa Math.floor para evitar valores decimais erráticos
        const dayProgress = Math.floor(
          ((timeDiff % timeAcceleration) / timeAcceleration) * 100,
        );

        // Só atualiza se o progresso for válido e diferente do atual
        const validProgress = Math.min(Math.max(dayProgress, 0), 100);
        setDayProgress(validProgress);
      }, 1000);

      return () => clearInterval(interval);
    } else {
      // Quando pausado, mantém a barra zerada
      setDayProgress(0);
    }
  }, [
    dashboardData?.game_session.status,
    dashboardData?.game_session.last_update_time,
    dashboardData?.game_session.time_acceleration,
  ]);

  // Atualiza dados a cada 1 segundo para vendas em tempo real
  useEffect(() => {
    const interval = setInterval(() => {
      if (dashboardData?.game_session.status === "ACTIVE") {
        handleUpdateTime();
      }
    }, 1000); // 1 segundo para vendas verdadeiramente em tempo real

    return () => clearInterval(interval);
  }, [dashboardData?.game_session.status]);

  useEffect(() => {
    loadDashboardData();
    loadRestockCost();
  }, []);

  // Recarregar custo de reposição quando os dados do dashboard mudarem
  useEffect(() => {
    if (dashboardData) {
      loadRestockCostSilently();
    }
  }, [dashboardData?.products]);

  if (loading) {
    return (
      <Container $isCollapsed={isCollapsed}>
        <LoadingContainer>
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
          >
            <MdRefresh size={32} />
          </motion.div>
          <span style={{ marginLeft: "1rem" }}>
            Carregando dados do jogo...
          </span>
        </LoadingContainer>
      </Container>
    );
  }

  if (error) {
    return (
      <Container $isCollapsed={isCollapsed}>
        <ErrorContainer>
          <MdWarning size={32} />
          <span style={{ marginLeft: "1rem" }}>{error}</span>
        </ErrorContainer>
      </Container>
    );
  }

  const {
    game_session,
    balance,
    products,
    sales,
    stock_alerts,
    realtime_sales,
  } = dashboardData || {};
  const progress = game_session
    ? calculateGameProgress(
        game_session.current_game_date,
        game_session.game_start_date,
        game_session.game_end_date,
      )
    : 0;

  return (
    <Container $isCollapsed={isCollapsed}>
      <Header>
        <Title>Supermercado Simulator</Title>
        <GameControls>
          {game_session?.status === "ACTIVE" ? (
            <ControlButton
              type="button"
              $variant="secondary"
              onClick={handlePauseGame}
              disabled={isGameControlUpdating}
            >
              <MdPause />
              Pausar
            </ControlButton>
          ) : game_session?.status === "PAUSED" ? (
            <ControlButton
              type="button"
              $variant="primary"
              onClick={handleResumeGame}
              disabled={isGameControlUpdating}
            >
              <MdPlayArrow />
              Retomar
            </ControlButton>
          ) : game_session?.status === "NOT_STARTED" ? (
            <ControlButton
              type="button"
              $variant="primary"
              onClick={handleStartGame}
              disabled={isGameControlUpdating}
            >
              <MdPlayArrow />
              Iniciar Jogo
            </ControlButton>
          ) : (
            <ControlButton
              type="button"
              $variant="primary"
              onClick={handleStartGame}
              disabled={isGameControlUpdating}
            >
              <MdPlayArrow />
              Reiniciar Jogo
            </ControlButton>
          )}
          <ControlButton
            type="button"
            $variant="secondary"
            onClick={handleManualUpdateTime}
            disabled={isGameControlUpdating}
          >
            <MdRefresh />
            Atualizar Tempo
          </ControlButton>
          <ControlButton
            type="button"
            $variant="danger"
            onClick={handleResetGame}
            disabled={isGameControlUpdating}
          >
            <MdRefresh />
            Reiniciar
          </ControlButton>
        </GameControls>
      </Header>

      <MainContent>
        <LeftPanel>
          {/* Janela de Vendas em Tempo Real */}
          <SalesWindow>
            <SalesHeader>
              <MdShoppingCart />
              Vendas em Tempo Real
            </SalesHeader>
            <SalesList>
              <AnimatePresence>
                {realtime_sales
                  ?.slice(0, 10)
                  .map((sale: RealtimeSale, index: number) => (
                    <SaleItem
                      key={sale.id}
                      initial={{ opacity: 0, x: 50 }}
                      animate={{ opacity: 1, x: 0 }}
                      exit={{ opacity: 0, x: -50 }}
                      transition={{ delay: index * 0.1 }}
                    >
                      <SaleIcon>🛒</SaleIcon>
                      <SaleInfo>
                        <SaleProduct>{sale.product_name}</SaleProduct>
                        <SaleDetails>
                          {sale.quantity}x - R${" "}
                          {parseFloat(sale.total_value.toString()).toFixed(2)} -{" "}
                          {sale.game_date_formatted} às {sale.game_time_formatted}
                        </SaleDetails>
                      </SaleInfo>
                    </SaleItem>
                  ))}
              </AnimatePresence>
              {(!realtime_sales || realtime_sales.length === 0) && (
                <div
                  style={{
                    textAlign: "center",
                    color: theme.colors.textSecondary,
                    padding: theme.spacing.xl,
                  }}
                >
                  {game_session?.is_market_open ? (
                    "Nenhuma venda ainda..."
                  ) : (
                    <div>
                      <div>🏪 Mercado fechado</div>
                      <div style={{ fontSize: theme.fontSizes.xs, marginTop: theme.spacing.sm }}>
                        Horário comercial: 6h às 22h
                      </div>
                    </div>
                  )}
                </div>
              )}
            </SalesList>
          </SalesWindow>
        </LeftPanel>

        <RightPanel>
          {/* Data Atual e Saldo */}
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "1fr 1fr",
              gap: "1.5rem",
            }}
          >
            <Card>
              <CardTitle>📅 Data Atual</CardTitle>
              <CardValue>
                {game_session
                  ? formatGameDate(game_session.current_game_date)
                  : "Carregando..."}
              </CardValue>
              {game_session && (
                <div
                  style={{
                    fontSize: theme.fontSizes.sm,
                    color: theme.colors.textSecondary,
                    marginTop: theme.spacing.sm,
                  }}
                >
                  🕐 {game_session.current_game_time}
                  {game_session.is_market_open ? (
                    <span style={{ color: theme.colors.primaryGreen, marginLeft: "0.5rem" }}>
                      ✅ Aberto
                    </span>
                  ) : (
                    <span style={{ color: theme.colors.error, marginLeft: "0.5rem" }}>
                      ❌ Fechado
                    </span>
                  )}
                </div>
              )}
              <div
                style={{
                  display: "grid",
                  gridTemplateColumns: "1fr 1fr",
                  gap: "1rem",
                  marginTop: theme.spacing.sm,
                }}
              >
                <div>
                  <div
                    style={{
                      fontSize: theme.fontSizes.sm,
                      color: theme.colors.textSecondary,
                    }}
                  >
                    ✅ Sobrevividos
                  </div>
                  <div
                    style={{
                      fontSize: "1.25rem",
                      fontWeight: 600,
                      color: theme.colors.primaryGreen,
                    }}
                  >
                    {game_session?.days_survived || 0}
                  </div>
                </div>
                <div>
                  <div
                    style={{
                      fontSize: theme.fontSizes.sm,
                      color: theme.colors.textSecondary,
                    }}
                  >
                    ⏳ Restantes
                  </div>
                  <div
                    style={{
                      fontSize: "1.25rem",
                      fontWeight: 600,
                      color: theme.colors.accentOrange,
                    }}
                  >
                    {game_session?.days_remaining || 0}
                  </div>
                </div>
              </div>
            </Card>

            <Card>
              <CardTitle>📦 Status do Estoque</CardTitle>
              <div
                style={{
                  display: "grid",
                  gridTemplateColumns: "1fr 1fr",
                  gap: "1rem",
                  marginTop: theme.spacing.sm,
                }}
              >
                <div>
                  <div
                    style={{
                      fontSize: theme.fontSizes.sm,
                      color: theme.colors.textSecondary,
                    }}
                  >
                    🚫 Em Falta
                  </div>
                  <div
                    style={{
                      fontSize: "1.5rem",
                      fontWeight: 600,
                      color: theme.colors.error,
                    }}
                  >
                    {products?.out_of_stock || 0}
                  </div>
                  {products && products.out_of_stock > 0 && (
                    <div
                      style={{
                        fontSize: theme.fontSizes.xs,
                        color: theme.colors.error,
                      }}
                    >
                      ⚠️ Reponha!
                    </div>
                  )}
                </div>
                <div>
                  <div
                    style={{
                      fontSize: theme.fontSizes.sm,
                      color: theme.colors.textSecondary,
                    }}
                  >
                    📉 Estoque Baixo
                  </div>
                  <div
                    style={{
                      fontSize: "1.5rem",
                      fontWeight: 600,
                      color: theme.colors.accentOrange,
                    }}
                  >
                    {products?.low_stock || 0}
                  </div>
                  {products && products.low_stock > 0 && (
                    <div
                      style={{
                        fontSize: theme.fontSizes.xs,
                        color: theme.colors.accentOrange,
                      }}
                    >
                      ⚠️ Considere repor
                    </div>
                  )}
                </div>
              </div>
              
              {/* Botão de Reposição */}
              <RestockButton
                type="button"
                $disabled={!restockCost || restockCost === 0 || isRestocking || isLoadingRestockCost}
                onClick={handleRestockAll}
                disabled={!restockCost || restockCost === 0 || isRestocking || isLoadingRestockCost}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                {isRestocking ? (
                  <>
                    <motion.div
                      animate={{ rotate: 360 }}
                      transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                    >
                      <MdRefresh size={16} />
                    </motion.div>
                    Repondo...
                  </>
                ) : (
                  <>
                    <MdAddShoppingCart size={16} />
                    Repor Todo Estoque
                  </>
                )}
              </RestockButton>

              {/* Informações de Custo */}
              {restockCost !== null && (
                <RestockInfo>
                  <div style={{ display: "flex", alignItems: "center", gap: "0.25rem", marginBottom: "0.25rem" }}>
                    <MdInfo size={14} />
                    <strong>Custo para repor:</strong>
                  </div>
                  <div style={{ fontWeight: 600, color: theme.colors.textPrimary }}>
                    R$ {restockCost.toLocaleString('pt-BR', {
                      minimumFractionDigits: 2,
                    })}
                  </div>
                  {restockCost === 0 && (
                    <div style={{ color: theme.colors.primaryGreen, fontSize: theme.fontSizes.xs }}>
                      ✅ Estoque já está no máximo!
                    </div>
                  )}
                </RestockInfo>
              )}
            </Card>
          </div>

          {/* Progresso do Dia e Status do Estoque */}
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "1fr 1fr",
              gap: "1.5rem",
            }}
          >
            <DayProgressCard>
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  marginBottom: theme.spacing.sm,
                }}
              >
                <CardTitle
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "0.5rem",
                  }}
                >
                  <MdAccessTime />
                  Progresso do Dia
                </CardTitle>
                <div>
                  <div
                    style={{
                      fontSize: theme.fontSizes.sm,
                      color: theme.colors.textSecondary,
                      textAlign: "center",
                    }}
                  >
                    Status
                  </div>
                  <StatusBadge
                    $color={
                      game_session
                        ? getGameStatusColor(game_session.status)
                        : theme.colors.mediumGrey
                    }
                  >
                    {game_session
                      ? getGameStatusText(game_session.status)
                      : "Carregando..."}
                  </StatusBadge>
                </div>
              </div>
              <ProgressBar>
                <ProgressFill
                  initial={{ width: 0 }}
                  animate={{ width: `${dayProgress}%` }}
                  transition={{ duration: 0.5 }}
                />
              </ProgressBar>
              <div
                style={{ fontSize: "0.875rem", color: "rgba(255,255,255,0.8)" }}
              >
                {Math.round(dayProgress)}% do dia concluído
              </div>
            </DayProgressCard>

            <Card>
              <CardTitle>Caixa da Loja</CardTitle>
              <CardValue>{balance?.balance_formatted || "R$ 0,00"}</CardValue>
              {balance && balance.current_balance < 1000 && (
                <div
                  style={{
                    color: theme.colors.error,
                    fontSize: theme.fontSizes.sm,
                    marginTop: theme.spacing.sm,
                  }}
                >
                  ⚠️ Saldo baixo!
                </div>
              )}
            </Card>
          </div>

          {/* Produtos Vendidos */}
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "1fr 1fr",
              gap: "1.5rem",
            }}
          >
            <Card>
              <CardTitle>🛒 Produtos Vendidos</CardTitle>
              <CardValue>
                {(sales?.total_sales || 0).toLocaleString()}
              </CardValue>
            </Card>

            <Card>
              <CardTitle>💰 Receita Total</CardTitle>
              <CardValue>
                R${" "}
                {(sales?.total_revenue || 0).toLocaleString("pt-BR", {
                  minimumFractionDigits: 2,
                })}
              </CardValue>
            </Card>
          </div>
        </RightPanel>
      </MainContent>
    </Container>
  );
}
