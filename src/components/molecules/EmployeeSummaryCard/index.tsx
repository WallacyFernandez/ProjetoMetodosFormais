"use client";

import React from "react";
import styled from "styled-components";
import type { EmployeeSummary } from "@/types/employee";

interface EmployeeSummaryCardProps {
  summary: EmployeeSummary;
  loading?: boolean;
}

const Card = styled.div`
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
`;

const Title = styled.h3`
  font-size: 1.125rem;
  font-weight: 600;
  color: #111827;
  margin-bottom: 1.5rem;
`;

const StatsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 1.5rem;
`;

const StatItem = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
`;

const StatLabel = styled.span`
  font-size: 0.875rem;
  color: #6b7280;
`;

const StatValue = styled.span`
  font-size: 1.5rem;
  font-weight: 700;
  color: #111827;
`;

const DepartmentGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e5e7eb;
`;

const DepartmentItem = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const DepartmentName = styled.span`
  font-size: 0.875rem;
  color: #374151;
`;

const DepartmentCount = styled.span`
  font-size: 0.875rem;
  font-weight: 600;
  color: #111827;
  background-color: #f3f4f6;
  padding: 0.25rem 0.5rem;
  border-radius: 6px;
`;

const Subtitle = styled.h4`
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.75rem;
`;

export default function EmployeeSummaryCard({
  summary,
  loading,
}: EmployeeSummaryCardProps) {
  if (loading) {
    return (
      <Card>
        <Title>Carregando...</Title>
      </Card>
    );
  }

  return (
    <Card>
      <Title>Resumo de Funcionários</Title>

      <StatsGrid>
        <StatItem>
          <StatLabel>Total de Funcionários</StatLabel>
          <StatValue>{summary.total_employees}</StatValue>
        </StatItem>

        <StatItem>
          <StatLabel>Funcionários Ativos</StatLabel>
          <StatValue style={{ color: "#059669" }}>
            {summary.active_employees}
          </StatValue>
        </StatItem>

        <StatItem>
          <StatLabel>Funcionários Inativos</StatLabel>
          <StatValue style={{ color: "#DC2626" }}>
            {summary.inactive_employees}
          </StatValue>
        </StatItem>

        <StatItem>
          <StatLabel>Folha Mensal Total</StatLabel>
          <StatValue style={{ color: "#2563EB" }}>
            {summary.total_monthly_payroll_formatted}
          </StatValue>
        </StatItem>
      </StatsGrid>

      {Object.keys(summary.employees_by_department).length > 0 && (
        <>
          <Subtitle>Funcionários por Departamento</Subtitle>
          <DepartmentGrid>
            {Object.entries(summary.employees_by_department).map(
              ([dept, count]) => (
                <DepartmentItem key={dept}>
                  <DepartmentName>{dept}</DepartmentName>
                  <DepartmentCount>{count}</DepartmentCount>
                </DepartmentItem>
              ),
            )}
          </DepartmentGrid>
        </>
      )}
    </Card>
  );
}
