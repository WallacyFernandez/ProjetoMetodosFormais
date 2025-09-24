"use client";

import React, { useState, useEffect } from "react";
import { styled } from "styled-components";
import { MdAdd, MdEdit, MdClose } from "react-icons/md";
import type { TransactionCreate, Category, Transaction } from "@/types/finance";
import CategoryDropdown from "@/components/molecules/CategoryDropdown";
import { toast } from "react-toastify";

interface TransactionFormProps {
  categories: Category[];
  onSubmit: (data: TransactionCreate) => Promise<void>;
  editingTransaction?: Transaction | null;
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

export default function TransactionForm({
  categories,
  onSubmit,
  editingTransaction,
  onCancel,
}: TransactionFormProps) {
  const [formData, setFormData] = useState<TransactionCreate>({
    amount: 0,
    transaction_type: "EXPENSE",
    category: "",
    description: "",
    transaction_date: new Date().toISOString().split("T")[0],
    is_recurring: false,
  });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (editingTransaction) {
      setFormData({
        amount: editingTransaction.amount,
        transaction_type: editingTransaction.transaction_type,
        category: editingTransaction.category,
        description: editingTransaction.description,
        transaction_date: editingTransaction.created_at.split("T")[0],
        is_recurring: editingTransaction.is_recurring,
      });
    }
  }, [editingTransaction]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    // Validações
    if (formData.amount <= 0) {
      toast.error("Por favor, insira um valor maior que zero");
      setLoading(false);
      return;
    }

    if (!formData.category) {
      toast.error("Por favor, selecione uma categoria");
      setLoading(false);
      return;
    }

    if (!formData.description.trim()) {
      toast.error("Por favor, insira uma descrição");
      setLoading(false);
      return;
    }

    try {
      await onSubmit(formData);
      setFormData({
        amount: 0,
        transaction_type: "EXPENSE",
        category: "",
        description: "",
        transaction_date: new Date().toISOString().split("T")[0],
        is_recurring: false,
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
    const { name, value, type } = e.target;

    setFormData((prev) => ({
      ...prev,
      [name]:
        type === "checkbox"
          ? (e.target as HTMLInputElement).checked
          : name === "amount"
            ? parseFloat(value) || 0
            : value,
    }));
  };

  return (
    <FormCard>
      <Header>
        <Title>
          {editingTransaction ? <MdEdit /> : <MdAdd />}
          {editingTransaction ? "Editar Transação" : "Nova Transação"}
        </Title>
        <CloseButton onClick={onCancel}>
          <MdClose size={20} />
        </CloseButton>
      </Header>

      <Form onSubmit={handleSubmit}>
        <FormGroup>
          <Label htmlFor="amount">Valor *</Label>
          <Input
            id="amount"
            name="amount"
            type="number"
            step="0.01"
            value={formData.amount.toString()}
            onChange={handleInputChange}
            placeholder="0,00"
            required
          />
        </FormGroup>

        <FormGroup>
          <Label htmlFor="transaction_type">Tipo *</Label>
          <Select
            id="transaction_type"
            name="transaction_type"
            value={formData.transaction_type}
            onChange={handleInputChange}
            required
          >
            <option value="EXPENSE">Despesa</option>
            <option value="INCOME">Receita</option>
          </Select>
        </FormGroup>

        <FormGroup>
          <Label htmlFor="category">Categoria *</Label>
          <CategoryDropdown
            categories={categories || []}
            selectedCategory={formData.category}
            transactionType={formData.transaction_type}
            onChange={(categoryId) =>
              setFormData((prev) => ({ ...prev, category: categoryId }))
            }
            required
            placeholder="Selecione uma categoria"
          />
        </FormGroup>

        <FormGroup>
          <Label htmlFor="description">Descrição</Label>
          <TextArea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleInputChange}
            placeholder="Descrição da transação..."
          />
        </FormGroup>

        <FormGroup>
          <Label htmlFor="date">Data *</Label>
          <Input
            id="date"
            name="transaction_date"
            type="date"
            value={formData.transaction_date}
            onChange={handleInputChange}
            required
          />
        </FormGroup>

        <FormGroup>
          <Label
            style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}
          >
            <input
              type="checkbox"
              name="is_recurring"
              checked={formData.is_recurring}
              onChange={handleInputChange}
            />
            Transação recorrente
          </Label>
        </FormGroup>

        <ButtonGroup>
          <Button type="submit" disabled={loading}>
            {loading
              ? "Salvando..."
              : editingTransaction
                ? "Atualizar"
                : "Criar"}
          </Button>
          <Button type="button" variant="secondary" onClick={onCancel}>
            Cancelar
          </Button>
        </ButtonGroup>
      </Form>
    </FormCard>
  );
}
