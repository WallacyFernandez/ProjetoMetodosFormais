"use client";

import React, { useState, useEffect } from "react";
import styled from "styled-components";
import { motion, AnimatePresence } from "framer-motion";
import {
  MdTrendingUp,
  MdTrendingDown,
  MdBarChart,
  MdPieChart,
  MdAnalytics,
  MdRefresh,
  MdFilterList,
  MdCalendarToday,
} from "react-icons/md";
import { toast } from "react-toastify";
import {
  getSalesChartsData,
  getDetailedAnalysis,
  formatCurrency,
  formatNumber,
} from "@/services/GameServices";
import { SalesChartData, DetailedAnalysis } from "@/types/game";
import SalesChart from "./SalesChart";
import TopProductsChart from "./TopProductsChart";
import CategoryChart from "./CategoryChart";
import DetailedStats from "./DetailedStats";

const Container = styled.div`
  display: flex;
  flex-direction: column;
  gap: 2rem;
`;

const Header = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
`;

const Title = styled.h2`
  font-size: 1.5rem;
  font-weight: bold;
  color: ${(props) => props.theme.colors.textPrimary};
  display: flex;
  align-items: center;
  gap: 0.5rem;
`;

const Controls = styled.div`
  display: flex;
  gap: 1rem;
  align-items: center;
`;

const Select = styled.select`
  padding: 0.5rem 1rem;
  border: 1px solid ${(props) => props.theme.colors.border};
  border-radius: 8px;
  background: ${(props) => props.theme.colors.backgroundSecondary};
  color: ${(props) => props.theme.colors.textPrimary};
  font-size: 0.875rem;

  &:focus {
    outline: none;
    border-color: ${(props) => props.theme.colors.primaryGreen};
  }
`;

const Button = styled.button<{ $variant?: "primary" | "secondary" }>`
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s ease;

  ${(props) => {
    switch (props.$variant) {
      case "primary":
        return `
          background: ${props.theme.colors.primaryGreen};
          color: white;
          &:hover { background: ${props.theme.colors.secondaryGreen}; }
        `;
      default:
        return `
          background: ${props.theme.colors.backgroundTertiary};
          color: ${props.theme.colors.textPrimary};
          &:hover { background: ${props.theme.colors.ghostWhite}; }
        `;
    }
  }}
`;

const ChartsGrid = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;

  @media (max-width: 1200px) {
    grid-template-columns: 1fr;
  }
`;

const ChartCard = styled(motion.div)`
  background: ${(props) => props.theme.colors.backgroundSecondary};
  border: 1px solid ${(props) => props.theme.colors.border};
  border-radius: 16px;
  padding: 1.5rem;
`;

const ChartHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
`;

const ChartTitle = styled.h3`
  font-size: 1.125rem;
  font-weight: 600;
  color: ${(props) => props.theme.colors.textPrimary};
  display: flex;
  align-items: center;
  gap: 0.5rem;
`;

const LoadingSpinner = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
  color: ${(props) => props.theme.colors.textSecondary};
`;

const ErrorMessage = styled.div`
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 8px;
  padding: 1rem;
  color: #dc2626;
  text-align: center;
`;

const EmptyState = styled.div`
  text-align: center;
  padding: 2rem;
  color: ${(props) => props.theme.colors.textSecondary};
`;

const EmptyIcon = styled.div`
  font-size: 3rem;
  margin-bottom: 1rem;
  opacity: 0.5;
`;

const EmptyText = styled.p`
  font-size: 1rem;
  margin-bottom: 0.5rem;
`;

const EmptySubtext = styled.p`
  font-size: 0.875rem;
  opacity: 0.7;
`;

