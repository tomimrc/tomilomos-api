import { useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell,
  LabelList,
} from 'recharts';
import type { ProfitabilityItem, FilterType } from '../types';
import { formatCurrency } from '@/lib/formatters';

interface ProfitabilityChartProps {
  items: ProfitabilityItem[];
  filter: FilterType;
  loading?: boolean;
}

export default function ProfitabilityChart({
  items,
  filter,
  loading = false,
}: ProfitabilityChartProps) {
  const navigate = useNavigate();

  // Apply filter and take top 10
  const chartData = useMemo(() => {
    let filtered = items.filter((i) => i.marginPercent !== null);

    if (filter === 'profitable')
      filtered = filtered.filter((i) => (i.marginPercent ?? 0) > 0);
    else if (filter === 'unprofitable')
      filtered = filtered.filter((i) => (i.marginPercent ?? 0) < 0);

    return filtered
      .sort((a, b) => (b.marginPercent ?? 0) - (a.marginPercent ?? 0))
      .slice(0, 10)
      .map((item) => ({
        name:
          item.product.name.length > 20
            ? item.product.name.slice(0, 18) + '…'
            : item.product.name,
        fullName: item.product.name,
        marginPercent: item.marginPercent,
        margin: item.margin,
        salePrice: parseFloat(item.product.sale_price),
        costPrice: item.cost ? parseFloat(item.cost.total_cost) : 0,
        productId: item.product.id,
      }));
  }, [items, filter]);

  const chartTitle =
    filter === 'profitable'
      ? 'Top Profitable Products'
      : filter === 'unprofitable'
        ? 'Top Unprofitable Products'
        : chartData.length < 10
          ? `All Products (${chartData.length})`
          : 'Top 10 Products by Margin';

  // Compute axis domain
  const minMargin = Math.min(...chartData.map((d) => d.marginPercent ?? 0), 0);

  if (loading) {
    return (
      <div className="mb-6 rounded-xl border border-gray-200 bg-white p-6">
        <div className="mb-4 h-5 w-48 animate-pulse rounded bg-gray-200" />
        <div className="space-y-3">
          {Array.from({ length: 6 }).map((_, i) => (
            <div
              key={i}
              className="h-6 animate-pulse rounded bg-gray-100"
              style={{ width: `${60 - i * 8}%` }}
            />
          ))}
        </div>
      </div>
    );
  }

  if (chartData.length === 0) {
    return (
      <div className="mb-6 rounded-xl border border-gray-200 bg-white p-6">
        <h3 className="mb-1 text-sm font-semibold text-gray-700">
          {chartTitle}
        </h3>
        <div className="flex h-48 items-center justify-center">
          <p className="text-sm text-gray-400">No margin data available</p>
        </div>
      </div>
    );
  }

  return (
    <div className="mb-6 rounded-xl border border-gray-200 bg-white p-6">
      <h3 className="mb-4 text-sm font-semibold text-gray-700">
        {chartTitle}
      </h3>
      <ResponsiveContainer width="100%" height={chartData.length * 40 + 40}>
        <BarChart
          data={chartData}
          layout="vertical"
          margin={{ top: 5, right: 60, left: 10, bottom: 5 }}
          onClick={(data) => {
            if (data?.activePayload?.[0]?.payload?.productId) {
              navigate(
                `/app/products/${data.activePayload[0].payload.productId}`
              );
            }
          }}
        >
          <XAxis
            type="number"
            domain={[minMargin < 0 ? minMargin * 1.1 : 0, 'auto']}
            tickFormatter={(v) => `${v.toFixed(0)}%`}
            tick={{ fontSize: 12 }}
          />
          <YAxis
            type="category"
            dataKey="name"
            width={130}
            tick={{ fontSize: 12 }}
          />
          <Tooltip
            formatter={(value: number, name: string) => {
              if (name === 'marginPercent') return [`${value.toFixed(2)}%`, 'Margin %'];
              return [value, name];
            }}
            labelFormatter={(label: string, payload: unknown[]) => {
              const fullName = (payload as { payload: { fullName: string } }[])[0]?.payload?.fullName;
              return fullName || label;
            }}
            contentStyle={{
              fontSize: '12px',
              borderRadius: '8px',
              border: '1px solid #e5e7eb',
            }}
          />
          <Bar
            dataKey="marginPercent"
            radius={[0, 4, 4, 0]}
            cursor="pointer"
            barSize={20}
          >
            {chartData.map((entry, idx) => (
              <Cell
                key={idx}
                fill={
                  (entry.marginPercent ?? 0) > 0 ? '#16a34a' : '#dc2626'
                }
              />
            ))}
            <LabelList
              dataKey="marginPercent"
              position="right"
              formatter={(v: number) => `${v.toFixed(1)}%`}
              style={{ fontSize: '12px', fill: '#6b7280' }}
            />
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
