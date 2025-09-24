'use client'

import React from 'react'
import { styled } from 'styled-components'
import { MdPieChart } from 'react-icons/md'
import type { CategorySummary } from '@/types/finance'

interface CategoryChartProps {
  categorySummary?: CategorySummary[];
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

const CategoriesList = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1rem;
`;

const CategoryItem = styled.div`
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem;
  border-radius: 8px;
  background: ${({ theme }) => theme.colors.backgroundSecondary};
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

const CategoryInfo = styled.div`
  flex: 1;
  min-width: 0;
`;

const CategoryName = styled.div`
  font-weight: 600;
  color: ${({ theme }) => theme.colors.textPrimary};
  margin-bottom: 0.25rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
`;

const CategoryDetails = styled.div`
  display: flex;
  align-items: center;
  gap: 0.5rem;
`;

const CategoryAmount = styled.div`
  font-weight: 600;
  color: ${({ theme }) => theme.colors.textPrimary};
`;

const CategoryPercentage = styled.div`
  font-size: 0.8rem;
  color: ${({ theme }) => theme.colors.textSecondary};
  background: ${({ theme }) => theme.colors.backgroundTertiary};
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
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

export default function CategoryChart({ categorySummary }: CategoryChartProps) {
  const safeCategorySummary = Array.isArray(categorySummary) ? categorySummary : []
  if (safeCategorySummary.length === 0) {
    return (
      <Card>
        <Header>
          <MdPieChart size={20} color="#6B7280" />
          <Title>Gastos por Categoria</Title>
        </Header>
        <EmptyState>
          Nenhum dado disponível
        </EmptyState>
      </Card>
    )
  }

  // Ordenar por valor total (maior primeiro)
  const sortedCategories = safeCategorySummary.sort((a, b) => b.total - a.total)

  return (
    <Card>
      <Header>
        <MdPieChart size={20} color="#6B7280" />
        <Title>Gastos por Categoria</Title>
      </Header>
      
      <CategoriesList>
        {sortedCategories.slice(0, 5).map((category, index) => (
          <CategoryItem key={`${category.category__name}-${category.transaction_type}`}>
            <CategoryIcon $color={category.category__color}>
              {category.category__icon}
            </CategoryIcon>
            
            <CategoryInfo>
              <CategoryName>
                {category.category__name}
              </CategoryName>
              <CategoryDetails>
                <CategoryAmount>
                  {formatCurrency(category.total)}
                </CategoryAmount>
                <CategoryPercentage>
                  {category.percentage.toFixed(1)}%
                </CategoryPercentage>
              </CategoryDetails>
            </CategoryInfo>
          </CategoryItem>
        ))}
      </CategoriesList>
    </Card>
  )
}
