'use client'

import React, { useState } from 'react'
import { styled } from 'styled-components'
import { MdAccountBalance, MdAdd, MdRemove, MdSettings, MdRefresh } from 'react-icons/md'
import type { UserBalance } from '@/types/finance'

interface BalanceManagementCardProps {
  balance: UserBalance | null;
  onAdd: (amount: number, description: string) => Promise<void>;
  onSubtract: (amount: number, description: string) => Promise<void>;
  onSet: (amount: number, description: string) => Promise<void>;
  onReset: () => Promise<void>;
}

const Card = styled.div`
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  padding: 2rem;
  color: white;
  box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -50%;
    width: 100%;
    height: 100%;
    background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
    pointer-events: none;
  }
`;

const Header = styled.div`
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
  position: relative;
  z-index: 1;
`;

const IconContainer = styled.div`
  background: rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  padding: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
`;

const Title = styled.h3`
  font-size: 1.2rem;
  font-weight: 600;
  margin: 0;
`;

const BalanceSection = styled.div`
  margin-bottom: 2rem;
  position: relative;
  z-index: 1;
`;

const BalanceAmount = styled.div`
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
`;

const BalanceLabel = styled.div`
  font-size: 0.9rem;
  opacity: 0.9;
`;

const ActionsGrid = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1.5rem;
  position: relative;
  z-index: 1;
`;

const ActionButton = styled.button<{ variant?: 'add' | 'subtract' | 'set' | 'reset' }>`
  padding: 0.75rem;
  border: none;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  backdrop-filter: blur(10px);
  
  &:hover {
    background: rgba(255, 255, 255, 0.3);
    transform: translateY(-2px);
  }
  
  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
`;

const Modal = styled.div<{ $isOpen: boolean }>`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: ${({ $isOpen }) => $isOpen ? 'flex' : 'none'};
  align-items: center;
  justify-content: center;
  z-index: 1000;
`;

const ModalContent = styled.div`
  background: white;
  border-radius: 16px;
  padding: 2rem;
  width: 90%;
  max-width: 400px;
  color: ${({ theme }) => theme.colors.textPrimary};
`;

const ModalHeader = styled.div`
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
`;

const ModalTitle = styled.h3`
  font-size: 1.2rem;
  font-weight: 600;
  margin: 0;
`;

const FormGroup = styled.div`
  margin-bottom: 1rem;
`;

const Label = styled.label`
  display: block;
  font-size: 0.9rem;
  font-weight: 500;
  margin-bottom: 0.5rem;
  color: ${({ theme }) => theme.colors.textSecondary};
`;

const Input = styled.input`
  width: 100%;
  padding: 0.75rem;
  border: 1px solid ${({ theme }) => theme.colors.border};
  border-radius: 8px;
  font-size: 0.9rem;
  
  &:focus {
    outline: none;
    border-color: ${({ theme }) => theme.colors.primaryBlue};
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
  }
`;

const ButtonGroup = styled.div`
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
`;

const Button = styled.button<{ variant?: 'primary' | 'secondary' }>`
  flex: 1;
  padding: 0.75rem 1rem;
  border: none;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  
  ${({ variant = 'primary', theme }) => variant === 'primary' ? `
    background: ${theme.colors.primaryBlue};
    color: white;
    
    &:hover {
      background: ${theme.colors.secondaryBlue};
    }
    
    &:disabled {
      background: ${theme.colors.textSecondary};
      cursor: not-allowed;
    }
  ` : `
    background: transparent;
    color: ${theme.colors.textSecondary};
    border: 1px solid ${theme.colors.border};
    
    &:hover {
      background: ${theme.colors.backgroundSecondary};
    }
  `}
