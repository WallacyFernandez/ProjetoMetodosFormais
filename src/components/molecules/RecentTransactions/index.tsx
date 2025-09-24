'use client'

import React from 'react'
import { styled } from 'styled-components'
import { MdReceipt, MdTrendingUp, MdTrendingDown } from 'react-icons/md'
import type { Transaction } from '@/types/finance'

interface RecentTransactionsProps {
  transactions?: Transaction[];
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

const TransactionsList = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1rem;
`;

const TransactionItem = styled.div`
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem;
  border-radius: 8px;
  background: ${({ theme }) => theme.colors.backgroundSecondary};
  transition: background-color 0.2s ease;

  &:hover {
    background: ${({ theme }) => theme.colors.backgroundTertiary};
  }
`;

const CategoryIcon = styled.div<{ $color: string }>`
  background: ${({ $color }) => $color}20;
  color: ${({ $color }) => $color};
  border-radius: 8px;
  padding: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  min-width: 40px;
  height: 40px;
`;

const TransactionInfo = styled.div`
  flex: 1;
  min-width: 0;
`;

const TransactionDescription = styled.div`
  font-weight: 600;
  color: ${({ theme }) => theme.colors.textPrimary};
  margin-bottom: 0.25rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
`;

const TransactionCategory = styled.div`
  font-size: 0.8rem;
  color: ${({ theme }) => theme.colors.textSecondary};
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
`;

const TransactionAmount = styled.div<{ $isIncome: boolean }>`
  font-weight: 700;
  color: ${({ $isIncome }) => $isIncome ? '#10B981' : '#EF4444'};
  display: flex;
  align-items: center;
  gap: 0.5rem;
`;

const TransactionDate = styled.div`
  font-size: 0.8rem;
  color: ${({ theme }) => theme.colors.textSecondary};
  text-align: right;
  margin-top: 0.25rem;
`;

const EmptyState = styled.div`
  text-align: center;
  padding: 2rem;
  color: ${({ theme }) => theme.colors.textSecondary};
`;

const formatCurrency = (amount: number): string => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(amount)
}

const formatDate = (dateString: string): string => {
  return new Date(dateString).toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  })
}

export default function RecentTransactions({ transactions }: RecentTransactionsProps) {
  const safeTransactions = Array.isArray(transactions) ? transactions : []
  if (safeTransactions.length === 0) {
    return (
      <Card>
        <Header>
          <MdReceipt size={20} color="#6B7280" />
          <Title>Transações Recentes</Title>
        </Header>
        <EmptyState>
          Nenhuma transação encontrada
        </EmptyState>
      </Card>
    )
  }

  return (
    <Card>
      <Header>
        <MdReceipt size={20} color="#6B7280" />
        <Title>Transações Recentes</Title>
      </Header>
      
      <TransactionsList>
        {safeTransactions.slice(0, 5).map((transaction) => (
          <TransactionItem key={transaction.id}>
            <CategoryIcon $color={transaction.category_color}>
              {transaction.category_icon}
            </CategoryIcon>
            
            <TransactionInfo>
              <TransactionDescription>
                {transaction.description}
              </TransactionDescription>
              <TransactionCategory>
                {transaction.category_name}
              </TransactionCategory>
            </TransactionInfo>
            
            <div>
              <TransactionAmount $isIncome={transaction.transaction_type === 'INCOME'}>
                {transaction.transaction_type === 'INCOME' ? (
                  <MdTrendingUp size={16} />
                ) : (
                  <MdTrendingDown size={16} />
                )}
                {formatCurrency(transaction.amount)}
              </TransactionAmount>
              <TransactionDate>
                {formatDate(transaction.transaction_date)}
              </TransactionDate>
            </div>
          </TransactionItem>
        ))}
      </TransactionsList>
    </Card>
  )
}
