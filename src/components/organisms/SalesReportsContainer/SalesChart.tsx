"use client";

import React from "react";
import styled from "styled-components";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
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

interface SalesChartProps {
  data: Array<{
    period: string;
    period_key: string;
    total_quantity: number;
    total_revenue: number;
    revenue_formatted: string;
  }>;
  period: "daily" | "weekly" | "monthly";
  isWeekdayChart?: boolean;
}

export default function SalesChart({
  data,
  period,
  isWeekdayChart = false,
}: SalesChartProps) {
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
          Nenhum dado disponível para o período selecionado
        </div>
      </ChartContainer>
    );
  }

  const CustomTooltipComponent = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <CustomTooltip>
          <TooltipLabel>{label}</TooltipLabel>
          <TooltipValue>Receita: {data.revenue_formatted}</TooltipValue>
          <TooltipValue>
            Quantidade: {data.total_quantity} unidades
          </TooltipValue>
        </CustomTooltip>
      );
    }
    return null;
  };

  const formatXAxisLabel = (value: string) => {
    if (isWeekdayChart) {
      return value.substring(0, 3); // Seg, Ter, Qua, etc.
    }

    if (period === "daily") {
      return value.substring(0, 5); // DD/MM
    } else if (period === "weekly") {
      return value.replace("Semana ", "S"); // S1, S2, etc.
    } else {
      return value.substring(0, 3); // Jan, Fev, etc.
    }
  };

  return (
    <ChartContainer>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart
          data={data}
          margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
          <XAxis
            dataKey="period"
            tickFormatter={formatXAxisLabel}
            stroke="#6B7280"
            fontSize={12}
          />
          <YAxis
            tickFormatter={(value) => `R$ ${(value / 1000).toFixed(0)}k`}
            stroke="#6B7280"
            fontSize={12}
          />
          <Tooltip content={<CustomTooltipComponent />} />
          <Line
            type="monotone"
            dataKey="total_revenue"
            stroke="#10B981"
            strokeWidth={3}
            dot={{ fill: "#10B981", strokeWidth: 2, r: 4 }}
            activeDot={{ r: 6, stroke: "#10B981", strokeWidth: 2 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </ChartContainer>
  );
}
