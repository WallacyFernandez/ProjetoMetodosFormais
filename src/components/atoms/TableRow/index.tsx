'use client'

import { IsSidebarOnContext } from '@/context/IsSidebarOnContext'
import { Project } from '@/types/GlobalTypes'
import React, { useContext, useEffect, useRef, useState } from 'react'
import { keyframes, styled } from 'styled-components'
import StatusBadge from '../StatusBadge'
import { FixedSizeList as List, ListChildComponentProps } from 'react-window';

const slideDown = keyframes`
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
`;

interface TableRowProps {
  items?: Project[],
  quantity?: number,
  $quantityRows?: number,
  $isCollapsed?: boolean,
  $isSent?: string
};

const Container = styled.ul<TableRowProps>`
  display: grid;
  list-style: none;
  grid-template-columns: repeat(5, 1fr); 
  align-items: center;
  gap: 0.5rem;
  table-layout: fixed;
  max-width: ${({ $isCollapsed, $quantityRows }) => {
  if ($isCollapsed && $quantityRows !== undefined) {
    return $quantityRows >= 3 ? '88.2%' : '87%';
  }
  if (!$isCollapsed && $quantityRows !== undefined) {
    return $quantityRows >= 3 ? '96.5%' : '95%'; 
  }
  return '95%'; 
}};
  background-color: ${({ theme }) => theme.colors.white};
  color: ${({ theme }) => theme.colors.darkText};
  border: 1px solid #0000002b;
  border-radius: 4px;
  margin-bottom: 1rem;
  padding: 1rem;
  animation: ${slideDown} .3s linear forwards;
  transition: all .3s ease-in-out;

  li {
    word-break: break-word;
    overflow-wrap: break-word;
    font-size: .9rem;
    text-align: center;
    pointer-events: ${({ $isCollapsed }) => $isCollapsed ? 'all' : 'none'};

    &:first-child {
      color: ${({ theme }) => theme.colors.black};
      text-align: left;

      @media (max-width: 768px) {
        text-align: center;
      }
    }

    @media (max-width: 768px) {
      font-size: .7rem;
    }
  }

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

const SubmissionCell = styled.li<TableRowProps>`
  color: ${({ theme, $isSent }) => $isSent === 'Enviado' ? theme.colors.mediumGrey : theme.colors.darkText};

  @media (max-width: 768px) {
    font-size: .7rem;
  }
`;

export default function TableRow({ items, quantity, $quantityRows }: TableRowProps) {
  const [ quantityRows, setQuantityRows ] = useState<number>(1)
  const { isCollapsed } = useContext(IsSidebarOnContext)
  const containerRef = useRef<HTMLDivElement | null>(null)
  const [ listHeight, setListHeight ] = useState<number>(240)

  useEffect(() => {
    setQuantityRows(quantity ?? 1)
  }, [quantity])

  useEffect(() => {
    const updateHeight = () => {
      if (containerRef.current) {
        const h = containerRef.current.clientHeight
        if (h && h > 0) setListHeight(h)
      }
    }
    updateHeight()
    window.addEventListener('resize', updateHeight)
    return () => window.removeEventListener('resize', updateHeight)
  }, [])

  if (!items) return null
  
  const row = ({index, style} : ListChildComponentProps) => {
    const el = items[index]

    return (
      <div style={style}>
        <Container key={el.id} $isCollapsed={isCollapsed} $quantityRows={quantityRows}>
          <li>{el.title}</li>
          <li>{el.description}</li>
          <li>{new Date(el.endDate).toLocaleDateString('pt-BR', {
            day: 'numeric',
            month: 'long',
            year: 'numeric'
          })}</li>
          <StatusBadge $status={el.status} />
          <SubmissionCell $isSent={el.submission}>{el.submission}</SubmissionCell>
        </Container>
      </div>
    )
  }

  return (
    <>
      <div ref={containerRef} style={{ height: '100%' }}>
        <List 
          height={listHeight}
          itemCount={items.length} 
          itemSize={80} 
          overscanCount={3}
          width="100%">
          {row}
        </List>
      </div>
    </>
  )
}
