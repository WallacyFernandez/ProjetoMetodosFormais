'use client'

import React from 'react'
import { styled } from 'styled-components'
import type { CategorySummary } from '@/types/finance'

interface CategoryReportCardProps {
  summary?: CategorySummary[];
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

const CategoryList = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1rem;
`;

const CategoryItem = styled.div`
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: ${({ theme }) => theme.colors.backgroundSecondary};
  border-radius: 8px;
  border: 1px solid ${({ theme }) => theme.colors.border};
`;

const CategoryIcon = styled.div<{ color: string }>`
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: ${({ color }) => color}20;
  color: ${({ color }) => color};
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  flex-shrink: 0;
`;

const CategoryInfo = styled.div`
  flex: 1;
`;

const CategoryName = styled.h4`
  font-size: 0.9rem;
  font-weight: 600;
  color: ${({ theme }) => theme.colors.textPrimary};
  margin: 0 0 0.25rem 0;
`;

const CategoryType = styled.span<{ type: string }>`
  font-size: 0.75rem;
  font-weight: 500;
  padding: 0.125rem 0.375rem;
  border-radius: 4px;
  background: ${({ type }) => {
    switch (type) {
      case 'INCOME': return '#10b98120'
      case 'EXPENSE': return '#ef444420'
      case 'BOTH': return '#3b82f620'
      default: return '#6b728020'
    }
  }};
  color: ${({ type }) => {
    switch (type) {
      case 'INCOME': return '#10b981'
      case 'EXPENSE': return '#ef4444'
      case 'BOTH': return '#3b82f6'
      default: return '#6b7280'
    }
  }};
`;

const CategoryAmount = styled.div<{ type: string }>`
  font-size: 1rem;
  font-weight: 700;
  color: ${({ type }) => {
    switch (type) {
      case 'INCOME': return '#10b981'
      case 'EXPENSE': return '#ef4444'
      case 'BOTH': return '#3b82f6'
      default: return '#6b7280'
    }
  }};
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

const getTypeLabel = (type: string) => {
  switch (type) {
    case 'INCOME': return 'Receita'
    case 'EXPENSE': return 'Despesa'
    case 'BOTH': return 'Ambos'
    default: return type
  }
}

export default function CategoryReportCard({ summary, loading }: CategoryReportCardProps) {
  const safeSummary = Array.isArray(summary) ? summary : []
  if (loading) {
    return (
      <Card>
        <Header>
          <Title>Resumo por Categoria</Title>
        </Header>
        <LoadingState>
          Carregando dados...
        </LoadingState>
      </Card>
    )
  }

  if (!summary || summary.length === 0) {
    return (
      <Card>
        <Header>
          <Title>Resumo por Categoria</Title>
        </Header>
        <EmptyState>
          <p>Nenhuma transação encontrada para o período selecionado</p>
        </EmptyState>
      </Card>
    )
  }

  return (
    <Card>
      <Header>
        <Title>Resumo por Categoria ({safeSummary.length})</Title>
      </Header>

      <CategoryList>
        {safeSummary.map((item, index) => (
          <CategoryItem key={`${item.category__name}-${index}`}>
            <CategoryIcon color={item.category__color}>
              {item.category__icon || '📁'}
            </CategoryIcon>
            
            <CategoryInfo>
              <CategoryName>{item.category__name}</CategoryName>
              <CategoryType type={item.transaction_type}>
                {getTypeLabel(item.transaction_type)}
              </CategoryType>
            </CategoryInfo>
            
            <CategoryAmount type={item.transaction_type}>
              {formatCurrency(item.total)}
            </CategoryAmount>
          </CategoryItem>
        ))}
      </CategoryList>
    </Card>
  )
}
