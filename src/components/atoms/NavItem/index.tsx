'use client'

import React, { useState } from 'react'
import { styled } from 'styled-components';
import { MdOutlineDashboardCustomize, MdHome } from "react-icons/md";

interface RouteListProps {
  $active: boolean;
};

const RouteList = styled.li<RouteListProps>`
  display: flex;
  justify-content: flex-start;
  align-items: center;
  background-color: ${({ theme, $active }) => $active ? theme.colors.white : 'transparent'};
  color: ${({ theme, $active }) => $active ? theme.colors.black : theme.colors.white};
  width: 100%;
  gap: 16px;
  padding: 8px 8px 8px 14px;
  border-radius: 20px;
  cursor: pointer;

  svg {
    height: 20px;
    width: 20px;
  }
`;

const Items = ['Dashboard', 'Example1', 'Example2', 'Example3']

export default function NavItem() {
  const [ highlightedRoute, setHighlightedRoute ] = useState<string>('Dashboard');
  
  return (
    <ul>
      {Items.map((el) => (
        <RouteList
          key={el}
          $active={highlightedRoute === el}
          onClick={() => setHighlightedRoute(el)} 
        >
          <span>{el === 'Dashboard' ? <MdOutlineDashboardCustomize /> : <MdHome />}</span> {el}
        </RouteList>
      ))}
    </ul>
  )
}