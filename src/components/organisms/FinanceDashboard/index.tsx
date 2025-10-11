"use client";

import React, { useContext, useEffect, useState } from "react";
import { styled } from "styled-components";
import { IsSidebarOnContext } from "@/context/IsSidebarOnContext";
import { GetDashboardData } from "@/services/FinanceServices";
import { getMonthlyProfits, MonthlyProfit } from "@/services/GameServices";
import type { DashboardData } from "@/types/finance";
import BalanceCard from "@/components/molecules/BalanceCard";
import StatsCards from "@/components/molecules/StatsCards";
import RecentTransactions from "@/components/molecules/RecentTransactions";
import CategoryChart from "@/components/molecules/CategoryChart";
import PageHeader from "@/components/molecules/PageHeader";
import MonthlyProfitHistory from "@/components/molecules/MonthlyProfitHistory";
import EmployeeQuickCard from "@/components/molecules/EmployeeQuickCard";
import { toast } from "react-toastify";

interface FinanceDashboardProps {
  $isCollapsed: boolean;
}

const Container = styled.div<FinanceDashboardProps>`
  background-color: ${({ theme }) => theme.colors.backgroundSecondary};
  margin-left: ${({ $isCollapsed }) => ($isCollapsed ? "0" : "16rem")};
  transition: all 0.3s ease-in-out;
  padding: 2rem;

  @media (max-width: 1000px) {
    margin-left: ${({ $isCollapsed }) => ($isCollapsed ? "7rem" : "18rem")};
  }

  @media (max-width: 834px) {
    margin-left: ${({ $isCollapsed }) => ($isCollapsed ? "3rem" : "17rem")};
  }

  @media (max-width: 768px) {
    margin-left: 0.3rem;
    margin-right: 0.3rem;
  }
`;

const DashboardGrid = styled.div`
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
  margin-top: 2rem;

  @media (min-width: 1200px) {
    grid-template-columns: 2fr 1fr;
  }
`;

const LeftColumn = styled.div`
  display: flex;
  flex-direction: column;
  gap: 2rem;
`;

const RightColumn = styled.div`
  display: flex;
  flex-direction: column;
  gap: 2rem;
`;

const CardsRow = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
`;

const LoadingContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 300px;
  font-size: 1.2rem;
  color: ${({ theme }) => theme.colors.textSecondary};
`;

const ErrorContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 300px;
  font-size: 1.2rem;
  color: ${({ theme }) => theme.colors.error};
  background-color: ${({ theme }) => theme.colors.backgroundSecondary};
  border-radius: 8px;
  border: 1px solid ${({ theme }) => theme.colors.error};
`;

export default function FinanceDashboard() {
  const { isCollapsed } = useContext(IsSidebarOnContext);
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(
    null,
  );
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [monthlyProfits, setMonthlyProfits] = useState<MonthlyProfit[]>([]);
  const [totalProfit, setTotalProfit] = useState(0);
  const [totalProfitFormatted, setTotalProfitFormatted] = useState("R$ 0,00");
  const [isLoadingProfits, setIsLoadingProfits] = useState(false);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await GetDashboardData();
      setDashboardData(data);
    } catch (err) {
      console.error("Erro ao carregar dados do dashboard:", err);
      setError("Erro ao carregar dados do dashboard");
      toast.error("Erro ao carregar dados do dashboard");
    } finally {
      setLoading(false);
    }
  };

  const loadMonthlyProfits = async () => {
    try {
      setIsLoadingProfits(true);
      const data = await getMonthlyProfits();
      setMonthlyProfits(data.monthly_profits);
      setTotalProfit(data.total_profit);
      setTotalProfitFormatted(data.total_profit_formatted);
    } catch (err) {
      console.error("Erro ao carregar lucros mensais:", err);
      toast.error("Erro ao carregar histórico de lucros");
    } finally {
      setIsLoadingProfits(false);
    }
  };

  useEffect(() => {
    loadDashboardData();
    loadMonthlyProfits();
  }, []);

  if (loading) {
    return (
      <Container $isCollapsed={isCollapsed}>
        <PageHeader $title="Dashboard Financeiro" $buttons={[]} />
        <LoadingContainer>Carregando dados do dashboard...</LoadingContainer>
      </Container>
    );
  }

  if (error || !dashboardData) {
    return (
      <Container $isCollapsed={isCollapsed}>
        <PageHeader $title="Dashboard Financeiro" $buttons={[]} />
        <ErrorContainer>{error || "Erro ao carregar dados"}</ErrorContainer>
      </Container>
    );
  }

  return (
    <Container $isCollapsed={isCollapsed}>
      <PageHeader $title="Dashboard Financeiro" $buttons={[]} />

      <CardsRow>
        <BalanceCard balance={dashboardData.current_balance} />
        <StatsCards monthlySummary={dashboardData.monthly_summary} />
        <EmployeeQuickCard />
      </CardsRow>

      <DashboardGrid>
        <LeftColumn>
          <RecentTransactions
            transactions={dashboardData.recent_transactions}
          />
          <MonthlyProfitHistory
            monthlyProfits={monthlyProfits}
            totalProfit={totalProfit}
            totalProfitFormatted={totalProfitFormatted}
          />
        </LeftColumn>

        <RightColumn>
          <CategoryChart categorySummary={dashboardData.category_summary} />
        </RightColumn>
      </DashboardGrid>
    </Container>
  );
}
