"use client";

import React, { useState } from "react";
import styled from "styled-components";
import type { PayrollProcess } from "@/types/employee";

interface PayrollProcessModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (data: PayrollProcess) => Promise<void>;
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
  max-width: 500px;
  width: 90%;
`;

const Title = styled.h2`
  font-size: 1.5rem;
  font-weight: 700;
  color: #111827;
  margin-bottom: 1rem;
`;

const Description = styled.p`
  font-size: 0.875rem;
  color: #6b7280;
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

const CheckboxGroup = styled.div`
  display: flex;
  align-items: center;
  gap: 0.5rem;
`;

const Checkbox = styled.input`
  width: 1rem;
  height: 1rem;
  cursor: pointer;
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

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
`;

const WarningBox = styled.div`
  background-color: #fef3c7;
  border: 1px solid #fcd34d;
  border-radius: 8px;
  padding: 1rem;
  margin-top: 1rem;
`;

const WarningText = styled.p`
  font-size: 0.875rem;
  color: #92400e;
  margin: 0;
`;

export default function PayrollProcessModal({
  isOpen,
  onClose,
  onSubmit,
}: PayrollProcessModalProps) {
  const [formData, setFormData] = useState<PayrollProcess>({
    payment_month:
      new Date().toISOString().split("T")[0].substring(0, 7) + "-01",
    include_inactive: false,
  });

  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      await onSubmit(formData);
      onClose();
    } catch (error) {
      console.error("Error processing payroll:", error);
    } finally {
      setIsSubmitting(false);
    }
  };

  if (!isOpen) return null;

  return (
    <Overlay $isOpen={isOpen} onClick={onClose}>
      <Modal onClick={(e) => e.stopPropagation()}>
        <Title>Processar Folha de Pagamento</Title>
        <Description>
          Processe os pagamentos mensais de todos os funcionários ativos. O
          valor será debitado automaticamente do seu saldo.
        </Description>

        <Form onSubmit={handleSubmit}>
          <FormGroup>
            <Label htmlFor="payment_month">Mês de Referência *</Label>
            <Input
              id="payment_month"
              type="month"
              value={formData.payment_month.substring(0, 7)}
              onChange={(e) =>
                setFormData({
                  ...formData,
                  payment_month: e.target.value + "-01",
                })
              }
              required
            />
          </FormGroup>

          <FormGroup>
            <CheckboxGroup>
              <Checkbox
                id="include_inactive"
                type="checkbox"
                checked={formData.include_inactive}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    include_inactive: e.target.checked,
                  })
                }
              />
              <Label htmlFor="include_inactive">
                Incluir funcionários inativos
              </Label>
            </CheckboxGroup>
          </FormGroup>

          <WarningBox>
            <WarningText>
              ⚠️ Esta ação criará registros de pagamento para todos os
              funcionários e debitará o valor total do seu saldo. Certifique-se
              de ter saldo suficiente antes de continuar.
            </WarningText>
          </WarningBox>

          <ButtonGroup>
            <Button
              type="button"
              $variant="secondary"
              onClick={onClose}
              disabled={isSubmitting}
            >
              Cancelar
            </Button>
            <Button type="submit" $variant="primary" disabled={isSubmitting}>
              {isSubmitting ? "Processando..." : "Processar Pagamentos"}
            </Button>
          </ButtonGroup>
        </Form>
      </Modal>
    </Overlay>
  );
}
