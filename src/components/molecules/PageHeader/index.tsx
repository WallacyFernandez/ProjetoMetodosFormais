'use client'

import { ButtonsConfig } from '@/types/GlobalTypes';
import Button from '@/components/atoms/Button';
import { IsSidebarOnContext } from '@/context/IsSidebarOnContext';
import React, { useContext } from 'react'
import { styled } from 'styled-components'
import UseViewport from '@/hooks/UseViewport';

interface PageHeaderProps {
  $title?: string,
  $buttons?: ButtonsConfig[],
  $isCollapsed?: boolean
};

const Container = styled.div`
  display: flex;
  position: relative;
  top: 2rem;
  align-items: center;
  width: 100%;
  transition: top .3s linear;

  h2  {
    font-size: 1.6rem;
  }

  @media (max-width: 768px) {
    top: 3rem;
  }
`;

const ContainerButtons = styled.div<PageHeaderProps>`
  display: flex;
  justify-content: flex-end;
  width: 100%;
  gap: .5rem;
  margin-right: ${({ $isCollapsed }) => $isCollapsed ? '7rem' : '6rem'};
  transition: all .3s ease-in-out;

  @media (max-width: 860px) {
    margin-right: ${({ $isCollapsed }) => $isCollapsed ? '3rem' : '1rem'};
  }
 
  @media (max-width: 768px) {
    margin-right: 0;
  }
`;

export default function PageHeader({ $title, $buttons} : PageHeaderProps) {
  const { isCollapsed } = useContext(IsSidebarOnContext)
  const viewport = UseViewport()

  return (
    <Container>
      <h2>{$title}</h2>
      <ContainerButtons $isCollapsed={isCollapsed}>
          {$buttons?.map((el) => (
            <Button onClick={el.action()} key={el.titleBtn} variant={el.type} disabled={!isCollapsed && !viewport}>
              {el.titleBtn}
            </Button>
          ))}
      </ContainerButtons>
    </Container>
  )
}

