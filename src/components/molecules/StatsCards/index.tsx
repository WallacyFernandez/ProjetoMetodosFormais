'use client'

import React from 'react'
import { styled } from 'styled-components'
import { MdTrendingUp, MdTrendingDown, MdReceipt } from 'react-icons/md'
import type { MonthlySummary } from '@/types/finance'

interface StatsCardsProps {
  monthlySummary: MonthlySummary;
}

const CardsContainer = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
`;

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
  justify-content: space-between;
  margin-bottom: 1rem;
`;

const Title = styled.h4`
  font-size: 0.9rem;
  font-weight: 600;
  color: ${({ theme }) => theme.colors.textSecondary};
  margin: 0;
`;

const IconContainer = styled.div<{ $color: string }>`
  background: ${({ $color }) => $color}20;
  border-radius: 8px;
  padding: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: ${({ $color }) => $color};
`;

const Amount = styled.div`
  font-size: 1.8rem;
  font-weight: 700;
  color: ${({ theme }) => theme.colors.textPrimary};
  margin-bottom: 0.5rem;
`;

const TransactionCount = styled.div`
  font-size: 0.8rem;
  color: ${({ theme }) => theme.colors.textSecondary};
  display: flex;
  align-items: center;
  gap: 0.5rem;
`;

const formatCurrency = (amount: number): string => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(amount)
}

export default function StatsCards({ monthlySummary }: StatsCardsProps) {
  const incomeColor = '#10B981' // green-500
  const expenseColor = '#EF4444' // red-500
  const balanceColor = monthlySummary.balance >= 0 ? '#3B82F6' : '#EF4444' // blue-500 or red-500

  return (
    <CardsContainer>
      {/* Receitas */}
      <Card>
        <Header>
          <Title>Receitas</Title>
          <IconContainer $color={incomeColor}>
            <MdTrendingUp size={20} />
          </IconContainer>
        </Header>
        <Amount>{formatCurrency(monthlySummary.income_total)}</Amount>
        <TransactionCount>
          <MdReceipt size={14} />
          Este mês
        </TransactionCount>
      </Card>

      {/* Despesas */}
      <Card>
        <Header>
          <Title>Despesas</Title>
          <IconContainer $color={expenseColor}>
            <MdTrendingDown size={20} />
          </IconContainer>
        </Header>
        <Amount>{formatCurrency(monthlySummary.expense_total)}</Amount>
        <TransactionCount>
          <MdReceipt size={14} />
          Este mês
        </TransactionCount>
      </Card>

      {/* Saldo Mensal */}
      <Card>
        <Header>
          <Title>Lucro Bruto Mensal</Title>
          <IconContainer $color={balanceColor}>
            {monthlySummary.balance >= 0 ? (
              <MdTrendingUp size={20} />
            ) : (
              <MdTrendingDown size={20} />
            )}
          </IconContainer>
        </Header>
        <Amount style={{ color: balanceColor }}>
          {formatCurrency(monthlySummary.balance)}
        </Amount>
        <TransactionCount>
          <MdReceipt size={14} />
          {monthlySummary.transaction_count} transações
        </TransactionCount>
      </Card>
    </CardsContainer>
  )
}