export default function SalesReportsContainer() {
  const [chartData, setChartData] = useState<SalesChartData | null>(null);
  const [detailedAnalysis, setDetailedAnalysis] =
    useState<DetailedAnalysis | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [period, setPeriod] = useState<"daily" | "weekly" | "monthly">(
    "monthly",
  );
  const [daysBack, setDaysBack] = useState(30);

  useEffect(() => {
    loadData();
  }, [period, daysBack]);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);

      const [chartsData, analysisData] = await Promise.all([
        getSalesChartsData(period, daysBack),
        getDetailedAnalysis(daysBack),
      ]);

      setChartData(chartsData);
      setDetailedAnalysis(analysisData);
    } catch (error: any) {
      console.error("Erro ao carregar dados dos relatórios:", error);
      setError("Erro ao carregar dados dos relatórios");
      toast.error("Erro ao carregar dados dos relatórios");
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = () => {
    loadData();
  };

  if (loading) {
    return (
      <Container>
        <LoadingSpinner>
          <MdAnalytics size={24} />
          <span style={{ marginLeft: "0.5rem" }}>
            Carregando relatórios de vendas...
          </span>
        </LoadingSpinner>
      </Container>
    );
  }

  if (error) {
    return (
      <Container>
        <ErrorMessage>
          <MdAnalytics size={24} style={{ marginBottom: "0.5rem" }} />
          <div>{error}</div>
          <Button
            $variant="primary"
            onClick={handleRefresh}
            style={{ marginTop: "1rem" }}
          >
            <MdRefresh />
            Tentar Novamente
          </Button>
        </ErrorMessage>
      </Container>
    );
  }

  if (!chartData || !detailedAnalysis) {
    return (
      <Container>
        <EmptyState>
          <EmptyIcon>
            <MdBarChart />
          </EmptyIcon>
          <EmptyText>Nenhum dado de vendas encontrado</EmptyText>
          <EmptySubtext>
            Realize algumas vendas para visualizar os relatórios
          </EmptySubtext>
        </EmptyState>
      </Container>
    );
  }

  return (
    <Container>
      <Header>
        <Title>
          <MdAnalytics />
          Relatórios de Vendas
        </Title>
        <Controls>
          <Select
            value={period}
            onChange={(e) =>
              setPeriod(e.target.value as "daily" | "weekly" | "monthly")
            }
          >
            <option value="daily">Diário</option>
            <option value="weekly">Semanal</option>
            <option value="monthly">Mensal</option>
          </Select>
          <Select
            value={daysBack}
            onChange={(e) => setDaysBack(parseInt(e.target.value))}
          >
            <option value="7">Últimos 7 dias</option>
            <option value="30">Últimos 30 dias</option>
            <option value="90">Últimos 90 dias</option>
          </Select>
          <Button onClick={handleRefresh}>
            <MdRefresh />
            Atualizar
          </Button>
        </Controls>
      </Header>

      <AnimatePresence mode="wait">
        <motion.div
          key={`${period}-${daysBack}`}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          transition={{ duration: 0.3 }}
        >
          {/* Estatísticas Detalhadas */}
          <DetailedStats data={detailedAnalysis} />

          {/* Gráficos */}
          <ChartsGrid>
            <ChartCard
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.1 }}
            >
              <ChartHeader>
                <ChartTitle>
                  <MdBarChart />
                  Vendas por Período
                </ChartTitle>
              </ChartHeader>
              <SalesChart data={chartData.sales_by_period} period={period} />
            </ChartCard>

            <ChartCard
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.2 }}
            >
              <ChartHeader>
                <ChartTitle>
                  <MdPieChart />
                  Produtos Mais Vendidos
                </ChartTitle>
              </ChartHeader>
              <TopProductsChart data={chartData.top_products} />
            </ChartCard>

            <ChartCard
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.3 }}
            >
              <ChartHeader>
                <ChartTitle>
                  <MdPieChart />
                  Vendas por Categoria
                </ChartTitle>
              </ChartHeader>
              <CategoryChart data={chartData.sales_by_category} />
            </ChartCard>

            <ChartCard
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.4 }}
            >
              <ChartHeader>
                <ChartTitle>
                  <MdCalendarToday />
                  Vendas por Dia da Semana
                </ChartTitle>
              </ChartHeader>
              <SalesChart
                data={detailedAnalysis.sales_by_weekday.map((item) => ({
                  period: item.weekday,
                  period_key: item.weekday,
                  total_quantity: item.total_quantity,
                  total_revenue: item.total_revenue,
                  revenue_formatted: formatCurrency(item.total_revenue),
                }))}
                period="weekly"
                isWeekdayChart={true}
              />
            </ChartCard>
          </ChartsGrid>
        </motion.div>
      </AnimatePresence>
    </Container>
  );
}