`;

const formatCurrency = (amount: number) => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(amount)
}

export default function BalanceManagementCard({ balance, onAdd, onSubtract, onSet, onReset }: BalanceManagementCardProps) {
  const [modalOpen, setModalOpen] = useState(false)
  const [modalType, setModalType] = useState<'add' | 'subtract' | 'set' | null>(null)
  const [amount, setAmount] = useState('')
  const [description, setDescription] = useState('')
  const [loading, setLoading] = useState(false)

  const handleOpenModal = (type: 'add' | 'subtract' | 'set') => {
    setModalType(type)
    setModalOpen(true)
    setAmount('')
    setDescription('')
  }

  const handleCloseModal = () => {
    setModalOpen(false)
    setModalType(null)
    setAmount('')
    setDescription('')
  }

  const handleSubmit = async () => {
    if (!amount || parseFloat(amount) <= 0) {
      alert('Por favor, insira um valor válido')
      return
    }

    setLoading(true)
    try {
      const numericAmount = parseFloat(amount)
      
      switch (modalType) {
        case 'add':
          await onAdd(numericAmount, description)
          break
        case 'subtract':
          await onSubtract(numericAmount, description)
          break
        case 'set':
          await onSet(numericAmount, description)
          break
      }
      
      handleCloseModal()
    } catch (error) {
      console.error('Erro na operação:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleReset = async () => {
    if (confirm('Tem certeza que deseja resetar o saldo para R$ 0,00?')) {
      setLoading(true)
      try {
        await onReset()
      } catch (error) {
        console.error('Erro ao resetar:', error)
      } finally {
        setLoading(false)
      }
    }
  }

  const getModalTitle = () => {
    switch (modalType) {
      case 'add': return 'Adicionar ao Saldo'
      case 'subtract': return 'Subtrair do Saldo'
      case 'set': return 'Definir Saldo'
      default: return ''
    }
  }

  const getModalIcon = () => {
    switch (modalType) {
      case 'add': return <MdAdd />
      case 'subtract': return <MdRemove />
      case 'set': return <MdSettings />
      default: return null
    }
  }

  return (
    <>
      <Card>
        <Header>
          <IconContainer>
            <MdAccountBalance size={24} />
          </IconContainer>
          <Title>Saldo Atual</Title>
        </Header>

        <BalanceSection>
          <BalanceAmount>
            {balance ? formatCurrency(balance.current_balance) : 'R$ 0,00'}
          </BalanceAmount>
          <BalanceLabel>
            Última atualização: {balance ? new Date(balance.last_updated).toLocaleString('pt-BR') : '-'}
          </BalanceLabel>
        </BalanceSection>

        <ActionsGrid>
          <ActionButton 
            variant="add" 
            onClick={() => handleOpenModal('add')}
            disabled={loading}
          >
            <MdAdd />
            Adicionar
          </ActionButton>
          
          <ActionButton 
            variant="subtract" 
            onClick={() => handleOpenModal('subtract')}
            disabled={loading}
          >
            <MdRemove />
            Subtrair
          </ActionButton>
          
          <ActionButton 
            variant="set" 
            onClick={() => handleOpenModal('set')}
            disabled={loading}
          >
            <MdSettings />
            Definir
          </ActionButton>
          
          <ActionButton 
            variant="reset" 
            onClick={handleReset}
            disabled={loading}
          >
            <MdRefresh />
            Resetar
          </ActionButton>
        </ActionsGrid>
      </Card>

      <Modal $isOpen={modalOpen}>
        <ModalContent>
          <ModalHeader>
            <IconContainer>
              {getModalIcon()}
            </IconContainer>
            <ModalTitle>{getModalTitle()}</ModalTitle>
          </ModalHeader>

          <FormGroup>
            <Label htmlFor="amount">Valor (R$)</Label>
            <Input
              id="amount"
              type="number"
              step="0.01"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              placeholder="0,00"
            />
          </FormGroup>

          <FormGroup>
            <Label htmlFor="description">Descrição (opcional)</Label>
            <Input
              id="description"
              type="text"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Motivo da operação..."
            />
          </FormGroup>

          <ButtonGroup>
            <Button 
              variant="primary" 
              onClick={handleSubmit}
              disabled={loading}
            >
              {loading ? 'Processando...' : 'Confirmar'}
            </Button>
            <Button 
              variant="secondary" 
              onClick={handleCloseModal}
              disabled={loading}
            >
              Cancelar
            </Button>
          </ButtonGroup>
        </ModalContent>
      </Modal>
    </>
  )
}
