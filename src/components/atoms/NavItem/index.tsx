'use client'

import React, { useState, useEffect } from 'react'
import { useRouter, usePathname } from 'next/navigation'
import { styled } from 'styled-components';
import { 
  MdOutlineDashboardCustomize, 
  MdReceipt, 
  MdAccountBalance, 
  MdCategory, 
  MdBarChart,
  MdGamepad,
  MdShoppingCart
} from "react-icons/md";

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
  transition: all 0.2s ease;

  &:hover {
    background-color: ${({ theme, $active }) => $active ? theme.colors.white : 'rgba(255, 255, 255, 0.1)'};
  }

  svg {
    height: 20px;
    width: 20px;
  }
`;

interface NavItem {
  name: string;
  icon: React.ReactNode;
  path: string;
}

const Items: NavItem[] = [
  { name: 'Dashboard', icon: <MdOutlineDashboardCustomize />, path: '/dashboard' },
  { name: 'Jogo', icon: <MdGamepad />, path: '/jogo' },
  { name: 'Estoque', icon: <MdShoppingCart />, path: '/estoque' },
  { name: 'Transações', icon: <MdReceipt />, path: '/transacoes' },
  { name: 'Saldo', icon: <MdAccountBalance />, path: '/saldo' },
  { name: 'Categorias', icon: <MdCategory />, path: '/categorias' },
  { name: 'Relatórios', icon: <MdBarChart />, path: '/relatorios' }
];

export default function NavItem() {
  const router = useRouter()
  const pathname = usePathname()
  const [ highlightedRoute, setHighlightedRoute ] = useState<string>('Dashboard');

  // Atualiza o item ativo baseado na rota atual
  useEffect(() => {
    const currentItem = Items.find(item => item.path === pathname)
    if (currentItem) {
      setHighlightedRoute(currentItem.name)
    }
  }, [pathname])

  const handleNavigation = (item: NavItem) => {
    setHighlightedRoute(item.name)
    router.push(item.path)
  }
  
  return (
    <ul>
      {Items.map((item) => (
        <RouteList
          key={item.name}
          $active={highlightedRoute === item.name}
          onClick={() => handleNavigation(item)} 
        >
          <span>{item.icon}</span> {item.name}
        </RouteList>
      ))}
    </ul>
  )
}