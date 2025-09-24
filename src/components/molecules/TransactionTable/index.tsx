'use client'

import React, { useState } from 'react'
import { styled } from 'styled-components'
import { MdEdit, MdDelete, MdTrendingUp, MdTrendingDown } from 'react-icons/md'
import type { Transaction } from '@/types/finance'

interface TransactionTableProps {
  transactions?: Transaction[];
  onEdit: (transaction: Transaction) => void;
  onDelete: (id: string) => void;
}

const TableCard = styled.div`
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

const Table = styled.table`
  width: 100%;
  border-collapse: collapse;
`;

const TableHead = styled.thead`
  background: ${({ theme }) => theme.colors.backgroundSecondary};
`;

const TableHeader = styled.th`
  padding: 1rem 0.75rem;
  text-align: left;
  font-size: 0.85rem;
  font-weight: 600;
  color: ${({ theme }) => theme.colors.textSecondary};
  border-bottom: 1px solid ${({ theme }) => theme.colors.border};
`;

const TableBody = styled.tbody``;

const TableRow = styled.tr`
  border-bottom: 1px solid ${({ theme }) => theme.colors.border};
  
  &:hover {
    background: ${({ theme }) => theme.colors.backgroundSecondary};
  }
  
  &:last-child {
    border-bottom: none;
  }
`;

const TableCell = styled.td`
  padding: 1rem 0.75rem;
  font-size: 0.9rem;
  color: ${({ theme }) => theme.colors.textPrimary};
`;

const AmountCell = styled(TableCell)<{ type: 'INCOME' | 'EXPENSE' }>`
  font-weight: 600;
  color: ${({ type, theme }) => type === 'INCOME' ? '#10b981' : '#ef4444'};
  display: flex;
  align-items: center;
  gap: 0.5rem;
`;

const ActionCell = styled(TableCell)`
  display: flex;
  gap: 0.5rem;
`;

const ActionButton = styled.button<{ variant?: 'edit' | 'delete' }>`
  padding: 0.5rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
  
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

const formatCurrency = (amount: number) => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(amount)
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('pt-BR')
}

export default function TransactionTable({ transactions, onEdit, onDelete }: TransactionTableProps) {
  const [sortField, setSortField] = useState<keyof Transaction>('created_at')
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('desc')

  const handleSort = (field: keyof Transaction) => {
    if (sortField === field) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc')
    } else {
      setSortField(field)
      setSortDirection('asc')
    }
  }

  const safeTransactions = Array.isArray(transactions) ? transactions : []
  const sortedTransactions = safeTransactions.sort((a, b) => {
    const aValue = a[sortField]
    const bValue = b[sortField]
    
    if (aValue == null || bValue == null) return 0
    if (aValue < bValue) return sortDirection === 'asc' ? -1 : 1
    if (aValue > bValue) return sortDirection === 'asc' ? 1 : -1
    return 0
  })

  if (safeTransactions.length === 0) {
    return (
      <TableCard>
        <Header>
          <Title>Transações</Title>
        </Header>
        <EmptyState>
          <EmptyTitle>Nenhuma transação encontrada</EmptyTitle>
          <EmptyText>Adicione uma nova transação para começar</EmptyText>
        </EmptyState>
      </TableCard>
    )
  }

  return (
    <TableCard>
      <Header>
        <Title>Transações ({safeTransactions.length})</Title>
      </Header>

      <Table>
        <TableHead>
          <tr>
            <TableHeader onClick={() => handleSort('created_at')}>
              Data {sortField === 'created_at' && (sortDirection === 'asc' ? '↑' : '↓')}
            </TableHeader>
            <TableHeader onClick={() => handleSort('description')}>
              Descrição {sortField === 'description' && (sortDirection === 'asc' ? '↑' : '↓')}
            </TableHeader>
            <TableHeader onClick={() => handleSort('category')}>
              Categoria {sortField === 'category' && (sortDirection === 'asc' ? '↑' : '↓')}
            </TableHeader>
            <TableHeader onClick={() => handleSort('amount')}>
              Valor {sortField === 'amount' && (sortDirection === 'asc' ? '↑' : '↓')}
            </TableHeader>
            <TableHeader>Ações</TableHeader>
          </tr>
        </TableHead>
        <TableBody>
          {sortedTransactions.map((transaction) => (
            <TableRow key={transaction.id}>
              <TableCell>{formatDate(transaction.created_at)}</TableCell>
              <TableCell>{transaction.description || '-'}</TableCell>
              <TableCell>{transaction.category_name}</TableCell>
              <AmountCell type={transaction.transaction_type}>
                {transaction.transaction_type === 'INCOME' ? (
                  <MdTrendingUp />
                ) : (
                  <MdTrendingDown />
                )}
                {formatCurrency(transaction.amount)}
              </AmountCell>
              <ActionCell>
                <ActionButton
                  variant="edit"
                  onClick={() => onEdit(transaction)}
                  title="Editar transação"
                >
                  <MdEdit size={16} />
                </ActionButton>
                <ActionButton
                  variant="delete"
                  onClick={() => onDelete(transaction.id)}
                  title="Excluir transação"
                >
                  <MdDelete size={16} />
                </ActionButton>
              </ActionCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableCard>
  )
}
