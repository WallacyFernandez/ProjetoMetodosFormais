'use client'

import React from 'react'
import { styled } from 'styled-components';

interface StatusBadgeProps {
  $status?: 'Finalizado' | 'Em-progresso' | 'Pendente';
};

const Container = styled.div<StatusBadgeProps>`
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
  background-color: ${({ theme }) => theme.colors.ghostWhite};
  color: ${({ theme, $status }) => {
    if ($status === 'Finalizado') return theme.colors.success;
    if ($status === 'Em-progresso') return theme.colors.primaryGreen;
    return theme.colors.error;
  }};
  border: none;
  border-radius: 15px;
  padding: 0.3rem 0.6rem;
  font-size: .9rem;

  @media (max-width: 768px) {
    font-size: .5rem;
      padding: .1rem .3rem;
  }
`;

const StatusDot = styled.span<StatusBadgeProps>`
  display: inline-block;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background-color: ${({ theme, $status }) => {
    if ($status === 'Finalizado') return theme.colors.success;
    if ($status === 'Em-progresso') return theme.colors.primaryGreen;
    return theme.colors.error;
  }};
`;

export default function StatusBadge({ $status }: StatusBadgeProps) {
  return (
    <Container $status={$status}>
      <StatusDot $status={$status} />
      {$status}
    </Container>
  )
}
