'use client'

import { IsSidebarOnContext } from '@/context/IsSidebarOnContext'
import React, { useContext } from 'react'
import { styled } from 'styled-components'

interface TableHeaderProps {
  TitleElements?: string[],
  $isCollapsed?: boolean
};

const Container = styled.ul<TableHeaderProps>`
  display: grid;
  list-style: none; 
  max-width: ${({ $isCollapsed }) => $isCollapsed ? '87%' : '95%'};
  grid-template-columns: 1fr 1fr 1fr 1fr 1fr;
  font-weight: 700;
  text-align: center;
  background-color: ${({ theme }) => theme.colors.paleGrey};
  color: ${({ theme }) => theme.colors.mediumGrey};
  border: 1px solid #0000002b;
  border-radius: 4px;
  padding: 1rem;
  margin: 1rem 0;
  transition: all .3s ease-in-out;

  @media (max-width: 870px) {
    max-width: 95%;
  }

  @media (max-width: 860px) {
    max-width: 97%;
  }

  @media (max-width: 834px) {
    max-width: 99%;
  }

  @media (max-width: 768px) {
    max-width: 100%;
  }
`;

export default function TableHeader({ TitleElements }: TableHeaderProps) {
  const { isCollapsed } = useContext(IsSidebarOnContext)

  return (
    <Container $isCollapsed={isCollapsed}>
        {TitleElements && TitleElements.map((el) => (
          <li key={el}>{el}</li>
        ))}
    </Container>
  )
}
