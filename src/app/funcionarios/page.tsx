"use client";

import React, { useState, useEffect, useContext } from "react";
import styled from "styled-components";
import SideBar from "@/components/organisms/Sidebar";
import { IsSidebarOnContext } from "@/context/IsSidebarOnContext";
import PageHeader from "@/components/molecules/PageHeader";
import EmployeeTable from "@/components/organisms/EmployeeTable";
import EmployeeFormModal from "@/components/organisms/EmployeeFormModal";
import PayrollProcessModal from "@/components/organisms/PayrollProcessModal";
import PositionFormModal, {
  type PositionFormData,
} from "@/components/organisms/PositionFormModal";
import EmployeeSummaryCard from "@/components/molecules/EmployeeSummaryCard";
import EmployeeServices from "@/services/EmployeeServices";
import type {
  Employee,
  EmployeeCreate,
  EmployeePosition,
  EmployeeSummary,
  PayrollProcess,
} from "@/types/employee";
import { toast } from "react-toastify";
import { showHttpErrorToast } from "@/utils/httpErrorToast";

const PageContainer = styled.div`
  min-height: 100%;
  background-color: #f5f5f5;
  padding-bottom: 5rem;
  margin: auto;
`;

interface ContainerProps {
  $isCollapsed: boolean;
}

const Container = styled.div<ContainerProps>`
  background-color: ${({ theme }) => theme.colors.backgroundSecondary};
  margin-left: ${({ $isCollapsed }) => ($isCollapsed ? "0" : "16rem")};
  transition: all 0.3s ease-in-out;
  padding: 2rem;

  @media (max-width: 1000px) {
    margin-left: ${({ $isCollapsed }) => ($isCollapsed ? "7rem" : "18rem")};
  }

  @media (max-width: 834px) {
    margin-left: ${({ $isCollapsed }) => ($isCollapsed ? "3rem" : "17rem")};
  }

  @media (max-width: 768px) {
    margin-left: 0.3rem;
    margin-right: 0.3rem;
  }
`;

const Section = styled.section`
  margin-bottom: 2rem;
`;

const Header = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  gap: 1rem;
`;

const ButtonGroup = styled.div`
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
`;

const Button = styled.button<{
  $variant?: "primary" | "secondary" | "success";
}>`
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.2s;

  ${({ $variant = "primary" }) => {
    switch ($variant) {
      case "success":
        return `
          background-color: #10B981;
          color: white;
          &:hover {
            background-color: #059669;
          }
        `;
      case "secondary":
        return `
          background-color: #F3F4F6;
          color: #374151;
          border: 1px solid #D1D5DB;
          &:hover {
            background-color: #E5E7EB;
          }
        `;
      default:
        return `
          background-color: #2563EB;
          color: white;
          &:hover {
            background-color: #1D4ED8;
          }
        `;
    }
  }}
`;

const Title = styled.h1`
  font-size: 1.875rem;
  font-weight: 700;
  color: #111827;
`;

const Tabs = styled.div`
  display: flex;
  gap: 1rem;
  border-bottom: 2px solid #e5e7eb;
  margin-bottom: 1.5rem;
`;

const Tab = styled.button<{ $active: boolean }>`
  padding: 0.75rem 1.5rem;
  border: none;
  background: none;
  font-size: 0.875rem;
  font-weight: 600;
  color: ${({ $active }) => ($active ? "#2563EB" : "#6B7280")};
  border-bottom: 2px solid
    ${({ $active }) => ($active ? "#2563EB" : "transparent")};
  margin-bottom: -2px;
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    color: #2563eb;
  }
