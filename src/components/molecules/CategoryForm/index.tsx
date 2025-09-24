"use client";

import React, { useState, useEffect } from "react";
import { styled } from "styled-components";
import { MdAdd, MdEdit, MdClose, MdFace } from "react-icons/md";
import type { Category, CategoryCreate } from "@/types/finance";
import IconPicker from "@/components/molecules/IconPicker";

interface CategoryFormProps {
  onSubmit: (data: CategoryCreate) => Promise<void>;
  editingCategory?: Category | null;
  onCancel: () => void;
}

const FormCard = styled.div`
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border: 1px solid ${({ theme }) => theme.colors.border};
`;

const Header = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
`;

const Title = styled.h3`
  font-size: 1.1rem;
  font-weight: 600;
  color: ${({ theme }) => theme.colors.textPrimary};
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: 1rem;
`;

const FormGroup = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
`;

const Label = styled.label`
  font-size: 0.9rem;
  font-weight: 500;
  color: ${({ theme }) => theme.colors.textSecondary};
`;

const Input = styled.input`
  padding: 0.75rem;
  border: 1px solid ${({ theme }) => theme.colors.border};
  border-radius: 8px;
  font-size: 0.9rem;
  background: white;

  &:focus {
    outline: none;
    border-color: ${({ theme }) => theme.colors.primaryBlue};
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
  }
`;

const Select = styled.select`
  padding: 0.75rem;
  border: 1px solid ${({ theme }) => theme.colors.border};
  border-radius: 8px;
  font-size: 0.9rem;
  background: white;

  &:focus {
    outline: none;
    border-color: ${({ theme }) => theme.colors.primaryBlue};
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
  }
`;

const TextArea = styled.textarea`
  padding: 0.75rem;
  border: 1px solid ${({ theme }) => theme.colors.border};
  border-radius: 8px;
  font-size: 0.9rem;
  background: white;
  min-height: 80px;
  resize: vertical;

  &:focus {
    outline: none;
    border-color: ${({ theme }) => theme.colors.primaryBlue};
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
  }
`;

const ColorInput = styled.input`
  padding: 0.5rem;
  border: 1px solid ${({ theme }) => theme.colors.border};
  border-radius: 8px;
  width: 60px;
  height: 40px;
  cursor: pointer;

  &:focus {
    outline: none;
    border-color: ${({ theme }) => theme.colors.primaryBlue};
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
  }
`;

const ButtonGroup = styled.div`
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
`;

const Button = styled.button<{ variant?: "primary" | "secondary" }>`
  flex: 1;
  padding: 0.75rem 1rem;
  border: none;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;

  ${({ variant = "primary", theme }) =>
    variant === "primary"
      ? `
    background: ${theme.colors.primaryBlue};
    color: white;
    
    &:hover {
      background: ${theme.colors.secondaryBlue};
    }
    
    &:disabled {
      background: ${theme.colors.textSecondary};
      cursor: not-allowed;
    }
  `
      : `
    background: transparent;
    color: ${theme.colors.textSecondary};
    border: 1px solid ${theme.colors.border};
    
    &:hover {
      background: ${theme.colors.backgroundSecondary};
    }
  `}
`;

const CloseButton = styled.button`
  background: none;
  border: none;
  color: ${({ theme }) => theme.colors.textSecondary};
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 4px;

  &:hover {
    background: ${({ theme }) => theme.colors.backgroundSecondary};
  }
`;

const IconSelectorButton = styled.button`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  padding: 0.75rem;
  border: 1px solid ${({ theme }) => theme.colors.border};
  border-radius: 8px;
  background: white;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 1.5rem;
  min-height: 48px;

  &:hover {
    border-color: ${({ theme }) => theme.colors.primaryBlue};
    background: ${({ theme }) => theme.colors.backgroundSecondary};
  }

  &:focus {
    outline: none;
    border-color: ${({ theme }) => theme.colors.primaryBlue};
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
  }
`;

const IconPreview = styled.div`
  display: flex;
  align-items: center;
  gap: 0.5rem;

  span {
    font-size: 1.5rem;
  }
`;

