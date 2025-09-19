'use client'

import React from 'react'
import { styled } from 'styled-components'

interface PaginationButtonProps {
  page: number | string
  active?: boolean
  onClick: () => void
}

const Button = styled.button<{ $active?: boolean }>`
  padding: 0.5rem 1rem;
  border-radius: 6px;
  background-color: ${({ theme, $active }) => ($active ? theme.colors.primaryGreen : theme.colors.white)};
  color: ${({ theme, $active }) => ($active ? theme.colors.white : theme.colors.black)};
  font-weight: 500;
  cursor: ${({ disabled }) => (disabled ? 'default' : 'pointer')};
  border: none;
  transition: all 0.2s ease;

  &:hover {
    background-color: ${({ theme, $active, disabled }) =>
      disabled ? theme.colors.platinum : $active ? theme.colors.primaryGreen : theme.colors.mediumGrey};
  }
`;

export default function PaginationButton({ page, active = false, onClick }: PaginationButtonProps) {
  return (
    <Button
      disabled={page === '...'}
      $active={active}
      onClick={onClick}
    >
      {page}
    </Button>
  )
}
