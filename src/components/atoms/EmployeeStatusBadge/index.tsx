"use client";

import React from "react";
import styled from "styled-components";
import type { EmploymentStatus } from "@/types/employee";

interface EmployeeStatusBadgeProps {
  status: EmploymentStatus;
  displayText: string;
}

const Badge = styled.span<{ $status: EmploymentStatus }>`
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;

  ${({ $status }) => {
    switch ($status) {
      case "ACTIVE":
        return `
          background-color: #D1FAE5;
          color: #065F46;
        `;
      case "INACTIVE":
        return `
          background-color: #FEE2E2;
          color: #991B1B;
        `;
      case "ON_LEAVE":
        return `
          background-color: #FEF3C7;
          color: #92400E;
        `;
      case "TERMINATED":
        return `
          background-color: #E5E7EB;
          color: #1F2937;
        `;
      default:
        return `
          background-color: #F3F4F6;
          color: #6B7280;
        `;
    }
  }}
`;

export default function EmployeeStatusBadge({
  status,
  displayText,
}: EmployeeStatusBadgeProps) {
  return <Badge $status={status}>{displayText}</Badge>;
}