const IconPlaceholder = styled.div`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: ${({ theme }) => theme.colors.textSecondary};

  span {
    font-size: 1.2rem;
  }
`;

export default function CategoryForm({
  onSubmit,
  editingCategory,
  onCancel,
}: CategoryFormProps) {
  const [formData, setFormData] = useState<CategoryCreate>({
    name: "",
    description: "",
    icon: "",
    color: "#3b82f6",
    category_type: "BOTH",
  });
  const [loading, setLoading] = useState(false);
  const [showIconPicker, setShowIconPicker] = useState(false);

  useEffect(() => {
    if (editingCategory) {
      setFormData({
        name: editingCategory.name,
        description: editingCategory.description,
        icon: editingCategory.icon,
        color: editingCategory.color,
        category_type: editingCategory.category_type,
      });
    }
  }, [editingCategory]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      await onSubmit(formData);
      setFormData({
        name: "",
        description: "",
        icon: "",
        color: "#3b82f6",
        category_type: "BOTH",
      });
    } catch (error) {
      console.error("Erro no formulário:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (
    e: React.ChangeEvent<
      HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement
    >,
  ) => {
    const { name, value } = e.target;

    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleIconSelect = (icon: string) => {
    setFormData((prev) => ({
      ...prev,
      icon: icon,
    }));
  };

  return (
    <FormCard>
      <Header>
        <Title>
          {editingCategory ? <MdEdit /> : <MdAdd />}
          {editingCategory ? "Editar Categoria" : "Nova Categoria"}
        </Title>
        <CloseButton onClick={onCancel}>
          <MdClose size={20} />
        </CloseButton>
      </Header>

      <Form onSubmit={handleSubmit}>
        <FormGroup>
          <Label htmlFor="name">Nome *</Label>
          <Input
            id="name"
            name="name"
            type="text"
            value={formData.name}
            onChange={handleInputChange}
            placeholder="Nome da categoria"
            required
          />
        </FormGroup>

        <FormGroup>
          <Label htmlFor="category_type">Tipo *</Label>
          <Select
            id="category_type"
            name="category_type"
            value={formData.category_type}
            onChange={handleInputChange}
            required
          >
            <option value="INCOME">Receita</option>
            <option value="EXPENSE">Despesa</option>
            <option value="BOTH">Receita e Despesa</option>
          </Select>
        </FormGroup>

        <FormGroup>
          <Label htmlFor="description">Descrição</Label>
          <TextArea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleInputChange}
            placeholder="Descrição da categoria..."
          />
        </FormGroup>

        <FormGroup>
          <Label htmlFor="icon">Ícone</Label>
          <IconSelectorButton
            type="button"
            onClick={() => setShowIconPicker(true)}
          >
            {formData.icon ? (
              <IconPreview>
                <span>{formData.icon}</span>
                <span>Clique para alterar</span>
              </IconPreview>
            ) : (
              <IconPlaceholder>
                <MdFace />
                <span>Escolher ícone</span>
              </IconPlaceholder>
            )}
          </IconSelectorButton>
        </FormGroup>

        <FormGroup>
          <Label htmlFor="color">Cor</Label>
          <div style={{ display: "flex", alignItems: "center", gap: "1rem" }}>
            <ColorInput
              id="color"
              name="color"
              type="color"
              value={formData.color}
              onChange={handleInputChange}
            />
            <Input
              type="text"
              value={formData.color}
              onChange={(e) =>
                setFormData((prev) => ({ ...prev, color: e.target.value }))
              }
              placeholder="#3b82f6"
              style={{ flex: 1 }}
            />
          </div>
        </FormGroup>

        <ButtonGroup>
          <Button type="submit" disabled={loading}>
            {loading ? "Salvando..." : editingCategory ? "Atualizar" : "Criar"}
          </Button>
          <Button type="button" variant="secondary" onClick={onCancel}>
            Cancelar
          </Button>
        </ButtonGroup>
      </Form>

      {showIconPicker && (
        <IconPicker
          selectedIcon={formData.icon}
          onIconSelect={handleIconSelect}
          categoryType={formData.category_type}
          onClose={() => setShowIconPicker(false)}
        />
      )}
    </FormCard>
  );
}
