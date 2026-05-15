import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  TrendingUp,
  TrendingDown,
  DollarSign,
  Package,
  Percent,
} from 'lucide-react';
import type { ProfitabilityItem } from '../types';
import { formatCurrency } from '@/lib/formatters';

interface SummaryData {
  avgMargin: number | null;
  mostProfitable: ProfitabilityItem | null;
  leastProfitable: ProfitabilityItem | null;
  activeProducts: number;
  totalProducts: number;
  excludedCount: number;
}

interface ProfitSummaryCardsProps {
  summary: SummaryData;
  loading?: boolean;
}

function CountUpValue({
  value,
  suffix = '',
}: {
  value: string;
  suffix?: string;
}) {
  return (
    <motion.span
      key={value}
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      {value}
      {suffix}
    </motion.span>
  );
}

export default function ProfitSummaryCards({
  summary,
  loading = false,
}: ProfitSummaryCardsProps) {
  if (loading) {
    return (
      <div className="mb-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {Array.from({ length: 4 }).map((_, i) => (
          <div
            key={i}
            className="animate-pulse rounded-xl border border-gray-200 bg-white p-5"
          >
            <div className="mb-3 h-4 w-20 rounded bg-gray-200" />
            <div className="mb-2 h-8 w-24 rounded bg-gray-200" />
            <div className="h-3 w-32 rounded bg-gray-100" />
          </div>
        ))}
      </div>
    );
  }

  const cards = [
    {
      icon: Percent,
      label: 'Average Margin',
      value:
        summary.avgMargin !== null
          ? `${summary.avgMargin.toFixed(2)}%`
          : '—',
      subtitle:
        summary.excludedCount > 0
          ? `${summary.excludedCount} excluded — cost unavailable`
          : undefined,
      color: 'text-indigo-600',
    },
    {
      icon: TrendingUp,
      label: 'Most Profitable',
      value: summary.mostProfitable
        ? `${summary.mostProfitable.marginPercent?.toFixed(1) ?? '—'}%`
        : '—',
      subtitle: summary.mostProfitable?.product.name || 'No products',
      link: summary.mostProfitable
        ? `/app/products/${summary.mostProfitable.product.id}`
        : undefined,
      color: 'text-green-600',
    },
    {
      icon: TrendingDown,
      label: 'Least Profitable',
      value: summary.leastProfitable
        ? `${summary.leastProfitable.marginPercent?.toFixed(1) ?? '—'}%`
        : '—',
      subtitle: summary.leastProfitable?.product.name || 'No products',
      link: summary.leastProfitable
        ? `/app/products/${summary.leastProfitable.product.id}`
        : undefined,
      color: 'text-red-600',
    },
    {
      icon: Package,
      label: 'Active Products',
      value: `${summary.activeProducts}`,
      subtitle: `out of ${summary.totalProducts} total`,
      color: 'text-blue-600',
    },
  ];

  return (
    <div className="mb-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
      {cards.map((card) => (
        <motion.div
          key={card.label}
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.2 }}
          whileHover={{ scale: 1.02, boxShadow: '0 4px 12px rgba(0,0,0,0.08)' }}
          className="rounded-xl border border-gray-200 bg-white p-5 shadow-sm transition-shadow"
        >
          <div className="mb-1 flex items-center gap-2">
            <card.icon className={`h-4 w-4 ${card.color}`} />
            <p className="text-xs font-medium uppercase tracking-wider text-gray-500">
              {card.label}
            </p>
          </div>

          <p className="text-2xl font-bold text-gray-900">
            <CountUpValue value={card.value} />
          </p>

          {card.subtitle && (
            <p className="mt-1 text-xs text-gray-400">
              {card.link ? (
                <Link
                  to={card.link}
                  className="hover:text-gray-600 hover:underline"
                >
                  {card.subtitle}
                </Link>
              ) : (
                card.subtitle
              )}
            </p>
          )}
        </motion.div>
      ))}
    </div>
  );
}
