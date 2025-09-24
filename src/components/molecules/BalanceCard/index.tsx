'use client'

import React from 'react'
import { styled } from 'styled-components'
import { MdAccountBalance, MdTrendingUp, MdTrendingDown } from 'react-icons/md'

interface BalanceCardProps {
  balance: number;
}

const Card = styled.div`
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  padding: 2rem;
  color: white;
  box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -50%;
    width: 100%;
    height: 100%;
    background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
    pointer-events: none;
  }
`;

const Header = styled.div`
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
`;

const IconContainer = styled.div`
  background: rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  padding: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
`;

const Title = styled.h3`
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0;
  opacity: 0.9;
`;

const BalanceAmount = styled.div`
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
`;

const BalanceLabel = styled.div`
  font-size: 0.9rem;
  opacity: 0.8;
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

export default function BalanceCard({ balance }: BalanceCardProps) {
  const isPositive = balance >= 0
  
  return (
    <Card>
      <Header>
        <IconContainer>
          <MdAccountBalance size={24} />
        </IconContainer>
        <Title>Saldo Atual</Title>
      </Header>
      
      <BalanceAmount>
        {formatCurrency(balance)}
      </BalanceAmount>
      
      <BalanceLabel>
        {isPositive ? (
          <>
            <MdTrendingUp size={16} />
            Saldo positivo
          </>
        ) : (
          <>
            <MdTrendingDown size={16} />
            Saldo negativo
          </>
        )}
      </BalanceLabel>
    </Card>
  )
}
