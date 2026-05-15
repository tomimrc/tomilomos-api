import { useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Cell,
  ResponsiveContainer,
  LabelList,
} from 'recharts';
import type { ProfitabilityRow } from '../hooks/useProfitability';
import { formatCurrency } from '@/lib/formatters';

interface ProfitabilityChartProps {
  rows: ProfitabilityRow[];
  filter: 'all' | 'profitable' | 'unprofitable';
}

interface ChartData {
  name: string;
  fullName: string;
  margin: number;
  productId: string;
  salePrice: string;
  costPrice: string | null;
}

export default function ProfitabilityChart({ rows, filter }: ProfitabilityChartProps) {
  const navigate = useNavigate();

  const chartData: ChartData[] = useMemo(() => {
    let filtered = rows.filter((r) => r.marginPercent !== null);

    if (filter === 'profitable') {
      filtered = filtered.filter((r) => r.marginPercent! > 0);
    } else if (filter === 'unprofitable') {
      filtered = filtered.filter((r) => r.marginPercent! < 0);
    }

    const sorted = [...filtered].sort(
      (a, b) => b.marginPercent! - a.marginPercent!
    );

    const top10 = sorted.slice(0, 10);

    return top10.map((r) => ({
      name:
        r.product.name.length > 20
          ? r.product.name.slice(0, 18) + '...'
          : r.product.name,
      fullName: r.product.name,
      margin: r.marginPercent!,
      productId: r.product.id,
      salePrice: r.product.sale_price,
      costPrice: r.cost ? r.cost.total_cost : null,
    }));
  }, [rows, filter]);

  const title =
    filter === 'all'
      ? 'Top Products by Margin'
      : filter === 'profitable'
        ? 'Top Profitable Products'
        : 'Unprofitable Products';

  if (chartData.length === 0) {
    return (
      <div className="rounded-xl border border-gray-200 bg-white p-6">
        <h3 className="mb-4 text-lg font-semibold text-gray-900">{title}</h3>
        <div className="flex h-64 items-center justify-center">
          <p className="text-sm text-gray-400">No margin data available</p>
        </div>
      </div>
    );
  }

  return (
    <div className="rounded-xl border border-gray-200 bg-white p-6">
      <h3 className="mb-4 text-lg font-semibold text-gray-900">
        {title} (Top {chartData.length})
      </h3>
      <ResponsiveContainer width="100%" height={Math.max(250, chartData.length * 40)}>
        <BarChart
          data={chartData}
          layout="vertical"
          margin={{ top: 5, right: 40, bottom: 5, left: 10 }}
          onClick={(data) => {
            if (data?.activePayload?.[0]) {
              const payload = data.activePayload[0].payload as ChartData;
              navigate(`/app/products/${payload.productId}`);
            }
          }}
        >
          <XAxis
            type="number"
            tickFormatter={(v: number) => `${v}%`}
            tick={{ fontSize: 12 }}
          />
          <YAxis
            type="category"
            dataKey="name"
            tick={{ fontSize: 12 }}
            width={140}
          />
          <Tooltip
            formatter={(_value: number, name: string) => {
              const entry = chartData.find((d) => d.name === name);
              return ['', '']; // unused, custom content below
            }}
            content={({ active, payload }) => {
              if (!active || !payload?.[0]) return null;
              const data = payload[0].payload as ChartData;
              return (
                <div className="rounded-lg border border-gray-200 bg-white px-3 py-2 text-xs shadow-lg">
                  <p className="font-semibold text-gray-900">{data.fullName}</p>
                  <p className="text-gray-500">
                    Sale: {formatCurrency(data.salePrice)}
                  </p>
                  <p className="text-gray-500">
                    Cost:{' '}
                    {data.costPrice ? formatCurrency(data.costPrice) : '\u2014'}
                  </p>
                  <p className="font-semibold text-indigo-600">
                    Margin: {data.margin.toFixed(2)}%
                  </p>
                </div>
              );
            }}
          />
          <Bar dataKey="margin" radius={[0, 4, 4, 0]} barSize={20}>
            {chartData.map((entry, index) => (
              <Cell
                key={index}
                fill={entry.margin >= 0 ? '#16a34a' : '#dc2626'}
                className="cursor-pointer"
              />
            ))}
            <LabelList
              dataKey="margin"
              position="right"
              formatter={(v: number) => `${v.toFixed(1)}%`}
              style={{ fontSize: 12, fontWeight: 600 }}
            />
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
