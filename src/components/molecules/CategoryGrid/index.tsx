'use client'

import React from 'react'
import { styled } from 'styled-components'
import { MdEdit, MdDelete } from 'react-icons/md'
import type { Category } from '@/types/finance'

interface CategoryGridProps {
  categories?: Category[];
  onEdit: (category: Category) => void;
  onDelete: (id: string) => void;
}

const GridCard = styled.div`
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
  margin-bottom: 1.5rem;
`;

const Title = styled.h3`
  font-size: 1.1rem;
  font-weight: 600;
  color: ${({ theme }) => theme.colors.textPrimary};
  margin: 0;
`;

const Grid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
`;

const CategoryCard = styled.div`
  background: ${({ theme }) => theme.colors.backgroundSecondary};
  border-radius: 12px;
  padding: 1.5rem;
  border: 1px solid ${({ theme }) => theme.colors.border};
  position: relative;
  transition: all 0.2s ease;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }
`;

const CategoryHeader = styled.div`
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
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
`;

const CategoryInfo = styled.div`
  flex: 1;
`;

const CategoryName = styled.h4`
  font-size: 1rem;
  font-weight: 600;
  color: ${({ theme }) => theme.colors.textPrimary};
  margin: 0 0 0.25rem 0;
`;

const CategoryType = styled.span<{ type: string }>`
  font-size: 0.75rem;
  font-weight: 500;
  padding: 0.25rem 0.5rem;
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

const CategoryDescription = styled.p`
  font-size: 0.85rem;
  color: ${({ theme }) => theme.colors.textSecondary};
  margin: 0.5rem 0 0 0;
  line-height: 1.4;
`;

const ActionButtons = styled.div`
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
  display: flex;
  gap: 0.25rem;
  opacity: 0;
  transition: opacity 0.2s ease;
  
  ${CategoryCard}:hover & {
    opacity: 1;
  }
`;

const ActionButton = styled.button<{ variant?: 'edit' | 'delete' }>`
  padding: 0.375rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  
  ${({ variant = 'edit' }) => variant === 'edit' ? `
    background: #f3f4f6;
    color: #374151;
    
    &:hover {
      background: #e5e7eb;
    }
  ` : `
    background: #fef2f2;
    color: #dc2626;
    
    &:hover {
      background: #fee2e2;
    }
  `}
`;

const EmptyState = styled.div`
  text-align: center;
  padding: 3rem 1rem;
  color: ${({ theme }) => theme.colors.textSecondary};
`;

const EmptyTitle = styled.h4`
  font-size: 1rem;
  font-weight: 600;
  margin: 0 0 0.5rem 0;
`;

const EmptyText = styled.p`
  font-size: 0.9rem;
  margin: 0;
`;

const getTypeLabel = (type: string) => {
  switch (type) {
    case 'INCOME': return 'Receita'
    case 'EXPENSE': return 'Despesa'
    case 'BOTH': return 'Ambos'
    default: return type
  }
}

export default function CategoryGrid({ categories, onEdit, onDelete }: CategoryGridProps) {
  const safeCategories = Array.isArray(categories) ? categories : []
  if (safeCategories.length === 0) {
    return (
      <GridCard>
        <Header>
          <Title>Categorias</Title>
        </Header>
        <EmptyState>
          <EmptyTitle>Nenhuma categoria encontrada</EmptyTitle>
          <EmptyText>Crie uma nova categoria para começar</EmptyText>
        </EmptyState>
      </GridCard>
    )
  }

  return (
    <GridCard>
      <Header>
        <Title>Categorias ({safeCategories.length})</Title>
      </Header>

      <Grid>
        {safeCategories.map((category) => (
          <CategoryCard key={category.id}>
            <ActionButtons>
              <ActionButton
                variant="edit"
                onClick={() => onEdit(category)}
                title="Editar categoria"
              >
                <MdEdit size={14} />
              </ActionButton>
              <ActionButton
                variant="delete"
                onClick={() => onDelete(category.id)}
                title="Excluir categoria"
              >
                <MdDelete size={14} />
              </ActionButton>
            </ActionButtons>

            <CategoryHeader>
              <CategoryIcon color={category.color}>
                {category.icon || '📁'}
              </CategoryIcon>
              <CategoryInfo>
                <CategoryName>{category.name}</CategoryName>
                <CategoryType type={category.category_type}>
                  {getTypeLabel(category.category_type)}
                </CategoryType>
              </CategoryInfo>
            </CategoryHeader>

            {category.description && (
              <CategoryDescription>{category.description}</CategoryDescription>
            )}
          </CategoryCard>
        ))}
      </Grid>
    </GridCard>
  )
}
