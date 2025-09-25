'use client'

import GameDashboard from '@/components/organisms/GameDashboard'
import SideBar from '@/components/organisms/Sidebar'
import React, { useEffect } from 'react'
import { styled } from 'styled-components'
import { toast } from 'react-toastify'

const Container = styled.div`
  min-height: 100%;
  padding-bottom: 5rem;
  margin: auto;
`;

export default function GamePage() {
  useEffect(() => {
    if (typeof window === 'undefined') return
    const justLoggedIn = sessionStorage.getItem('justLoggedIn')
    if (justLoggedIn) {
      sessionStorage.removeItem('justLoggedIn')
      toast.success('Bem-vindo(a) ao Supermercado Simulator!')
    }
  }, [])

  return (
    <Container>
      <SideBar />
      <GameDashboard />
    </Container>
  )
}
