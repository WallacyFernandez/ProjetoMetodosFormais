"use client";

import React, { useContext, useEffect, useState } from "react";
import { styled } from "styled-components";
import { IsSidebarOnContext } from "@/context/IsSidebarOnContext";
import {
  GetTransactions,
  CreateTransaction,
  DeleteTransaction,
} from "@/services/FinanceServices";
import { GetCategories } from "@/services/FinanceServices";
import type { Transaction, TransactionCreate, Category } from "@/types/finance";
import PageHeader from "@/components/molecules/PageHeader";
import TransactionForm from "@/components/molecules/TransactionForm";
import TransactionTable from "@/components/molecules/TransactionTable";
import { toast } from "react-toastify";

interface TransacoesContainerProps {
  $isCollapsed: boolean;
}

const Container = styled.div<TransacoesContainerProps>`
  background-color: ${({ theme }) => theme.colors.backgroundSecondary};
  margin-left: ${({ $isCollapsed }) => ($isCollapsed ? "80px" : "280px")};
  min-height: 100vh;
  padding: 2rem;
  transition: margin-left 0.3s ease;
`;

const Content = styled.div`
  max-width: 1200px;
  margin: 0 auto;
`;

const Grid = styled.div<{ $showForm: boolean }>`
  display: grid;
  grid-template-columns: ${({ $showForm }) => ($showForm ? "1fr 2fr" : "1fr")};
  gap: ${({ $showForm }) => ($showForm ? "2rem" : "0")};
  margin-top: 2rem;
  transition: all 0.3s ease;

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
`;

export default function TransacoesContainer() {
  const { isCollapsed } = useContext(IsSidebarOnContext);
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingTransaction, setEditingTransaction] =
    useState<Transaction | null>(null);

  const loadData = async () => {
    try {
      setLoading(true);
      const [transactionsData, categoriesData] = await Promise.all([
        GetTransactions(),
        GetCategories(),
      ]);

      setTransactions(transactionsData || []);
      setCategories(categoriesData || []);
    } catch (error) {
      console.error("Erro ao carregar dados:", error);
      toast.error("Erro ao carregar dados");
      setTransactions([]);
      setCategories([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleCreateTransaction = async (
    transactionData: TransactionCreate,
  ) => {
    try {
      const newTransaction = await CreateTransaction(transactionData);
      setTransactions((prev) => {
        const currentTransactions = Array.isArray(prev) ? prev : [];
        return [newTransaction, ...currentTransactions];
      });
      setShowForm(false);
      toast.success("Transação criada com sucesso!");
    } catch (error) {
      console.error("Erro ao criar transação:", error);
      toast.error("Erro ao criar transação");
    }
  };

  const handleDeleteTransaction = async (id: string) => {
    try {
      await DeleteTransaction(id);
      setTransactions((prev) => {
        const currentTransactions = Array.isArray(prev) ? prev : [];
        return currentTransactions.filter((t) => t.id !== id);
      });
      toast.success("Transação excluída com sucesso!");
    } catch (error) {
      console.error("Erro ao excluir transação:", error);
      toast.error("Erro ao excluir transação");
    }
  };

  const handleEditTransaction = (transaction: Transaction) => {
    setEditingTransaction(transaction);
    setShowForm(true);
  };

  if (loading) {
    return (
      <Container $isCollapsed={isCollapsed}>
        <Content>
          <PageHeader
            $title="Transações"
            $subtitle="Gerencie suas transações financeiras"
          />
          <div style={{ textAlign: "center", padding: "2rem" }}>
            Carregando...
          </div>
        </Content>
      </Container>
    );
  }

  return (
    <Container $isCollapsed={isCollapsed}>
      <Content>
        <PageHeader
          $title="Transações"
          $subtitle="Gerencie suas transações financeiras"
          actionButton={{
            text: showForm ? "Ver Lista" : "Nova Transação",
            onClick: () => setShowForm(!showForm),
          }}
        />

        <Grid $showForm={showForm}>
          {showForm && (
            <div>
              <TransactionForm
                categories={categories}
                onSubmit={handleCreateTransaction}
                editingTransaction={editingTransaction}
                onCancel={() => {
                  setShowForm(false);
                  setEditingTransaction(null);
                }}
              />
            </div>
          )}

          <div>
            <TransactionTable
              transactions={transactions}
              onEdit={handleEditTransaction}
              onDelete={handleDeleteTransaction}
            />
          </div>
        </Grid>
      </Content>
    </Container>
  );
}
