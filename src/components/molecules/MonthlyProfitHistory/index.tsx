"use client";

import React from "react";
import styled from "styled-components";
import { motion } from "framer-motion";
import { MonthlyProfit } from "@/services/GameServices";
import theme from "@/app/styles/theme";
import { MdTrendingUp, MdTrendingDown, MdAttachMoney } from "react-icons/md";

const Container = styled.div`
  background: ${theme.colors.white};
  border-radius: ${theme.borderRadius.lg};
  padding: ${theme.spacing.lg};
  box-shadow: ${theme.shadows.md};
  border: 1px solid ${theme.colors.border};
  height: 400px;
  overflow: hidden;
`;

const Header = styled.div`
  display: flex;
  align-items: center;
  gap: ${theme.spacing.sm};
  margin-bottom: ${theme.spacing.md};
  color: ${theme.colors.textPrimary};
  font-weight: 600;
`;

const TotalProfit = styled.div`
  background: ${theme.colors.backgroundTertiary};
  border-radius: ${theme.borderRadius.md};
  padding: ${theme.spacing.md};
  margin-bottom: ${theme.spacing.md};
  text-align: center;
`;

const TotalProfitLabel = styled.div`
  font-size: ${theme.fontSizes.sm};
  color: ${theme.colors.textSecondary};
  margin-bottom: ${theme.spacing.xs};
`;

const TotalProfitValue = styled.div`
  font-size: 1.5rem;
  font-weight: 800;
  color: ${theme.colors.textPrimary};
`;

const ProfitList = styled.div`
  height: 280px;
  overflow-y: auto;
  overflow-x: hidden;
`;

const ProfitItem = styled(motion.div)<{ $isPositive: boolean }>`
  display: flex;
  align-items: center;
  gap: ${theme.spacing.md};
  padding: ${theme.spacing.md};
  background: ${theme.colors.backgroundTertiary};
  border-radius: ${theme.borderRadius.md};
  margin-bottom: ${theme.spacing.sm};
  border-left: 3px solid
    ${({ $isPositive }) =>
      $isPositive ? theme.colors.primaryGreen : theme.colors.error};
`;

const MonthInfo = styled.div`
  flex: 1;
  min-width: 0;
`;

const MonthName = styled.div`
  font-weight: 600;
  color: ${theme.colors.textPrimary};
  font-size: ${theme.fontSizes.sm};
`;

const ProfitDetails = styled.div`
  font-size: ${theme.fontSizes.xs};
  color: ${theme.colors.textSecondary};
  margin-top: ${theme.spacing.xs};
`;

const ProfitValue = styled.div<{ $isPositive: boolean }>`
  font-weight: 700;
  font-size: ${theme.fontSizes.sm};
  color: ${({ $isPositive }) =>
    $isPositive ? theme.colors.primaryGreen : theme.colors.error};
`;

const ProfitIcon = styled.div<{ $isPositive: boolean }>`
  font-size: 1.25rem;
  color: ${({ $isPositive }) =>
    $isPositive ? theme.colors.primaryGreen : theme.colors.error};
`;

const EmptyState = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 200px;
  color: ${theme.colors.textSecondary};
  text-align: center;
`;

const EmptyIcon = styled.div`
  font-size: 3rem;
  margin-bottom: ${theme.spacing.md};
  opacity: 0.5;
`;

interface MonthlyProfitHistoryProps {
  monthlyProfits: MonthlyProfit[];
  totalProfit: number;
  totalProfitFormatted: string;
}

export default function MonthlyProfitHistory({
  monthlyProfits,
  totalProfit,
  totalProfitFormatted,
}: MonthlyProfitHistoryProps) {
  const isTotalPositive = totalProfit >= 0;

  return (
    <Container>
      <Header>
        <MdAttachMoney />
        Histórico de Lucros Mensais
      </Header>

      <TotalProfit>
        <TotalProfitLabel>Lucro Bruto Total</TotalProfitLabel>
        <TotalProfitValue>{totalProfitFormatted}</TotalProfitValue>
      </TotalProfit>

      <ProfitList>
        {monthlyProfits.length > 0 ? (
          monthlyProfits.map((profit, index) => {
            const isPositive = profit.profit >= 0;
            return (
              <ProfitItem
                key={profit.month_key}
                $isPositive={isPositive}
                initial={{ opacity: 0, x: 50 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <ProfitIcon $isPositive={isPositive}>
                  {isPositive ? <MdTrendingUp /> : <MdTrendingDown />}
                </ProfitIcon>
                <MonthInfo>
                  <MonthName>{profit.month}</MonthName>
                  <ProfitDetails>
                    Receitas: {profit.revenue_formatted} | Despesas:{" "}
                    {profit.expenses_formatted}
                  </ProfitDetails>
                </MonthInfo>
                <ProfitValue $isPositive={isPositive}>
                  {profit.profit_formatted}
                </ProfitValue>
              </ProfitItem>
            );
          })
        ) : (
          <EmptyState>
            <EmptyIcon>📊</EmptyIcon>
            <div>Nenhum lucro mensal registrado ainda</div>
            <div
              style={{
                fontSize: theme.fontSizes.xs,
                marginTop: theme.spacing.sm,
              }}
            >
              Os lucros aparecerão aqui conforme as vendas forem registradas
            </div>
          </EmptyState>
        )}
      </ProfitList>
    </Container>
  );
}
