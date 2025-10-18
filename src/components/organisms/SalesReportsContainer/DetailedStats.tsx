"use client";

import React from "react";
import styled from "styled-components";
import { motion } from "framer-motion";
import {
  MdTrendingUp,
  MdTrendingDown,
  MdAttachMoney,
  MdShoppingCart,
  MdAnalytics,
  MdStar,
} from "react-icons/md";
import { DetailedAnalysis } from "@/types/game";
import { formatCurrency, formatNumber } from "@/services/GameServices";

const StatsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
`;

const StatCard = styled(motion.div)`
  background: ${(props) => props.theme.colors.backgroundSecondary};
  border: 1px solid ${(props) => props.theme.colors.border};
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
`;

const StatIcon = styled.div<{ color: string }>`
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: ${(props) => props.color}20;
  color: ${(props) => props.color};
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
`;

const StatContent = styled.div`
  flex: 1;
`;

const StatValue = styled.div`
  font-size: 1.5rem;
  font-weight: bold;
  color: ${(props) => props.theme.colors.textPrimary};
`;

const StatLabel = styled.div`
  font-size: 0.875rem;
  color: ${(props) => props.theme.colors.textSecondary};
`;

const StatChange = styled.div<{ $positive: boolean }>`
  font-size: 0.75rem;
  color: ${(props) => (props.$positive ? "#10B981" : "#EF4444")};
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.25rem;
`;

const AnalysisSection = styled.div`
  background: ${(props) => props.theme.colors.backgroundSecondary};
  border: 1px solid ${(props) => props.theme.colors.border};
  border-radius: 16px;
  padding: 1.5rem;
  margin-bottom: 1rem;
`;

const SectionTitle = styled.h3`
  font-size: 1.125rem;
  font-weight: 600;
  color: ${(props) => props.theme.colors.textPrimary};
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
`;

const AnalysisGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
`;

const AnalysisItem = styled.div`
  padding: 1rem;
  background: ${(props) => props.theme.colors.backgroundTertiary};
  border-radius: 8px;
`;

const AnalysisLabel = styled.div`
  font-size: 0.875rem;
  color: ${(props) => props.theme.colors.textSecondary};
  margin-bottom: 0.5rem;
`;

const AnalysisValue = styled.div`
  font-size: 1.125rem;
  font-weight: 600;
  color: ${(props) => props.theme.colors.textPrimary};
`;

interface DetailedStatsProps {
  data: DetailedAnalysis;
}

export default function DetailedStats({ data }: DetailedStatsProps) {
  const {
    general_stats,
    best_selling_product,
    most_sold_product,
    growth_analysis,
  } = data;

  return (
    <>
      {/* Estatísticas Principais */}
      <StatsGrid>
        <StatCard
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
        >
          <StatIcon color="#10B981">
            <MdAttachMoney />
          </StatIcon>
          <StatContent>
            <StatValue>{general_stats.total_revenue_formatted}</StatValue>
            <StatLabel>Receita Total</StatLabel>
            <StatChange $positive={growth_analysis.growth_percentage >= 0}>
              {growth_analysis.growth_percentage >= 0 ? (
                <MdTrendingUp />
              ) : (
                <MdTrendingDown />
              )}
              {growth_analysis.growth_formatted}
            </StatChange>
          </StatContent>
        </StatCard>

        <StatCard
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <StatIcon color="#3B82F6">
            <MdShoppingCart />
          </StatIcon>
          <StatContent>
            <StatValue>{formatNumber(general_stats.total_quantity)}</StatValue>
            <StatLabel>Unidades Vendidas</StatLabel>
            <StatChange $positive={true}>
              <MdAnalytics />
              {general_stats.total_transactions} transações
            </StatChange>
          </StatContent>
        </StatCard>

        <StatCard
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
        >
          <StatIcon color="#F59E0B">
            <MdAttachMoney />
          </StatIcon>
          <StatContent>
            <StatValue>{general_stats.avg_unit_price_formatted}</StatValue>
            <StatLabel>Preço Médio Unitário</StatLabel>
          </StatContent>
        </StatCard>

        <StatCard
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
        >
          <StatIcon color="#8B5CF6">
            <MdStar />
          </StatIcon>
          <StatContent>
            <StatValue>
              {best_selling_product?.product__name || "N/A"}
            </StatValue>
            <StatLabel>Produto com Maior Receita</StatLabel>
            {best_selling_product && (
              <StatChange $positive={true}>
                {formatCurrency(best_selling_product.total_revenue)}
              </StatChange>
            )}
          </StatContent>
        </StatCard>
      </StatsGrid>

      {/* Análise Detalhada */}
      <AnalysisSection>
        <SectionTitle>
          <MdAnalytics />
          Análise Detalhada
        </SectionTitle>
        <AnalysisGrid>
          <AnalysisItem>
            <AnalysisLabel>Produto Mais Vendido</AnalysisLabel>
            <AnalysisValue>
              {most_sold_product?.product__name || "N/A"}
            </AnalysisValue>
            {most_sold_product && (
              <div
                style={{
                  fontSize: "0.875rem",
                  color: "#6B7280",
                  marginTop: "0.25rem",
                }}
              >
                {formatNumber(most_sold_product.total_quantity)} unidades
              </div>
            )}
          </AnalysisItem>

          <AnalysisItem>
            <AnalysisLabel>Crescimento de Vendas</AnalysisLabel>
            <AnalysisValue
              style={{
                color:
                  growth_analysis.growth_percentage >= 0
                    ? "#10B981"
                    : "#EF4444",
              }}
            >
              {growth_analysis.growth_formatted}
            </AnalysisValue>
            <div
              style={{
                fontSize: "0.875rem",
                color: "#6B7280",
                marginTop: "0.25rem",
              }}
            >
              vs período anterior
            </div>
          </AnalysisItem>

          <AnalysisItem>
            <AnalysisLabel>Período Analisado</AnalysisLabel>
            <AnalysisValue>{data.period.days_back} dias</AnalysisValue>
            <div
              style={{
                fontSize: "0.875rem",
                color: "#6B7280",
                marginTop: "0.25rem",
              }}
            >
              {data.period.start_date} - {data.period.end_date}
            </div>
          </AnalysisItem>

          <AnalysisItem>
            <AnalysisLabel>Total de Transações</AnalysisLabel>
            <AnalysisValue>
              {formatNumber(general_stats.total_transactions)}
            </AnalysisValue>
            <div
              style={{
                fontSize: "0.875rem",
                color: "#6B7280",
                marginTop: "0.25rem",
              }}
            >
              vendas realizadas
            </div>
          </AnalysisItem>
        </AnalysisGrid>
      </AnalysisSection>
    </>
  );
}
