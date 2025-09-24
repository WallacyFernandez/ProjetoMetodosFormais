'use client'

import SaldoContainer from '@/components/organisms/SaldoContainer'
import SideBar from '@/components/organisms/Sidebar'
import React, { useEffect } from 'react'
import { styled } from 'styled-components'
import { toast } from 'react-toastify'

const Container = styled.div`
  min-height: 100%;
  background-color: #F5F5F5;
  padding-bottom: 5rem;
  margin: auto;
`;

export default function SaldoPage() {
  useEffect(() => {
    if (typeof window === 'undefined') return
    const justLoggedIn = sessionStorage.getItem('justLoggedIn')
    if (justLoggedIn) {
      sessionStorage.removeItem('justLoggedIn')
      toast.success('Bem-vindo(a)!')
    }
  }, [])

  return (
    <Container>
      <SideBar />
      <SaldoContainer />
    </Container>
  )
}
