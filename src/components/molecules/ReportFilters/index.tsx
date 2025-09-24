'use client'

import React from 'react'
import { styled } from 'styled-components'

interface ReportFiltersProps {
  filters: { year: number; month: number };
  onChange: (filters: { year: number; month: number }) => void;
  loading: boolean;
}

const FiltersCard = styled.div`
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border: 1px solid ${({ theme }) => theme.colors.border};
`;

const Title = styled.h3`
  font-size: 1.1rem;
  font-weight: 600;
  color: ${({ theme }) => theme.colors.textPrimary};
  margin: 0 0 1rem 0;
`;

const FiltersGrid = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
`;

const FormGroup = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
`;

const Label = styled.label`
  font-size: 0.9rem;
  font-weight: 500;
  color: ${({ theme }) => theme.colors.textSecondary};
`;

const Select = styled.select`
  padding: 0.75rem;
  border: 1px solid ${({ theme }) => theme.colors.border};
  border-radius: 8px;
  font-size: 0.9rem;
  background: white;
  
  &:focus {
    outline: none;
    border-color: ${({ theme }) => theme.colors.primaryBlue};
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
  }
  
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
`;

const months = [
  { value: 1, label: 'Janeiro' },
  { value: 2, label: 'Fevereiro' },
  { value: 3, label: 'Março' },
  { value: 4, label: 'Abril' },
  { value: 5, label: 'Maio' },
  { value: 6, label: 'Junho' },
  { value: 7, label: 'Julho' },
  { value: 8, label: 'Agosto' },
  { value: 9, label: 'Setembro' },
  { value: 10, label: 'Outubro' },
  { value: 11, label: 'Novembro' },
  { value: 12, label: 'Dezembro' }
]

const generateYears = () => {
  const currentYear = new Date().getFullYear()
  const years = []
  for (let i = currentYear; i >= currentYear - 5; i--) {
    years.push(i)
  }
  return years
}

export default function ReportFilters({ filters, onChange, loading }: ReportFiltersProps) {
  const handleYearChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    onChange({
      ...filters,
      year: parseInt(e.target.value)
    })
  }

  const handleMonthChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    onChange({
      ...filters,
      month: parseInt(e.target.value)
    })
  }

  return (
    <FiltersCard>
      <Title>Filtros do Relatório</Title>
      
      <FiltersGrid>
        <FormGroup>
          <Label htmlFor="year">Ano</Label>
          <Select
            id="year"
            value={filters.year}
            onChange={handleYearChange}
            disabled={loading}
          >
            {generateYears().map(year => (
              <option key={year} value={year}>
                {year}
              </option>
            ))}
          </Select>
        </FormGroup>

        <FormGroup>
          <Label htmlFor="month">Mês</Label>
          <Select
            id="month"
            value={filters.month}
            onChange={handleMonthChange}
            disabled={loading}
          >
            {months.map(month => (
              <option key={month.value} value={month.value}>
                {month.label}
              </option>
            ))}
          </Select>
        </FormGroup>
      </FiltersGrid>
    </FiltersCard>
  )
}
