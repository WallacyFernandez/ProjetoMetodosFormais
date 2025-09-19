'use client'

import React, { useCallback, useContext, useEffect, useState } from 'react'
import PageHeader from '@/components/molecules/PageHeader'
import { keyframes, styled } from 'styled-components'
import { ButtonsConfig } from '@/types/GlobalTypes'
import { IsSidebarOnContext } from '@/context/IsSidebarOnContext'
import Pagination from '@/components/molecules/Pagination'
import { MdOutlineKeyboardArrowDown } from "react-icons/md";
import dynamic from 'next/dynamic'

const LoadingDiv = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 300px;
  width: 100%;
`

const ProjectTable = dynamic(() => import('@/components/molecules/ProjectTable'), {
  ssr: false,
  loading: () => (
    <LoadingDiv>Carregando...</LoadingDiv>
  )
})


const modalFilterRowsOpen = keyframes`
  from {
    height: 0;
  }
  to {
    height: 100px;
  }
`;

const modalFilterRowsClose = keyframes`
  from {
    height: 100px;
  }
  to {
    height: 0;
  }
`;

interface ProjectsSectionProps {
  $isCollapsed: boolean
};

interface ModalFilterRowsProps {
  $filterRowsModal: boolean
};

const Wrapper = styled.div`
  /* display: flex;
  justify-content: center;

  flex-direction: column;
  width: 100%; */
`

const Container = styled.div<ProjectsSectionProps>`
  background-color: ${({ theme }) => theme.colors.backgroundSecondary};
  margin-left: ${({ $isCollapsed }) => $isCollapsed ? '10rem' : '20rem'};
  transition: all .3s ease-in-out;

  @media (max-width: 1000px) {
    margin-left: ${({ $isCollapsed }) => $isCollapsed ? '7rem' : '18rem'};
  }

  @media (max-width: 834px) {
    margin-left: ${({ $isCollapsed }) => $isCollapsed ? '3rem' : '17rem'};
  }

  @media (max-width: 768px) {
    margin-left: .3rem;
    margin-right: .3rem;
  }
`;

const WrapperFilterAndPagination = styled.div`
  display: flex;
  width: 100%;
  margin: 1.5rem 0;

  @media (max-width: 1000px) {
    flex-direction: column;
    gap: 2rem;
  }
`;

const ContainerFilterRows = styled.div`
  display: flex;
  position: relative;
  justify-content: flex-start;
  align-items: center;
  transition: all .3s ease-in-out;
`;

const FilterRowsContainerBlock = styled.span<ModalFilterRowsProps>`
  display: flex;
  position: relative;
  justify-content: center;
  align-items: center;
  height: 40px;
  width: 4rem;
  text-align: center;
  border: 1px solid #0000002b;
  border-radius: 5px;
  margin: 0 .5rem 0 .5rem;
  cursor: pointer;

  svg {
    height: 22px;
    width: 22px;
    transition: transform 0.5s ease;
    transform: ${({ $filterRowsModal }) => $filterRowsModal ? 'rotate(180deg)' : 'rotate(0deg)'};
  }

`;

const ModalFilterRows = styled.div<ModalFilterRowsProps>`
  position: absolute;
  top: 100%;
  width: 4rem;
  background-color: ${({ theme }) => theme.colors.white};
  overflow-y: scroll;
  border: 1px solid #0000002b;
  animation: ${({ $filterRowsModal }) => $filterRowsModal ? modalFilterRowsOpen : modalFilterRowsClose} .5s ease forwards;

  p {
    margin-bottom: .7rem;
    cursor: pointer;

    &:first-child {
      margin-top: .3rem;
    }
  }
