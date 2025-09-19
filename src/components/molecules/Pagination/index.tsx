'use client'

import { MdKeyboardArrowRight, MdKeyboardArrowLeft } from "react-icons/md"
import { styled } from 'styled-components'
import PaginationButton from '@/components/atoms/PaginationButton'
import { useContext } from "react"
import { IsSidebarOnContext } from "@/context/IsSidebarOnContext"
import UseViewport from "@/hooks/UseViewport"

interface PaginationControlsProps {
  totalPages: number
  currentPage: number
  onPageChange: (page: number) => void
};

const PaginationWrapper = styled.div<{ $isCollapsed : boolean }>`
  display: flex;
  width: ${({ $isCollapsed }) => $isCollapsed ? '57%' : '60%'};
  justify-content: center;
  align-items: center;
  gap: .5rem; 
  transition: all .3s linear;

  @media (max-width: 1000px) {
    width: ${({ $isCollapsed }) => $isCollapsed ? '87%' : '94%'};
  }

  @media (max-width: 768px) {
    gap: 0;
    width: 100%;
  }
`;

const ArrowButton = styled.button<{ disabled?: boolean }>`
  display: flex;
  background: transparent;
  border: none;
  font-size: 1.5rem;
  color: ${({ theme, disabled }) => (disabled ? theme.colors.mediumGrey : theme.colors.black)};
  cursor: ${({ disabled }) => (disabled ? 'not-allowed' : 'pointer')};
`;

export default function PaginationControls({ totalPages, currentPage, onPageChange } : PaginationControlsProps) {
  const { isCollapsed } = useContext(IsSidebarOnContext)
  const viewport = UseViewport()

  const generatePages = () => {
    const pages: (number | string)[] = []
    const visibleNumbers = viewport ? 4 : 3 // Quantidade fixa de números no meio
    const totalVisible = visibleNumbers + 2 

    if (totalPages <= totalVisible) {
      for (let i = 1; i <= totalPages; i++) {
        pages.push(i)
      }
      return pages
    }

    pages.push(1)

    const half = Math.floor(visibleNumbers / 2)
    let start = currentPage - half
    let end = currentPage + half

    // Corrige quando o range estoura para o início
    if (start <= 2) {
      start = 2
      end = start + visibleNumbers - 1
    }

    // Corrige quando o range estoura para o fim
    if (end >= totalPages - 1) {
      end = totalPages - 1
      start = end - visibleNumbers + 1
    }

    if (start > 2) {
      pages.push('...')
    }

    for (let i = start; i <= end; i++) {
      pages.push(i)
    }

    if (end < totalPages - 1) {
      pages.push('...')
    }

    pages.push(totalPages)

    return pages
  }

  return (
    <PaginationWrapper $isCollapsed={isCollapsed}>
      <ArrowButton
        disabled={currentPage === 1}
        onClick={() => onPageChange(currentPage - 1)}
      >
        <MdKeyboardArrowLeft />
      </ArrowButton>

      {generatePages().map((page, index) => (
        <PaginationButton
          key={index}
          page={page}
          active={page === currentPage}
          onClick={() => typeof page === 'number' && onPageChange(page)}
        />
      ))}

      <ArrowButton
        disabled={currentPage === totalPages}
        onClick={() => onPageChange(currentPage + 1)}
      >
        <MdKeyboardArrowRight />
      </ArrowButton>
    </PaginationWrapper>
  )
}
