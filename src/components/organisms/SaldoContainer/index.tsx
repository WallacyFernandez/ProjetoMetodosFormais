'use client'

import React, { useContext, useEffect, useState } from 'react'
import { styled } from 'styled-components'
import { IsSidebarOnContext } from '@/context/IsSidebarOnContext'
import { 
  GetUserBalance, 
  AddToBalance, 
  SubtractFromBalance, 
  SetBalance, 
  ResetBalance,
  GetBalanceHistory 
} from '@/services/FinanceServices'
import type { UserBalance, BalanceHistory } from '@/types/finance'
import PageHeader from '@/components/molecules/PageHeader'
import BalanceCard from '@/components/molecules/BalanceManagementCard'
import BalanceHistoryTable from '@/components/molecules/BalanceHistoryTable'
import { toast } from 'react-toastify'

interface SaldoContainerProps {
  $isCollapsed: boolean;
}

const Container = styled.div<SaldoContainerProps>`
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

const Grid = styled.div`
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 2rem;
  margin-top: 2rem;

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
`;

export default function SaldoContainer() {
  const { isCollapsed } = useContext(IsSidebarOnContext)
  const [balance, setBalance] = useState<UserBalance | null>(null)
  const [history, setHistory] = useState<BalanceHistory[]>([])
  const [loading, setLoading] = useState(true)

  const loadData = async () => {
    try {
      setLoading(true)
      const [balanceData, historyData] = await Promise.all([
        GetUserBalance(),
        GetBalanceHistory()
      ])
      setBalance(balanceData)
      setHistory(historyData)
    } catch (error) {
      console.error('Erro ao carregar dados:', error)
      toast.error('Erro ao carregar dados do saldo')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadData()
  }, [])

  const handleAddBalance = async (amount: number, description: string) => {
    try {
      const updatedBalance = await AddToBalance({
        amount,
        description
      })
      setBalance(updatedBalance)
      await loadData() // Recarregar histórico
      toast.success('Valor adicionado ao saldo!')
    } catch (error) {
      console.error('Erro ao adicionar saldo:', error)
      toast.error('Erro ao adicionar saldo')
    }
  }

  const handleSubtractBalance = async (amount: number, description: string) => {
    try {
      const updatedBalance = await SubtractFromBalance({
        amount,
        description
      })
      setBalance(updatedBalance)
      await loadData() // Recarregar histórico
      toast.success('Valor subtraído do saldo!')
    } catch (error) {
      console.error('Erro ao subtrair saldo:', error)
      toast.error('Erro ao subtrair saldo')
    }
  }

  const handleSetBalance = async (amount: number, description: string) => {
    try {
      const updatedBalance = await SetBalance({
        amount,
        description
      })
      setBalance(updatedBalance)
      await loadData() // Recarregar histórico
      toast.success('Saldo definido com sucesso!')
    } catch (error) {
      console.error('Erro ao definir saldo:', error)
      toast.error('Erro ao definir saldo')
    }
  }

  const handleResetBalance = async () => {
    try {
      const updatedBalance = await ResetBalance()
      setBalance(updatedBalance)
      await loadData() // Recarregar histórico
      toast.success('Saldo resetado com sucesso!')
    } catch (error) {
      console.error('Erro ao resetar saldo:', error)
      toast.error('Erro ao resetar saldo')
    }
  }

  if (loading) {
    return (
      <Container $isCollapsed={isCollapsed}>
        <Content>
          <PageHeader $title="Gestão de Saldo" $subtitle="Gerencie seu saldo financeiro" />
          <div style={{ textAlign: 'center', padding: '2rem' }}>
            Carregando...
          </div>
        </Content>
      </Container>
    )
  }

  return (
    <Container $isCollapsed={isCollapsed}>
      <Content>
        <PageHeader 
          $title="Gestão de Saldo" 
          $subtitle="Gerencie seu saldo financeiro"
        />

        <Grid>
          <div>
            <BalanceCard
              balance={balance}
              onAdd={handleAddBalance}
              onSubtract={handleSubtractBalance}
              onSet={handleSetBalance}
              onReset={handleResetBalance}
            />
          </div>
          
          <div>
            <BalanceHistoryTable history={history} />
          </div>
        </Grid>
      </Content>
    </Container>
  )
}
