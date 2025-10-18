"use client";

import React from "react";
import styled from "styled-components";
import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Tooltip,
  Legend,
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

const LegendContainer = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 1rem;
`;

const LegendItem = styled.div`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.75rem;
`;

const LegendColor = styled.div<{ color: string }>`
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: ${(props) => props.color};
`;

interface CategoryChartProps {
  data: Array<{
    product__category__name: string;
    product__category__color: string;
    total_quantity: number;
    total_revenue: number;
  }>;
}

export default function CategoryChart({ data }: CategoryChartProps) {
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
          Nenhuma categoria com vendas no período selecionado
        </div>
      </ChartContainer>
    );
  }

  const CustomTooltipComponent = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <CustomTooltip>
          <TooltipLabel>{data.name}</TooltipLabel>
          <TooltipValue>Receita: {formatCurrency(data.value)}</TooltipValue>
          <TooltipValue>
            Quantidade: {data.total_quantity} unidades
          </TooltipValue>
        </CustomTooltip>
      );
    }
    return null;
  };

  const chartData = data.map((item) => ({
    name: item.product__category__name,
    value: item.total_revenue,
    total_quantity: item.total_quantity,
    color: item.product__category__color,
  }));

  const COLORS = chartData.map((item) => item.color);

  return (
    <ChartContainer>
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name, percent }) =>
              `${name} ${(percent * 100).toFixed(0)}%`
            }
            outerRadius={80}
            fill="#8884d8"
            dataKey="value"
          >
            {chartData.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={COLORS[index % COLORS.length]}
              />
            ))}
          </Pie>
          <Tooltip content={<CustomTooltipComponent />} />
        </PieChart>
      </ResponsiveContainer>

      <LegendContainer>
        {chartData.map((item, index) => (
          <LegendItem key={index}>
            <LegendColor color={item.color} />
            <span>{item.name}</span>
          </LegendItem>
        ))}
      </LegendContainer>
    </ChartContainer>
  );
}
