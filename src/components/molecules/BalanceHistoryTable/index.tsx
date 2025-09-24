'use client'

import React, { useState } from 'react'
import { styled } from 'styled-components'
import { MdTrendingUp, MdTrendingDown, MdSettings, MdRefresh } from 'react-icons/md'
import type { BalanceHistory } from '@/types/finance'

interface BalanceHistoryTableProps {
  history?: BalanceHistory[];
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

const OperationCell = styled(TableCell)`
  display: flex;
  align-items: center;
  gap: 0.5rem;
`;

const AmountCell = styled(TableCell)<{ operation: string }>`
  font-weight: 600;
  color: ${({ operation, theme }) => {
    switch (operation) {
      case 'ADD': return '#10b981'
      case 'SUBTRACT': return '#ef4444'
      case 'SET': return '#3b82f6'
      case 'RESET': return '#6b7280'
      default: return theme.colors.textPrimary
    }
  }};
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

const getOperationIcon = (operation: string) => {
  switch (operation) {
    case 'ADD': return <MdTrendingUp />
    case 'SUBTRACT': return <MdTrendingDown />
    case 'SET': return <MdSettings />
    case 'RESET': return <MdRefresh />
    default: return null
  }
}

const getOperationColor = (operation: string) => {
  switch (operation) {
    case 'ADD': return '#10b981'
    case 'SUBTRACT': return '#ef4444'
    case 'SET': return '#3b82f6'
    case 'RESET': return '#6b7280'
    default: return '#6b7280'
  }
}

const formatCurrency = (amount: number) => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(amount)
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleString('pt-BR')
}

export default function BalanceHistoryTable({ history }: BalanceHistoryTableProps) {
  const [sortField, setSortField] = useState<keyof BalanceHistory>('created_at')
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('desc')

  const handleSort = (field: keyof BalanceHistory) => {
    if (sortField === field) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc')
    } else {
      setSortField(field)
      setSortDirection('asc')
    }
  }

  const safeHistory = Array.isArray(history) ? history : []
  const sortedHistory = safeHistory.sort((a, b) => {
    const aValue = a[sortField]
    const bValue = b[sortField]
    
    if (aValue < bValue) return sortDirection === 'asc' ? -1 : 1
    if (aValue > bValue) return sortDirection === 'asc' ? 1 : -1
    return 0
  })

  if (safeHistory.length === 0) {
    return (
      <TableCard>
        <Header>
          <Title>Histórico de Saldo</Title>
        </Header>
        <EmptyState>
          <EmptyTitle>Nenhuma operação encontrada</EmptyTitle>
          <EmptyText>Realize operações no saldo para ver o histórico</EmptyText>
        </EmptyState>
      </TableCard>
    )
  }

  return (
    <TableCard>
      <Header>
        <Title>Histórico de Saldo ({safeHistory.length})</Title>
      </Header>

      <Table>
        <TableHead>
          <tr>
            <TableHeader onClick={() => handleSort('created_at')}>
              Data {sortField === 'created_at' && (sortDirection === 'asc' ? '↑' : '↓')}
            </TableHeader>
            <TableHeader onClick={() => handleSort('operation')}>
              Operação {sortField === 'operation' && (sortDirection === 'asc' ? '↑' : '↓')}
            </TableHeader>
            <TableHeader onClick={() => handleSort('amount')}>
              Valor {sortField === 'amount' && (sortDirection === 'asc' ? '↑' : '↓')}
            </TableHeader>
            <TableHeader onClick={() => handleSort('description')}>
              Descrição {sortField === 'description' && (sortDirection === 'asc' ? '↑' : '↓')}
            </TableHeader>
            <TableHeader onClick={() => handleSort('new_balance')}>
              Novo Saldo {sortField === 'new_balance' && (sortDirection === 'asc' ? '↑' : '↓')}
            </TableHeader>
          </tr>
        </TableHead>
        <TableBody>
          {sortedHistory.map((item) => (
            <TableRow key={item.id}>
              <TableCell>{formatDate(item.created_at)}</TableCell>
              <OperationCell>
                <span style={{ color: getOperationColor(item.operation) }}>
                  {getOperationIcon(item.operation)}
                </span>
                {item.operation_display}
              </OperationCell>
              <AmountCell operation={item.operation}>
                {formatCurrency(item.amount)}
              </AmountCell>
              <TableCell>{item.description || '-'}</TableCell>
              <TableCell style={{ fontWeight: '600' }}>
                {formatCurrency(item.new_balance)}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableCard>
  )
}
