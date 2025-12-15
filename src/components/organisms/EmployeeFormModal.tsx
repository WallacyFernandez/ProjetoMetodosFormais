"use client";

import React, { useState, useEffect } from "react";
import styled from "styled-components";
import { toast } from "react-toastify";
import { getErrorMessage } from "@/utils/httpErrorToast";
import type { HttpError } from "@/services/httpClient";
import type {
  Employee,
  EmployeeCreate,
  EmployeePosition,
} from "@/types/employee";

interface EmployeeFormModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (data: EmployeeCreate) => Promise<void>;
  employee?: Employee | null;
  positions: EmployeePosition[];
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

export default function EmployeeFormModal({
  isOpen,
  onClose,
  onSubmit,
  employee,
  positions,
}: EmployeeFormModalProps) {
  const [formData, setFormData] = useState<EmployeeCreate>({
    name: "",
    cpf: "",
    email: "",
    phone: "",
    position: "",
    salary: 0,
    hire_date: new Date().toISOString().split("T")[0],
    notes: "",
  });

  const [selectedPosition, setSelectedPosition] =
    useState<EmployeePosition | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    if (!isOpen) return; // Só atualiza quando o modal estiver aberto

    if (employee) {
      setFormData({
        name: employee.name,
        cpf: employee.cpf,
        email: employee.email || "",
        phone: employee.phone || "",
        position: employee.position,
        salary: employee.salary,
        hire_date: employee.hire_date,
        notes: employee.notes || "",
      });

      const pos = positions.find((p) => p.id === employee.position);
      setSelectedPosition(pos || null);
    } else {
      setFormData({
        name: "",
        cpf: "",
        email: "",
        phone: "",
        position: "",
        salary: 0,
        hire_date: new Date().toISOString().split("T")[0],
        notes: "",
      });
      setSelectedPosition(null);
    }
  }, [employee, isOpen]);

  const handlePositionChange = (value: string) => {
    if (!value) {
      setSelectedPosition(null);
      setFormData((prev) => ({
        ...prev,
        position: "",
        salary: 0,
      }));
      return;
    }

    const position = positions.find((p) => p.id === value);

    setSelectedPosition(position || null);
    setFormData((prev) => ({
      ...prev,
      position: value,
      salary: position ? Number(position.base_salary) : 0,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      const submitData = {
        ...formData,
        // Corrigir problema de fuso horário - enviar apenas a data
        hire_date: formData.hire_date
          ? new Date(formData.hire_date + "T00:00:00")
              .toISOString()
              .split("T")[0]
          : formData.hire_date,
      };

      await onSubmit(submitData);
      onClose();
    } catch (error: any) {
      console.error("Error submitting form:", error);
      const errorMessage = getErrorMessage(error as HttpError, 'Erro ao salvar funcionário. Verifique os dados informados.');
      toast.error(errorMessage);
    } finally {
      setIsSubmitting(false);
    }
  };

  if (!isOpen) return null;

  return (
    <Overlay $isOpen={isOpen} onClick={onClose}>
      <Modal onClick={(e) => e.stopPropagation()}>
        <Title>{employee ? "Editar Funcionário" : "Novo Funcionário"}</Title>

        <Form onSubmit={handleSubmit}>
          <FormGroup>
            <Label htmlFor="name">Nome Completo *</Label>
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
            <Label htmlFor="cpf">CPF *</Label>
            <Input
              id="cpf"
              type="text"
              value={formData.cpf}
              onChange={(e) =>
                setFormData({ ...formData, cpf: e.target.value })
              }
              placeholder="000.000.000-00"
              required
            />
            <HelperText>Digite apenas números</HelperText>
          </FormGroup>

          <FormGroup>
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              type="email"
              value={formData.email}
              onChange={(e) =>
                setFormData({ ...formData, email: e.target.value })
              }
            />
          </FormGroup>

          <FormGroup>
            <Label htmlFor="phone">Telefone</Label>
            <Input
              id="phone"
              type="tel"
              value={formData.phone}
              onChange={(e) =>
                setFormData({ ...formData, phone: e.target.value })
              }
              placeholder="(00) 00000-0000"
            />
          </FormGroup>

          <FormGroup>
            <Label htmlFor="position">Cargo *</Label>
            <Select
              id="position"
              value={formData.position || ""}
              onChange={(e) => handlePositionChange(e.target.value)}
              required
            >
              <option value="">Selecione um cargo</option>
              {positions.map((position) => (
                <option key={position.id} value={position.id}>
                  {position.name} - {position.department_display}
                </option>
              ))}
            </Select>
          </FormGroup>

          {selectedPosition && (
            <FormGroup>
              <Label htmlFor="salary">Salário *</Label>
              <Input
                id="salary"
                type="number"
                step="0.01"
                min={Number(selectedPosition.min_salary)}
                max={Number(selectedPosition.max_salary)}
                value={formData.salary}
                onChange={(e) =>
                  setFormData({ ...formData, salary: Number(e.target.value) })
                }
                required
              />
              <HelperText>
                Faixa salarial: R${" "}
                {Number(selectedPosition.min_salary).toFixed(2)} - R${" "}
                {Number(selectedPosition.max_salary).toFixed(2)}
              </HelperText>
            </FormGroup>
          )}

          <FormGroup>
            <Label htmlFor="hire_date">Data de Contratação *</Label>
            <Input
              id="hire_date"
              type="date"
              value={formData.hire_date}
              onChange={(e) =>
                setFormData({ ...formData, hire_date: e.target.value })
              }
              required
            />
          </FormGroup>

          <FormGroup>
            <Label htmlFor="notes">Observações</Label>
            <TextArea
              id="notes"
              value={formData.notes}
              onChange={(e) =>
                setFormData({ ...formData, notes: e.target.value })
              }
            />
          </FormGroup>

          <ButtonGroup>
            <Button type="button" $variant="secondary" onClick={onClose}>
              Cancelar
            </Button>
            <Button type="submit" $variant="primary" disabled={isSubmitting}>
              {isSubmitting ? "Salvando..." : employee ? "Atualizar" : "Criar"}
            </Button>
          </ButtonGroup>
        </Form>
      </Modal>
    </Overlay>
  );
}
