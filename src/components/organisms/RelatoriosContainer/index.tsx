'use client'

import React, { useContext, useEffect, useState } from 'react'
import { styled } from 'styled-components'
import { IsSidebarOnContext } from '@/context/IsSidebarOnContext'
import { 
  GetMonthlySummary, 
  GetCategorySummary 
} from '@/services/FinanceServices'
import type { MonthlySummary, CategorySummary } from '@/types/finance'
import PageHeader from '@/components/molecules/PageHeader'
import ReportFilters from '@/components/molecules/ReportFilters'
import MonthlyReportCard from '@/components/molecules/MonthlyReportCard'
import CategoryReportCard from '@/components/molecules/CategoryReportCard'
import { toast } from 'react-toastify'

interface RelatoriosContainerProps {
  $isCollapsed: boolean;
}

const Container = styled.div<RelatoriosContainerProps>`
  background-color: ${({ theme }) => theme.colors.backgroundSecondary};
  margin-left: ${({ $isCollapsed }) => $isCollapsed ? '80px' : '280px'};
  min-height: 100vh;
  padding: 2rem;
  transition: margin-left 0.3s ease;
`;

const Content = styled.div`
  max-width: 1200px;
  margin: 0 auto;
`;

const FiltersSection = styled.div`
  margin-bottom: 2rem;
`;

const ReportsGrid = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-top: 2rem;

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
`;

export default function RelatoriosContainer() {
  const { isCollapsed } = useContext(IsSidebarOnContext)
  const [monthlySummary, setMonthlySummary] = useState<MonthlySummary | null>(null)
  const [categorySummary, setCategorySummary] = useState<CategorySummary[]>([])
  const [loading, setLoading] = useState(false)
  const [filters, setFilters] = useState({
    year: new Date().getFullYear(),
    month: new Date().getMonth() + 1
  })

  const loadReports = async () => {
    try {
      setLoading(true)
      const [monthlyData, categoryData] = await Promise.all([
        GetMonthlySummary({ year: filters.year, month: filters.month }),
        GetCategorySummary({ year: filters.year, month: filters.month })
      ])
      setMonthlySummary(monthlyData)
      setCategorySummary(categoryData)
    } catch (error) {
      console.error('Erro ao carregar relatórios:', error)
      toast.error('Erro ao carregar relatórios')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadReports()
  }, [filters])

  const handleFiltersChange = (newFilters: { year: number; month: number }) => {
    setFilters(newFilters)
  }

  return (
    <Container $isCollapsed={isCollapsed}>
      <Content>
        <PageHeader 
          $title="Relatórios" 
          $subtitle="Visualize seus dados financeiros"
        />

        <FiltersSection>
          <ReportFilters
            filters={filters}
            onChange={handleFiltersChange}
            loading={loading}
          />
        </FiltersSection>

        <ReportsGrid>
          <div>
            <MonthlyReportCard 
              summary={monthlySummary} 
              loading={loading}
            />
          </div>
          
          <div>
            <CategoryReportCard 
              summary={categorySummary} 
              loading={loading}
            />
          </div>
        </ReportsGrid>
      </Content>
    </Container>
  )
}