`;

type TabType = "employees" | "summary";

export default function FuncionariosPage() {
  const { isCollapsed } = useContext(IsSidebarOnContext);
  const [activeTab, setActiveTab] = useState<TabType>("employees");
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [positions, setPositions] = useState<EmployeePosition[]>([]);
  const [summary, setSummary] = useState<EmployeeSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [isFormModalOpen, setIsFormModalOpen] = useState(false);
  const [isPayrollModalOpen, setIsPayrollModalOpen] = useState(false);
  const [isPositionModalOpen, setIsPositionModalOpen] = useState(false);
  const [selectedEmployee, setSelectedEmployee] = useState<Employee | null>(
    null,
  );

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [employeesData, positionsData, summaryData] = await Promise.all([
        EmployeeServices.getEmployees(),
        EmployeeServices.getPositions(),
        EmployeeServices.getEmployeesSummary(),
      ]);

      setEmployees(employeesData);
      setPositions(positionsData);
      setSummary(summaryData);
    } catch (error) {
      showHttpErrorToast(error as any);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateEmployee = async (data: EmployeeCreate) => {
    try {
      await EmployeeServices.createEmployee(data);
      toast.success("Funcionário criado com sucesso!");
      loadData();
      setIsFormModalOpen(false);
    } catch (error) {
      showHttpErrorToast(error as any);
      throw error;
    }
  };

  const handleUpdateEmployee = async (data: EmployeeCreate) => {
    if (!selectedEmployee) return;

    try {
      await EmployeeServices.updateEmployee(selectedEmployee.id, data);
      toast.success("Funcionário atualizado com sucesso!");
      loadData();
      setIsFormModalOpen(false);
      setSelectedEmployee(null);
    } catch (error) {
      showHttpErrorToast(error as any);
      throw error;
    }
  };

  const handleDeleteEmployee = async (employee: Employee) => {
    if (!confirm(`Tem certeza que deseja excluir ${employee.name}?`)) return;

    try {
      await EmployeeServices.deleteEmployee(employee.id);
      toast.success("Funcionário excluído com sucesso!");
      loadData();
    } catch (error) {
      showHttpErrorToast(error as any);
    }
  };

  const handleTerminateEmployee = async (employee: Employee) => {
    if (!confirm(`Tem certeza que deseja demitir ${employee.name}?`)) return;

    try {
      await EmployeeServices.terminateEmployee(employee.id);
      toast.success("Funcionário demitido com sucesso!");
      loadData();
    } catch (error) {
      showHttpErrorToast(error as any);
    }
  };

  const handleReactivateEmployee = async (employee: Employee) => {
    if (!confirm(`Tem certeza que deseja reativar ${employee.name}?`)) return;

    try {
      await EmployeeServices.reactivateEmployee(employee.id);
      toast.success("Funcionário reativado com sucesso!");
      loadData();
    } catch (error) {
      showHttpErrorToast(error as any);
    }
  };

  const handleProcessPayroll = async (data: PayrollProcess) => {
    try {
      const result = await EmployeeServices.processMonthlyPayments(data);
      toast.success(result.message);
      loadData();
      setIsPayrollModalOpen(false);
    } catch (error) {
      showHttpErrorToast(error as any);
      throw error;
    }
  };

  const handleCreateDefaultPositions = async () => {
    if (!confirm("Deseja criar os cargos padrão?")) return;

    try {
      const result = await EmployeeServices.createDefaultPositions();
      toast.success(result.message);
      loadData();
    } catch (error) {
      showHttpErrorToast(error as any);
    }
  };

  const openCreateModal = () => {
    setSelectedEmployee(null);
    setIsFormModalOpen(true);
  };

  const openEditModal = (employee: Employee) => {
    setSelectedEmployee(employee);
    setIsFormModalOpen(true);
  };

  const handleCreatePosition = async (data: PositionFormData) => {
    try {
      await EmployeeServices.createPosition(data);
      toast.success("Cargo criado com sucesso!");
      loadData();
      setIsPositionModalOpen(false);
    } catch (error) {
      showHttpErrorToast(error as any);
      throw error;
    }
  };

  return (
    <PageContainer>
      <SideBar />
      <Container $isCollapsed={isCollapsed}>
        <Section>
          <Header>
            <Tabs>
              <Tab
                $active={activeTab === "employees"}
                onClick={() => setActiveTab("employees")}
              >
                Funcionários
              </Tab>
              <Tab
                $active={activeTab === "summary"}
                onClick={() => setActiveTab("summary")}
              >
                Resumo
              </Tab>
            </Tabs>

            <ButtonGroup>
              {positions.length === 0 && (
                <Button
                  $variant="secondary"
                  onClick={handleCreateDefaultPositions}
                >
                  Criar Cargos Padrão
                </Button>
              )}
              <Button
                $variant="secondary"
                onClick={() => setIsPositionModalOpen(true)}
              >
                + Novo Cargo
              </Button>
              <Button
                $variant="success"
                onClick={() => setIsPayrollModalOpen(true)}
              >
                Processar Folha
              </Button>
              <Button $variant="primary" onClick={openCreateModal}>
                + Novo Funcionário
              </Button>
            </ButtonGroup>
          </Header>

          {activeTab === "employees" && (
            <EmployeeTable
              employees={employees}
              onEdit={openEditModal}
              onDelete={handleDeleteEmployee}
              onTerminate={handleTerminateEmployee}
              onReactivate={handleReactivateEmployee}
              loading={loading}
            />
          )}

          {activeTab === "summary" && summary && (
            <EmployeeSummaryCard summary={summary} loading={loading} />
          )}
        </Section>

        <EmployeeFormModal
          isOpen={isFormModalOpen}
          onClose={() => {
            setIsFormModalOpen(false);
            setSelectedEmployee(null);
          }}
          onSubmit={
            selectedEmployee ? handleUpdateEmployee : handleCreateEmployee
          }
          employee={selectedEmployee}
          positions={positions}
        />

        <PayrollProcessModal
          isOpen={isPayrollModalOpen}
          onClose={() => setIsPayrollModalOpen(false)}
          onSubmit={handleProcessPayroll}
        />

        <PositionFormModal
          isOpen={isPositionModalOpen}
          onClose={() => setIsPositionModalOpen(false)}
          onSubmit={handleCreatePosition}
        />
      </Container>
    </PageContainer>
  );
}
