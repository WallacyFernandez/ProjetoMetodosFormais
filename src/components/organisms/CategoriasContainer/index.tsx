'use client'

import React, { useContext, useEffect, useState } from 'react'
import { styled } from 'styled-components'
import { IsSidebarOnContext } from '@/context/IsSidebarOnContext'
import { 
  GetCategories, 
  CreateCategory, 
  UpdateCategory, 
  DeleteCategory 
} from '@/services/FinanceServices'
import type { Category, CategoryCreate } from '@/types/finance'
import PageHeader from '@/components/molecules/PageHeader'
import CategoryForm from '@/components/molecules/CategoryForm'
import CategoryGrid from '@/components/molecules/CategoryGrid'
import { toast } from 'react-toastify'

interface CategoriasContainerProps {
  $isCollapsed: boolean;
}

const Container = styled.div<CategoriasContainerProps>`
  background-color: ${({ theme }) => theme.colors.backgroundSecondary};
  margin-left: ${({ $isCollapsed }) => $isCollapsed ? '80px' : '280px'};
  min-height: 100vh;
  padding: 2rem;
  transition: margin-left 0.3s ease;
`;

const Content = styled.div`
  max-width: 1200px;
  margin: 0 auto;
`;

const Grid = styled.div`
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 2rem;
  margin-top: 2rem;

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
`;

export default function CategoriasContainer() {
  const { isCollapsed } = useContext(IsSidebarOnContext)
  const [categories, setCategories] = useState<Category[]>([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [editingCategory, setEditingCategory] = useState<Category | null>(null)

  const loadCategories = async () => {
    try {
      setLoading(true)
      const categoriesData = await GetCategories()
      setCategories(categoriesData)
    } catch (error) {
      console.error('Erro ao carregar categorias:', error)
      toast.error('Erro ao carregar categorias')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadCategories()
  }, [])

  const handleCreateCategory = async (categoryData: CategoryCreate) => {
    try {
      const newCategory = await CreateCategory(categoryData)
      setCategories(prev => [...prev, newCategory])
      setShowForm(false)
      toast.success('Categoria criada com sucesso!')
    } catch (error) {
      console.error('Erro ao criar categoria:', error)
      toast.error('Erro ao criar categoria')
    }
  }

  const handleUpdateCategory = async (id: string, categoryData: Partial<CategoryCreate>) => {
    try {
      const updatedCategory = await UpdateCategory(id, categoryData)
      setCategories(prev => prev.map(cat => cat.id === id ? updatedCategory : cat))
      setShowForm(false)
      setEditingCategory(null)
      toast.success('Categoria atualizada com sucesso!')
    } catch (error) {
      console.error('Erro ao atualizar categoria:', error)
      toast.error('Erro ao atualizar categoria')
    }
  }

  const handleDeleteCategory = async (id: string) => {
    try {
      await DeleteCategory(id)
      setCategories(prev => prev.filter(cat => cat.id !== id))
      toast.success('Categoria excluída com sucesso!')
    } catch (error) {
      console.error('Erro ao excluir categoria:', error)
      toast.error('Erro ao excluir categoria')
    }
  }

  const handleEditCategory = (category: Category) => {
    setEditingCategory(category)
    setShowForm(true)
  }

  if (loading) {
    return (
      <Container $isCollapsed={isCollapsed}>
        <Content>
          <PageHeader $title="Categorias" $subtitle="Gerencie suas categorias financeiras" />
          <div style={{ textAlign: 'center', padding: '2rem' }}>
            Carregando...
          </div>
        </Content>
      </Container>
    )
  }

  return (
    <Container $isCollapsed={isCollapsed}>
      <Content>
        <PageHeader 
          $title="Categorias" 
          $subtitle="Gerencie suas categorias financeiras"
          actionButton={{
            text: showForm ? 'Ver Categorias' : 'Nova Categoria',
            onClick: () => {
              setShowForm(!showForm)
              setEditingCategory(null)
            }
          }}
        />

        <Grid>
          <div>
            <CategoryForm
              onSubmit={editingCategory ? 
                (data) => handleUpdateCategory(editingCategory.id, data) :
                handleCreateCategory
              }
              editingCategory={editingCategory}
              onCancel={() => {
                setShowForm(false)
                setEditingCategory(null)
              }}
            />
          </div>
          
          <div>
            <CategoryGrid
              categories={categories}
              onEdit={handleEditCategory}
              onDelete={handleDeleteCategory}
            />
          </div>
        </Grid>
      </Content>
    </Container>
  )
}
