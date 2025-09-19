'use client'

import Logo from '@/components/atoms/Logo'
import React, { useContext, useState } from 'react'
import { keyframes, styled } from 'styled-components'
import { MdKeyboardArrowRight, MdKeyboardArrowLeft, MdMenu } from "react-icons/md";
import { PiHandWaving } from "react-icons/pi";
import UserAvatar from '@/components/atoms/UserAvatar';
import { IsSidebarOnContext } from '@/context/IsSidebarOnContext';
import UseViewport from '@/hooks/UseViewport';
import NavItem from '@/components/atoms/NavItem';
import UserProfile from '@/components/molecules/UserProfile';

interface ContainerSidebarProp {
  $isCollapsed: boolean
}

const ContainerSidebar = styled.div<ContainerSidebarProp>`
  position: absolute;
  top: 0;
  height: 100%;
  width: 100%;
  max-width: ${({ $isCollapsed }) => ($isCollapsed ? '0rem' : '16rem')};
  background-color: ${({ theme }) => theme.colors.primaryGreen};
  border-top-right-radius: 15px;
  border-bottom-right-radius: 15px;
  overflow: hidden;
  z-index: 4;
  transition: max-width 0.3s ease-in-out;
`;

const ToogleContainerSidebar = styled.div<ContainerSidebarProp>`
  position: absolute;
  left: ${({ $isCollapsed }) => ($isCollapsed ? '8px' : '243px')};
  top: 20px;
  z-index: 5;
  transition: left 0.3s ease-in-out;

  div {
    background-color: ${({ theme }) => theme.colors.white};
    border-radius: 50%;
    height: 24px;
    width: 24px;
    text-align: center;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;

    svg {
      height: 22px;
      width: 22px;
      transition: transform 0.3s ease-in-out;
    }
  }
`;

const HeaderSidebar = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  width: 90%;
  gap: ${({ theme }) => theme.spacing.xs};
  margin-top: ${({ theme }) => theme.spacing.sm};

  h3 {
    color: ${({ theme }) => theme.colors.white};
  }
`;

const MainSidebar = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  height: 100%;
  margin-top: ${({ theme }) => theme.spacing.xxl};

  ul {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 85%;
    list-style: none;
    gap: 16px;
  }
`;

const FooterSidebar = styled.div`
  position: absolute;
  width: 100%;
  border-top: 1px solid ${({ theme }) => theme.colors.white};
  bottom: 0;
  cursor: pointer;
`;

const FooterContainer = styled.div`
  display: flex;
  align-items: center;
  gap: .7rem;
  padding: 1.2rem;
 
  svg {
    height: 34px;
    width: 34px;
    color: ${({ theme }) => theme.colors.white};
  } 
`;

export default function SideBar() {
  const { isCollapsed, setIsCollapsed} = useContext(IsSidebarOnContext)
  const viewport = UseViewport()

  const handleSidebar = () => {
    setIsCollapsed(prev => !prev)
  }

  return (
    <>
      <ToogleContainerSidebar $isCollapsed={isCollapsed}>
        <div onClick={handleSidebar}>
          {viewport ? (
            <>
              {isCollapsed ? <MdKeyboardArrowRight /> : <MdKeyboardArrowLeft />}
            </>
          ) : (
            <>
              <MdMenu />
            </>
          )}
        </div>
      </ToogleContainerSidebar>
      <ContainerSidebar $isCollapsed={isCollapsed}>

        <HeaderSidebar>
          <Logo variant='white' width={70} height={60} />
          <h3>CashLab</h3>
        </HeaderSidebar>

        <MainSidebar>
          <NavItem />
        </MainSidebar>

        <FooterSidebar>
          <FooterContainer>
            <UserProfile />
            <MdKeyboardArrowRight />
          </FooterContainer>
        </FooterSidebar>
      </ContainerSidebar>
    
    </>
  );
}
