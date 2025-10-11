"use client";

import React from "react";
import styled from "styled-components";
import type { DepartmentType } from "@/types/employee";

interface DepartmentBadgeProps {
  department: DepartmentType;
  displayText: string;
}

const Badge = styled.span<{ $department: DepartmentType }>`
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;

  ${({ $department }) => {
    switch ($department) {
      case "VENDAS":
        return `
          background-color: #DBEAFE;
          color: #1E40AF;
        `;
      case "ESTOQUE":
        return `
          background-color: #FEF3C7;
          color: #92400E;
        `;
      case "CAIXA":
        return `
          background-color: #D1FAE5;
          color: #065F46;
        `;
      case "GERENCIA":
        return `
          background-color: #E9D5FF;
          color: #6B21A8;
        `;
      case "LIMPEZA":
        return `
          background-color: #E0E7FF;
          color: #3730A3;
        `;
      case "SEGURANCA":
        return `
          background-color: #FEE2E2;
          color: #991B1B;
        `;
      case "RH":
        return `
          background-color: #FCE7F3;
          color: #9F1239;
        `;
      default:
        return `
          background-color: #F3F4F6;
          color: #6B7280;
        `;
    }
  }}
`;

export default function DepartmentBadge({
  department,
  displayText,
}: DepartmentBadgeProps) {
  return <Badge $department={department}>{displayText}</Badge>;
}