`;

export default function ProjectsSection()  {
  const [ filterRowsModal, setFilterRowsModal ] = useState<boolean>(false)
  const [ quantityOfRows, setQuantityOfRows ] = useState<number>(10)
  const [ rowsPerPage, setRowsPerPage ] = useState(quantityOfRows)
  const [ currentPage, setCurrentPage ] = useState(1)
  const [ isTableLoaded, setIsTableLoaded ] = useState(false)
  const { isCollapsed } = useContext(IsSidebarOnContext)
    
  const toogleModalFilterRows = () => {
    setFilterRowsModal(prev => !prev)
  }
  
  const handleQuantityOfRows = (qnt: number) => {
    setQuantityOfRows(Math.max(10, qnt))
  }

  const handleNewProject = () => {
    console.log("Novo projeto")
  }

  const buttonsConfig: ButtonsConfig[] = [
    {
      titleBtn: 'Novo projeto',
      type: 'primary',
      action: () => () => handleNewProject()
    }
  ]

  const projectValues = [
  { id: '1', title: 'Projeto1', description: 'Descrição do Projeto 1', endDate: new Date('2025-09-15'), status: 'Pendente' as const, submission: 'Carregar' as const },
  { id: '2', title: 'Projeto2', description: 'Descrição do Projeto 2', endDate: new Date('2025-10-01'), status: 'Em-progresso' as const, submission: 'Carregar' as const },
  { id: '3', title: 'Projeto3', description: 'Descrição do Projeto 3', endDate: new Date('2025-09-30'), status: 'Pendente' as const, submission: 'Carregar' as const },
  { id: '4', title: 'Projeto4', description: 'Descrição do Projeto 4', endDate: new Date('2025-09-20'), status: 'Finalizado' as const, submission: 'Enviado' as const },
  { id: '5', title: 'Projeto5', description: 'Descrição do Projeto 5', endDate: new Date('2025-08-15'), status: 'Finalizado' as const, submission: 'Enviado' as const },
  { id: '6', title: 'Projeto6', description: 'Descrição do Projeto 6', endDate: new Date('2025-07-15'), status: 'Finalizado' as const, submission: 'Enviado' as const },
  { id: '7', title: 'Projeto7', description: 'Descrição do Projeto 7', endDate: new Date('2025-09-10'), status: 'Pendente' as const, submission: 'Carregar' as const },
  { id: '8', title: 'Projeto8', description: 'Descrição do Projeto 8', endDate: new Date('2025-09-25'), status: 'Em-progresso' as const, submission: 'Carregar' as const },
  { id: '9', title: 'Projeto9', description: 'Descrição do Projeto 9', endDate: new Date('2025-09-18'), status: 'Pendente' as const, submission: 'Carregar' as const },
  { id: '10', title: 'Projeto10', description: 'Descrição do Projeto 10', endDate: new Date('2025-10-05'), status: 'Em-progresso' as const, submission: 'Carregar' as const },
  { id: '11', title: 'Projeto11', description: 'Descrição do Projeto 11', endDate: new Date('2025-10-25'), status: 'Finalizado' as const, submission: 'Enviado' as const },
  { id: '12', title: 'Projeto12', description: 'Descrição do Projeto 12', endDate: new Date('2025-09-12'), status: 'Finalizado' as const, submission: 'Enviado' as const },
  { id: '13', title: 'Projeto13', description: 'Descrição do Projeto 13', endDate: new Date('2025-09-17'), status: 'Finalizado' as const, submission: 'Enviado' as const },
  { id: '14', title: 'Projeto14', description: 'Descrição do Projeto 14', endDate: new Date('2025-08-10'), status: 'Em-progresso' as const, submission: 'Carregar' as const },
  { id: '15', title: 'Projeto15', description: 'Descrição do Projeto 15', endDate: new Date('2025-09-10'), status: 'Pendente' as const, submission: 'Carregar' as const },
  { id: '16', title: 'Projeto16', description: 'Descrição do Projeto 16', endDate: new Date('2025-09-30'), status: 'Finalizado' as const, submission: 'Enviado' as const },
  { id: '17', title: 'Projeto17', description: 'Descrição do Projeto 17', endDate: new Date('2025-09-14'), status: 'Finalizado' as const, submission: 'Enviado' as const },
  { id: '18', title: 'Projeto18', description: 'Descrição do Projeto 18', endDate: new Date('2025-08-05'), status: 'Finalizado' as const, submission: 'Enviado' as const },
  { id: '19', title: 'Projeto19', description: 'Descrição do Projeto 19', endDate: new Date('2025-07-25'), status: 'Em-progresso' as const, submission: 'Carregar' as const },
  { id: '20', title: 'Projeto20', description: 'Descrição do Projeto 20', endDate: new Date('2025-09-01'), status: 'Pendente' as const, submission: 'Carregar' as const },
  { id: '21', title: 'Projeto21', description: 'Descrição do Projeto 21', endDate: new Date('2025-09-05'), status: 'Finalizado' as const, submission: 'Enviado' as const },
  { id: '22', title: 'Projeto22', description: 'Descrição do Projeto 22', endDate: new Date('2025-10-15'), status: 'Finalizado' as const, submission: 'Enviado' as const },
  { id: '23', title: 'Projeto23', description: 'Descrição do Projeto 23', endDate: new Date('2025-10-10'), status: 'Pendente' as const, submission: 'Carregar' as const },
  { id: '24', title: 'Projeto24', description: 'Descrição do Projeto 24', endDate: new Date('2025-09-20'), status: 'Em-progresso' as const, submission: 'Carregar' as const },
  { id: '25', title: 'Projeto25', description: 'Descrição do Projeto 25', endDate: new Date('2025-09-22'), status: 'Finalizado' as const, submission: 'Enviado' as const },
  { id: '26', title: 'Projeto26', description: 'Descrição do Projeto 26', endDate: new Date('2025-08-25'), status: 'Em-progresso' as const, submission: 'Carregar' as const },
  { id: '27', title: 'Projeto27', description: 'Descrição do Projeto 27', endDate: new Date('2025-09-28'), status: 'Finalizado' as const, submission: 'Enviado' as const },
  { id: '28', title: 'Projeto28', description: 'Descrição do Projeto 28', endDate: new Date('2025-08-12'), status: 'Finalizado' as const, submission: 'Enviado' as const },
  { id: '29', title: 'Projeto29', description: 'Descrição do Projeto 29', endDate: new Date('2025-10-20'), status: 'Pendente' as const, submission: 'Carregar' as const },
  { id: '30', title: 'Projeto30', description: 'Descrição do Projeto 30', endDate: new Date('2025-09-12'), status: 'Em-progresso' as const, submission: 'Carregar' as const },
  { id: '31', title: 'Projeto31', description: 'Descrição do Projeto 31', endDate: new Date('2025-09-15'), status: 'Finalizado' as const, submission: 'Enviado' as const },
  { id: '32', title: 'Projeto32', description: 'Descrição do Projeto 32', endDate: new Date('2025-09-25'), status: 'Finalizado' as const, submission: 'Enviado' as const },
  { id: '33', title: 'Projeto33', description: 'Descrição do Projeto 33', endDate: new Date('2025-08-22'), status: 'Pendente' as const, submission: 'Carregar' as const },
  { id: '34', title: 'Projeto34', description: 'Descrição do Projeto 34', endDate: new Date('2025-09-29'), status: 'Em-progresso' as const, submission: 'Carregar' as const },
  { id: '35', title: 'Projeto35', description: 'Descrição do Projeto 35', endDate: new Date('2025-08-30'), status: 'Em-progresso' as const, submission: 'Carregar' as const },
  { id: '36', title: 'Projeto36', description: 'Descrição do Projeto 36', endDate: new Date('2025-09-18'), status: 'Pendente' as const, submission: 'Carregar' as const },
  { id: '37', title: 'Projeto37', description: 'Descrição do Projeto 37', endDate: new Date('2025-08-17'), status: 'Em-progresso' as const, submission: 'Carregar' as const },
  { id: '38', title: 'Projeto38', description: 'Descrição do Projeto 38', endDate: new Date('2025-10-02'), status: 'Finalizado' as const, submission: 'Enviado' as const },
  { id: '39', title: 'Projeto39', description: 'Descrição do Projeto 39', endDate: new Date('2025-09-13'), status: 'Pendente' as const, submission: 'Carregar' as const },
  { id: '40', title: 'Projeto40', description: 'Descrição do Projeto 40', endDate: new Date('2025-08-09'), status: 'Finalizado' as const, submission: 'Enviado' as const },
  /* Again */
   { id: '1', title: 'Projeto1', description: 'Descrição do Projeto 1', endDate: new Date('2025-09-15'), status: 'Pendente' as const, submission: 'Carregar' as const },
  { id: '2', title: 'Projeto2', description: 'Descrição do Projeto 2', endDate: new Date('2025-10-01'), status: 'Em-progresso' as const, submission: 'Carregar' as const },
  { id: '3', title: 'Projeto3', description: 'Descrição do Projeto 3', endDate: new Date('2025-09-30'), status: 'Pendente' as const, submission: 'Carregar' as const },
  { id: '4', title: 'Projeto4', description: 'Descrição do Projeto 4', endDate: new Date('2025-09-20'), status: 'Finalizado' as const, submission: 'Enviado' as const },
  { id: '5', title: 'Projeto5', description: 'Descrição do Projeto 5', endDate: new Date('2025-08-15'), status: 'Finalizado' as const, submission: 'Enviado' as const },
  { id: '6', title: 'Projeto6', description: 'Descrição do Projeto 6', endDate: new Date('2025-07-15'), status: 'Finalizado' as const, submission: 'Enviado' as const },
  { id: '7', title: 'Projeto7', description: 'Descrição do Projeto 7', endDate: new Date('2025-09-10'), status: 'Pendente' as const, submission: 'Carregar' as const },
  { id: '8', title: 'Projeto8', description: 'Descrição do Projeto 8', endDate: new Date('2025-09-25'), status: 'Em-progresso' as const, submission: 'Carregar' as const },
  { id: '9', title: 'Projeto9', description: 'Descrição do Projeto 9', endDate: new Date('2025-09-18'), status: 'Pendente' as const, submission: 'Carregar' as const },
  { id: '10', title: 'Projeto10', description: 'Descrição do Projeto 10', endDate: new Date('2025-10-05'), status: 'Em-progresso' as const, submission: 'Carregar' as const },
  { id: '11', title: 'Projeto11', description: 'Descrição do Projeto 11', endDate: new Date('2025-10-25'), status: 'Finalizado' as const, submission: 'Enviado' as const },
  { id: '12', title: 'Projeto12', description: 'Descrição do Projeto 12', endDate: new Date('2025-09-12'), status: 'Finalizado' as const, submission: 'Enviado' as const },
  { id: '13', title: 'Projeto13', description: 'Descrição do Projeto 13', endDate: new Date('2025-09-17'), status: 'Finalizado' as const, submission: 'Enviado' as const },
  { id: '14', title: 'Projeto14', description: 'Descrição do Projeto 14', endDate: new Date('2025-08-10'), status: 'Em-progresso' as const, submission: 'Carregar' as const },
  { id: '15', title: 'Projeto15', description: 'Descrição do Projeto 15', endDate: new Date('2025-09-10'), status: 'Pendente' as const, submission: 'Carregar' as const },
  { id: '16', title: 'Projeto16', description: 'Descrição do Projeto 16', endDate: new Date('2025-09-30'), status: 'Finalizado' as const, submission: 'Enviado' as const },
  { id: '17', title: 'Projeto17', description: 'Descrição do Projeto 17', endDate: new Date('2025-09-14'), status: 'Finalizado' as const, submission: 'Enviado' as const },
  { id: '18', title: 'Projeto18', description: 'Descrição do Projeto 18', endDate: new Date('2025-08-05'), status: 'Finalizado' as const, submission: 'Enviado' as const },
  { id: '19', title: 'Projeto19', description: 'Descrição do Projeto 19', endDate: new Date('2025-07-25'), status: 'Em-progresso' as const, submission: 'Carregar' as const },
  { id: '20', title: 'Projeto20', description: 'Descrição do Projeto 20', endDate: new Date('2025-09-01'), status: 'Pendente' as const, submission: 'Carregar' as const },
  { id: '21', title: 'Projeto21', description: 'Descrição do Projeto 21', endDate: new Date('2025-09-05'), status: 'Finalizado' as const, submission: 'Enviado' as const },
  { id: '22', title: 'Projeto22', description: 'Descrição do Projeto 22', endDate: new Date('2025-10-15'), status: 'Finalizado' as const, submission: 'Enviado' as const },
  { id: '23', title: 'Projeto23', description: 'Descrição do Projeto 23', endDate: new Date('2025-10-10'), status: 'Pendente' as const, submission: 'Carregar' as const },
  { id: '24', title: 'Projeto24', description: 'Descrição do Projeto 24', endDate: new Date('2025-09-20'), status: 'Em-progresso' as const, submission: 'Carregar' as const },
  { id: '25', title: 'Projeto25', description: 'Descrição do Projeto 25', endDate: new Date('2025-09-22'), status: 'Finalizado' as const, submission: 'Enviado' as const },
  { id: '26', title: 'Projeto26', description: 'Descrição do Projeto 26', endDate: new Date('2025-08-25'), status: 'Em-progresso' as const, submission: 'Carregar' as const },
  { id: '27', title: 'Projeto27', description: 'Descrição do Projeto 27', endDate: new Date('2025-09-28'), status: 'Finalizado' as const, submission: 'Enviado' as const },
  { id: '28', title: 'Projeto28', description: 'Descrição do Projeto 28', endDate: new Date('2025-08-12'), status: 'Finalizado' as const, submission: 'Enviado' as const },
  { id: '29', title: 'Projeto29', description: 'Descrição do Projeto 29', endDate: new Date('2025-10-20'), status: 'Pendente' as const, submission: 'Carregar' as const },
  { id: '30', title: 'Projeto30', description: 'Descrição do Projeto 30', endDate: new Date('2025-09-12'), status: 'Em-progresso' as const, submission: 'Carregar' as const },
  { id: '31', title: 'Projeto31', description: 'Descrição do Projeto 31', endDate: new Date('2025-09-15'), status: 'Finalizado' as const, submission: 'Enviado' as const },
  { id: '32', title: 'Projeto32', description: 'Descrição do Projeto 32', endDate: new Date('2025-09-25'), status: 'Finalizado' as const, submission: 'Enviado' as const },
  { id: '33', title: 'Projeto33', description: 'Descrição do Projeto 33', endDate: new Date('2025-08-22'), status: 'Pendente' as const, submission: 'Carregar' as const },
  { id: '34', title: 'Projeto34', description: 'Descrição do Projeto 34', endDate: new Date('2025-09-29'), status: 'Em-progresso' as const, submission: 'Carregar' as const },
  { id: '35', title: 'Projeto35', description: 'Descrição do Projeto 35', endDate: new Date('2025-08-30'), status: 'Em-progresso' as const, submission: 'Carregar' as const },
  { id: '36', title: 'Projeto36', description: 'Descrição do Projeto 36', endDate: new Date('2025-09-18'), status: 'Pendente' as const, submission: 'Carregar' as const },
  { id: '37', title: 'Projeto37', description: 'Descrição do Projeto 37', endDate: new Date('2025-08-17'), status: 'Em-progresso' as const, submission: 'Carregar' as const },
  { id: '38', title: 'Projeto38', description: 'Descrição do Projeto 38', endDate: new Date('2025-10-02'), status: 'Finalizado' as const, submission: 'Enviado' as const },
  { id: '39', title: 'Projeto39', description: 'Descrição do Projeto 39', endDate: new Date('2025-09-13'), status: 'Pendente' as const, submission: 'Carregar' as const },
  { id: '40', title: 'Projeto40', description: 'Descrição do Projeto 40', endDate: new Date('2025-08-09'), status: 'Finalizado' as const, submission: 'Enviado' as const }
  ]

  const totalPages = Math.ceil(projectValues.length / rowsPerPage)
  const startIndex = (currentPage - 1) * rowsPerPage
  const endIndex = startIndex + rowsPerPage
  const currentItems = projectValues.slice(startIndex, endIndex)

  const handlePageChange = useCallback((page: number) => {
    if (page > 0 && page <= totalPages) {
      setCurrentPage(page);
    }
  }, [totalPages])


  useEffect(() => {
    setRowsPerPage(quantityOfRows)
    setCurrentPage(1) 
  }, [quantityOfRows])

  return (
    <Container $isCollapsed={isCollapsed}>
      <Wrapper>
        <PageHeader $title='Projetos' $buttons={buttonsConfig} />
        <ProjectTable quantityOfRows={rowsPerPage} currentItems={currentItems} onLoaded={() => setIsTableLoaded(true)} />

        {/* Modal para filtrar as linhas da tabela junto com a Pagination */}
        {isTableLoaded && (
          <WrapperFilterAndPagination>
            <ContainerFilterRows>
              Mostrar
              <FilterRowsContainerBlock $filterRowsModal={filterRowsModal} onClick={toogleModalFilterRows}>
                {quantityOfRows} <MdOutlineKeyboardArrowDown />
                {filterRowsModal && (
                  <ModalFilterRows $filterRowsModal={filterRowsModal}>
                    {Array.from({ length: 41 }, (_, index) => 10 + index).map((value) => (
                      <p key={value} onClick={() => handleQuantityOfRows(value)}>
                        {value}
                      </p>
                    ))}
                  </ModalFilterRows>
                )}
              </FilterRowsContainerBlock>
              <span>linha</span>
            </ContainerFilterRows>
          
            <Pagination totalPages={totalPages} currentPage={currentPage} onPageChange={handlePageChange}  /> 
          </WrapperFilterAndPagination>
        )}
      </Wrapper>
    </Container>
  )
}

