'use client'

import React, { useEffect } from 'react'
import TableHeader from '@/components/atoms/TableHeader'
import TableRow from '@/components/atoms/TableRow'
import { styled } from 'styled-components'
import { Project } from '@/types/GlobalTypes'

interface ProjectTableProps {
  quantityOfRows: number,
  currentItems: Project[],
  onLoaded: () => void
};

const TitleElements = ['Título', 'Exemplo', 'Data Final', 'Status', 'Envio']

const Container = styled.div`
  height: 100%;
  margin-top: 4rem;
`;

const RowsWrapper = styled.div`
  height: 55vh;
`;

export default function ProjectTable({ quantityOfRows, currentItems, onLoaded } : ProjectTableProps) {
  
  /* Quando montar, coloca o state para true */
  useEffect(() => {
    onLoaded()
  }, [])

  return (
    <Container>
      <TableHeader TitleElements={TitleElements} />
      <RowsWrapper>
        <TableRow items={currentItems} quantity={quantityOfRows} />
      </RowsWrapper>
    </Container>
  )
}