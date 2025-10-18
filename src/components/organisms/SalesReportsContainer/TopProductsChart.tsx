"use client";

import React from "react";
import styled from "styled-components";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { formatCurrency } from "@/services/GameServices";

const ChartContainer = styled.div`
  width: 100%;
  height: 300px;
`;

const CustomTooltip = styled.div`
  background: ${(props) => props.theme.colors.backgroundSecondary};
  border: 1px solid ${(props) => props.theme.colors.border};
  border-radius: 8px;
  padding: 0.75rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
`;

const TooltipLabel = styled.div`
  font-weight: 600;
  color: ${(props) => props.theme.colors.textPrimary};
  margin-bottom: 0.5rem;
`;

const TooltipValue = styled.div`
  color: ${(props) => props.theme.colors.textSecondary};
  font-size: 0.875rem;
`;

interface TopProductsChartProps {
  data: Array<{
    product__id: string;
    product__name: string;
    product__category__name: string;
    product__category__color: string;
    total_quantity: number;
    total_revenue: number;
  }>;
}

export default function TopProductsChart({ data }: TopProductsChartProps) {
  if (!data || data.length === 0) {
    return (
      <ChartContainer>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            height: "100%",
            color: "#6B7280",
            fontSize: "0.875rem",
          }}
        >
          Nenhum produto vendido no período selecionado
        </div>
      </ChartContainer>
    );
  }

  const CustomTooltipComponent = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <CustomTooltip>
          <TooltipLabel>{data.product__name}</TooltipLabel>
          <TooltipValue>
            Receita: {formatCurrency(data.total_revenue)}
          </TooltipValue>
          <TooltipValue>
            Quantidade: {data.total_quantity} unidades
          </TooltipValue>
          <TooltipValue>Categoria: {data.product__category__name}</TooltipValue>
        </CustomTooltip>
      );
    }
    return null;
  };

  const formatProductName = (name: string) => {
    if (name.length > 12) {
      return name.substring(0, 12) + "...";
    }
    return name;
  };

  return (
    <ChartContainer>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={data}
          margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
          <XAxis
            dataKey="product__name"
            tickFormatter={formatProductName}
            stroke="#6B7280"
            fontSize={12}
            angle={-45}
            textAnchor="end"
            height={80}
          />
          <YAxis
            tickFormatter={(value) => `R$ ${(value / 1000).toFixed(0)}k`}
            stroke="#6B7280"
            fontSize={12}
          />
          <Tooltip content={<CustomTooltipComponent />} />
          <Bar dataKey="total_revenue" fill="#3B82F6" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </ChartContainer>
  );
}
