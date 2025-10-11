"use client";

import React, { useEffect, useState } from "react";
import styled from "styled-components";
import { MdPeople, MdTrendingUp } from "react-icons/md";
import { useRouter } from "next/navigation";
import EmployeeServices from "@/services/EmployeeServices";
import type { EmployeeSummary } from "@/types/employee";

const Card = styled.div`
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transform: translateY(-2px);
  }
`;

const Header = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
`;

const Title = styled.h3`
  font-size: 0.875rem;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.05em;
`;

const Icon = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 8px;
  background-color: #dbeafe;
  color: #2563eb;

  svg {
    width: 1.5rem;
    height: 1.5rem;
  }
`;

const Content = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
`;

const MainStat = styled.div`
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
`;

const Value = styled.span`
  font-size: 2rem;
  font-weight: 700;
  color: #111827;
`;

const Label = styled.span`
  font-size: 0.875rem;
  color: #6b7280;
`;

const SubStat = styled.div`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding-top: 0.75rem;
  border-top: 1px solid #e5e7eb;
`;

const SubLabel = styled.span`
  font-size: 0.75rem;
  color: #6b7280;
`;

const SubValue = styled.span`
  font-size: 0.875rem;
  font-weight: 600;
  color: #2563eb;
`;

const LoadingText = styled.p`
  font-size: 0.875rem;
  color: #6b7280;
  text-align: center;
`;

export default function EmployeeQuickCard() {
  const router = useRouter();
  const [summary, setSummary] = useState<EmployeeSummary | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadSummary();
  }, []);

  const loadSummary = async () => {
    try {
      const data = await EmployeeServices.getEmployeesSummary();
      setSummary(data);
    } catch (error) {
      console.error("Erro ao carregar resumo de funcionários:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleClick = () => {
    router.push("/funcionarios");
  };

  if (loading) {
    return (
      <Card>
        <Header>
          <Title>Funcionários</Title>
          <Icon>
            <MdPeople />
          </Icon>
        </Header>
        <LoadingText>Carregando...</LoadingText>
      </Card>
    );
  }

  if (!summary) {
    return null;
  }

  return (
    <Card onClick={handleClick}>
      <Header>
        <Title>Funcionários</Title>
        <Icon>
          <MdPeople />
        </Icon>
      </Header>

      <Content>
        <MainStat>
          <Value>{summary.active_employees}</Value>
          <Label>ativos</Label>
        </MainStat>

        <SubStat>
          <SubLabel>Folha Mensal:</SubLabel>
          <SubValue>{summary.total_monthly_payroll_formatted}</SubValue>
        </SubStat>
      </Content>
    </Card>
  );
}
