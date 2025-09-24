'use client'

import React from 'react'
import { styled } from 'styled-components'
import { MdTrendingUp, MdTrendingDown, MdAccountBalance } from 'react-icons/md'
import type { MonthlySummary } from '@/types/finance'

interface MonthlyReportCardProps {
  summary: MonthlySummary | null;
  loading: boolean;
}

const Card = styled.div`
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border: 1px solid ${({ theme }) => theme.colors.border};
`;

const Header = styled.div`
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
`;

const Title = styled.h3`
  font-size: 1.1rem;
  font-weight: 600;
  color: ${({ theme }) => theme.colors.textPrimary};
  margin: 0;
`;

const StatsGrid = styled.div`
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
`;

const StatCard = styled.div`
  background: ${({ theme }) => theme.colors.backgroundSecondary};
  border-radius: 8px;
  padding: 1rem;
  border: 1px solid ${({ theme }) => theme.colors.border};
`;

const StatHeader = styled.div`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
`;

const StatIcon = styled.div<{ color: string }>`
  color: ${({ color }) => color};
  display: flex;
  align-items: center;
  justify-content: center;
`;

const StatLabel = styled.span`
  font-size: 0.85rem;
  font-weight: 500;
  color: ${({ theme }) => theme.colors.textSecondary};
`;

const StatValue = styled.div`
  font-size: 1.25rem;
  font-weight: 700;
  color: ${({ theme }) => theme.colors.textPrimary};
`;

const EmptyState = styled.div`
  text-align: center;
  padding: 2rem 1rem;
  color: ${({ theme }) => theme.colors.textSecondary};
`;

const LoadingState = styled.div`
  text-align: center;
  padding: 2rem 1rem;
  color: ${({ theme }) => theme.colors.textSecondary};
`;

const formatCurrency = (amount: number) => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(amount)
}

export default function MonthlyReportCard({ summary, loading }: MonthlyReportCardProps) {
  if (loading) {
    return (
      <Card>
        <Header>
          <Title>Resumo Mensal</Title>
        </Header>
        <LoadingState>
          Carregando dados...
        </LoadingState>
      </Card>
    )
  }

  if (!summary) {
    return (
      <Card>
        <Header>
          <Title>Resumo Mensal</Title>
        </Header>
        <EmptyState>
          <p>Nenhum dado disponível para o período selecionado</p>
        </EmptyState>
      </Card>
    )
  }

  return (
    <Card>
      <Header>
        <Title>Resumo Mensal</Title>
      </Header>

      <StatsGrid>
        <StatCard>
          <StatHeader>
            <StatIcon color="#10b981">
              <MdTrendingUp />
            </StatIcon>
            <StatLabel>Total de Receitas</StatLabel>
          </StatHeader>
          <StatValue>{formatCurrency(summary.income_total)}</StatValue>
        </StatCard>

        <StatCard>
          <StatHeader>
            <StatIcon color="#ef4444">
              <MdTrendingDown />
            </StatIcon>
            <StatLabel>Total de Despesas</StatLabel>
          </StatHeader>
          <StatValue>{formatCurrency(summary.expense_total)}</StatValue>
        </StatCard>

        <StatCard>
          <StatHeader>
            <StatIcon color={summary.balance >= 0 ? '#10b981' : '#ef4444'}>
              <MdAccountBalance />
            </StatIcon>
            <StatLabel>Saldo Líquido</StatLabel>
          </StatHeader>
          <StatValue>{formatCurrency(summary.balance)}</StatValue>
        </StatCard>

        <StatCard>
          <StatHeader>
            <StatIcon color="#6b7280">
              <span>📊</span>
            </StatIcon>
            <StatLabel>Total de Transações</StatLabel>
          </StatHeader>
          <StatValue>{summary.transaction_count}</StatValue>
        </StatCard>
      </StatsGrid>
    </Card>
  )
}
