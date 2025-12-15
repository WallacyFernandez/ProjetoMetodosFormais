"use client";

import React, { useState, useEffect } from "react";
import styled from "styled-components";
import { toast } from "react-toastify";
import { getErrorMessage } from "@/utils/httpErrorToast";
import type { HttpError } from "@/services/httpClient";
import type { EmployeePosition, DepartmentType } from "@/types/employee";

interface PositionFormModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (data: PositionFormData) => Promise<void>;
  position?: EmployeePosition | null;
}

export interface PositionFormData {
  name: string;
  description?: string;
  base_salary: number;
  min_salary: number;
  max_salary: number;
  department: DepartmentType;
  is_active: boolean;
}

const Overlay = styled.div<{ $isOpen: boolean }>`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: ${({ $isOpen }) => ($isOpen ? "flex" : "none")};
  align-items: center;
  justify-content: center;
  z-index: 1000;
`;

const Modal = styled.div`
  background: white;
  border-radius: 12px;
  padding: 2rem;
  max-width: 600px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
`;

const Title = styled.h2`
  font-size: 1.5rem;
  font-weight: 700;
  color: #111827;
  margin-bottom: 1.5rem;
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
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
`;

const Input = styled.input`
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 0.875rem;

  &:focus {
    outline: none;
    border-color: #2563eb;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
  }
`;

const Select = styled.select`
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 0.875rem;
  background-color: white;

  &:focus {
    outline: none;
    border-color: #2563eb;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
  }
`;

const TextArea = styled.textarea`
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 0.875rem;
  min-height: 100px;
  resize: vertical;

  &:focus {
    outline: none;
    border-color: #2563eb;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
  }
`;

const ButtonGroup = styled.div`
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
  margin-top: 1rem;
`;

const Button = styled.button<{ $variant?: "primary" | "secondary" }>`
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.2s;

  ${({ $variant = "primary" }) =>
    $variant === "primary"
      ? `
    background-color: #2563EB;
    color: white;
    &:hover {
      background-color: #1D4ED8;
    }
  `
      : `
    background-color: #F3F4F6;
    color: #374151;
    &:hover {
      background-color: #E5E7EB;
    }
  `}
`;

const HelperText = styled.span`
  font-size: 0.75rem;
  color: #6b7280;
`;

const SalaryRow = styled.div`
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
`;

export default function PositionFormModal({
  isOpen,
  onClose,
  onSubmit,
  position,
}: PositionFormModalProps) {
  const [formData, setFormData] = useState<PositionFormData>({
    name: "",
    description: "",
    base_salary: 0,
    min_salary: 0,
    max_salary: 0,
    department: "VENDAS",
    is_active: true,
  });

  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    if (position) {
      setFormData({
        name: position.name,
        description: position.description || "",
        base_salary: position.base_salary,
        min_salary: position.min_salary,
        max_salary: position.max_salary,
        department: position.department,
        is_active: position.is_active,
      });
    } else {
      setFormData({
        name: "",
        description: "",
        base_salary: 0,
        min_salary: 0,
        max_salary: 0,
        department: "VENDAS",
        is_active: true,
      });
    }
  }, [position, isOpen]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      await onSubmit(formData);
      onClose();
    } catch (error: any) {
      console.error("Error submitting form:", error);
      const errorMessage = getErrorMessage(error as HttpError, 'Erro ao salvar cargo. Verifique os dados informados.');
      toast.error(errorMessage);
    } finally {
      setIsSubmitting(false);
    }
  };

  if (!isOpen) return null;

  return (
    <Overlay $isOpen={isOpen} onClick={onClose}>
      <Modal onClick={(e) => e.stopPropagation()}>
        <Title>{position ? "Editar Cargo" : "Novo Cargo"}</Title>

        <Form onSubmit={handleSubmit}>
          <FormGroup>
            <Label htmlFor="name">Nome do Cargo *</Label>
            <Input
              id="name"
              type="text"
              value={formData.name}
              onChange={(e) =>
                setFormData({ ...formData, name: e.target.value })
              }
              required
            />
          </FormGroup>

          <FormGroup>
            <Label htmlFor="department">Departamento *</Label>
            <Select
              id="department"
              value={formData.department}
              onChange={(e) =>
                setFormData({
                  ...formData,
                  department: e.target.value as DepartmentType,
                })
              }
              required
            >
              <option value="VENDAS">Vendas</option>
              <option value="ESTOQUE">Estoque</option>
              <option value="CAIXA">Caixa</option>
              <option value="GERENCIA">Gerência</option>
              <option value="LIMPEZA">Limpeza</option>
              <option value="SEGURANCA">Segurança</option>
              <option value="RH">Recursos Humanos</option>
            </Select>
          </FormGroup>

          <FormGroup>
            <Label>Faixa Salarial *</Label>
            <SalaryRow>
              <div>
                <Label htmlFor="min_salary">Mínimo</Label>
                <Input
                  id="min_salary"
                  type="number"
                  step="0.01"
                  min="0"
                  value={formData.min_salary}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      min_salary: Number(e.target.value),
                    })
                  }
                  required
                />
              </div>
              <div>
                <Label htmlFor="base_salary">Base</Label>
                <Input
                  id="base_salary"
                  type="number"
                  step="0.01"
                  min="0"
                  value={formData.base_salary}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      base_salary: Number(e.target.value),
                    })
                  }
                  required
                />
              </div>
              <div>
                <Label htmlFor="max_salary">Máximo</Label>
                <Input
                  id="max_salary"
                  type="number"
                  step="0.01"
                  min="0"
                  value={formData.max_salary}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      max_salary: Number(e.target.value),
                    })
                  }
                  required
                />
              </div>
            </SalaryRow>
            <HelperText>
              O salário base deve estar entre o mínimo e o máximo
            </HelperText>
          </FormGroup>

          <FormGroup>
            <Label htmlFor="description">Descrição</Label>
            <TextArea
              id="description"
              value={formData.description}
              onChange={(e) =>
                setFormData({ ...formData, description: e.target.value })
              }
            />
          </FormGroup>

          <ButtonGroup>
            <Button type="button" $variant="secondary" onClick={onClose}>
              Cancelar
            </Button>
            <Button type="submit" $variant="primary" disabled={isSubmitting}>
              {isSubmitting ? "Salvando..." : position ? "Atualizar" : "Criar"}
            </Button>
          </ButtonGroup>
        </Form>
      </Modal>
    </Overlay>
  );
}
