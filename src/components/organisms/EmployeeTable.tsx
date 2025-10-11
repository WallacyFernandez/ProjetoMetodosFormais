"use client";

import React from "react";
import styled from "styled-components";
import type { Employee } from "@/types/employee";
import EmployeeStatusBadge from "@/components/atoms/EmployeeStatusBadge";
import DepartmentBadge from "@/components/atoms/DepartmentBadge";

interface EmployeeTableProps {
  employees: Employee[];
  onEdit?: (employee: Employee) => void;
  onDelete?: (employee: Employee) => void;
  onTerminate?: (employee: Employee) => void;
  onReactivate?: (employee: Employee) => void;
  loading?: boolean;
}

const TableContainer = styled.div`
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
`;

const Table = styled.table`
  width: 100%;
  border-collapse: collapse;
`;

const Thead = styled.thead`
  background-color: #f9fafb;
`;

const Th = styled.th`
  padding: 0.75rem 1rem;
  text-align: left;
  font-size: 0.75rem;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border-bottom: 1px solid #e5e7eb;
`;

const Tbody = styled.tbody``;

const Tr = styled.tr`
  &:hover {
    background-color: #f9fafb;
  }

  border-bottom: 1px solid #e5e7eb;

  &:last-child {
    border-bottom: none;
  }
`;

const Td = styled.td`
  padding: 1rem;
  font-size: 0.875rem;
  color: #111827;
`;

const EmployeeName = styled.div`
  font-weight: 600;
  color: #111827;
`;

const EmployeeInfo = styled.div`
  font-size: 0.75rem;
  color: #6b7280;
  margin-top: 0.25rem;
`;

const ActionButtons = styled.div`
  display: flex;
  gap: 0.5rem;
`;

const Button = styled.button<{
  $variant?: "primary" | "danger" | "warning" | "success";
}>`
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.2s;

  ${({ $variant = "primary" }) => {
    switch ($variant) {
      case "danger":
        return `
          background-color: #FEE2E2;
          color: #991B1B;
          &:hover {
            background-color: #FECACA;
          }
        `;
      case "warning":
        return `
          background-color: #FEF3C7;
          color: #92400E;
          &:hover {
            background-color: #FDE68A;
          }
        `;
      case "success":
        return `
          background-color: #D1FAE5;
          color: #065F46;
          &:hover {
            background-color: #A7F3D0;
          }
        `;
      default:
        return `
          background-color: #DBEAFE;
          color: #1E40AF;
          &:hover {
            background-color: #BFDBFE;
          }
        `;
    }
  }}
`;

const EmptyState = styled.div`
  padding: 3rem;
  text-align: center;
  color: #6b7280;
`;

export default function EmployeeTable({
  employees,
  onEdit,
  onDelete,
  onTerminate,
  onReactivate,
  loading,
}: EmployeeTableProps) {
  if (loading) {
    return (
      <TableContainer>
        <EmptyState>Carregando funcionários...</EmptyState>
      </TableContainer>
    );
  }

  if (employees.length === 0) {
    return (
      <TableContainer>
        <EmptyState>Nenhum funcionário encontrado.</EmptyState>
      </TableContainer>
    );
  }

  return (
    <TableContainer>
      <Table>
        <Thead>
          <Tr>
            <Th>Funcionário</Th>
            <Th>CPF</Th>
            <Th>Cargo</Th>
            <Th>Departamento</Th>
            <Th>Salário</Th>
            <Th>Status</Th>
            <Th>Data de Contratação</Th>
            <Th>Ações</Th>
          </Tr>
        </Thead>
        <Tbody>
          {employees.map((employee) => (
            <Tr key={employee.id}>
              <Td>
                <EmployeeName>{employee.name}</EmployeeName>
                {employee.email && (
                  <EmployeeInfo>{employee.email}</EmployeeInfo>
                )}
                {employee.phone && (
                  <EmployeeInfo>{employee.phone}</EmployeeInfo>
                )}
              </Td>
              <Td>{employee.cpf}</Td>
              <Td>{employee.position_name}</Td>
              <Td>
                <DepartmentBadge
                  department={employee.position_department}
                  displayText={employee.position_department}
                />
              </Td>
              <Td>{employee.salary_formatted}</Td>
              <Td>
                <EmployeeStatusBadge
                  status={employee.employment_status}
                  displayText={employee.employment_status_display}
                />
              </Td>
              <Td>
                {employee.hire_date
                  ? new Date(
                      employee.hire_date + "T00:00:00",
                    ).toLocaleDateString("pt-BR")
                  : "-"}
              </Td>
              <Td>
                <ActionButtons>
                  {onEdit && (
                    <Button $variant="primary" onClick={() => onEdit(employee)}>
                      Editar
                    </Button>
                  )}
                  {employee.employment_status === "ACTIVE" && onTerminate && (
                    <Button
                      $variant="danger"
                      onClick={() => onTerminate(employee)}
                    >
                      Demitir
                    </Button>
                  )}
                  {employee.employment_status === "TERMINATED" &&
                    onReactivate && (
                      <Button
                        $variant="success"
                        onClick={() => onReactivate(employee)}
                      >
                        Reativar
                      </Button>
                    )}
                  {onDelete && (
                    <Button
                      $variant="danger"
                      onClick={() => onDelete(employee)}
                    >
                      Excluir
                    </Button>
                  )}
                </ActionButtons>
              </Td>
            </Tr>
          ))}
        </Tbody>
      </Table>
    </TableContainer>
  );
}
