import { useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { TrendingUp, TrendingDown, Minus, Percent, Package } from 'lucide-react';
import type { ProfitabilityRow } from '../hooks/useProfitability';

interface ProfitabilitySummaryProps {
  rows: ProfitabilityRow[];
}

export default function ProfitabilitySummary({ rows }: ProfitabilitySummaryProps) {
  const navigate = useNavigate();

  const { avgMargin, mostProfitable, leastProfitable, activeCount, totalCount, excludedCount } =
    useMemo(() => {
      const withCost = rows.filter((r) => r.costAvailable && r.marginPercent !== null);
      const allProducts = rows; // already filtered to active in the hook

      const avg =
        withCost.length > 0
          ? withCost.reduce((sum, r) => sum + (r.marginPercent ?? 0), 0) / withCost.length
          : null;

      const sorted = [...withCost].sort((a, b) => b.marginPercent! - a.marginPercent!);

      const most = sorted[0] ?? null;
      // Alphabetical tie-break for most
      let least = sorted[sorted.length - 1] ?? null;
      // Alphabetical tie-break for least: find min margin, then first alphabetically
      if (sorted.length > 1) {
        const minMargin = least!.marginPercent!;
        const tied = sorted.filter((r) => r.marginPercent === minMargin);
        tied.sort((a, b) => a.product.name.localeCompare(b.product.name));
        least = tied[0] ?? least;
      }

      return {
        avgMargin: avg !== null ? Math.round(avg * 100) / 100 : null,
        mostProfitable: most,
        leastProfitable: least,
        activeCount: allProducts.length,
        totalCount: rows.length,
        excludedCount: allProducts.length - withCost.length,
      };
    }, [rows]);

  const cards = [
    {
      icon: Percent,
      iconColor: 'text-indigo-600',
      bgColor: 'bg-indigo-50',
      label: 'Average Margin',
      value: avgMargin !== null ? `${avgMargin.toFixed(2)}%` : '\u2014',
      subtitle:
        excludedCount > 0
          ? `${excludedCount} excluded \u2014 cost unavailable`
          : undefined,
    },
    {
      icon: TrendingUp,
      iconColor: 'text-green-600',
      bgColor: 'bg-green-50',
      label: 'Most Profitable',
      value: mostProfitable ? (
        <button
          onClick={() => navigate(`/app/products/${mostProfitable.product.id}`)}
          className="font-semibold text-green-700 hover:underline"
        >
          {mostProfitable.product.name}
        </button>
      ) : (
        <span className="text-gray-400">No products</span>
      ),
      subtitle: mostProfitable ? `${mostProfitable.marginPercent!.toFixed(2)}%` : undefined,
    },
    {
      icon: TrendingDown,
      iconColor: 'text-red-600',
      bgColor: 'bg-red-50',
      label: 'Least Profitable',
      value: leastProfitable ? (
        <button
          onClick={() => navigate(`/app/products/${leastProfitable.product.id}`)}
          className="font-semibold text-red-700 hover:underline"
        >
          {leastProfitable.product.name}
        </button>
      ) : (
        <span className="text-gray-400">No products</span>
      ),
      subtitle: leastProfitable ? `${leastProfitable.marginPercent!.toFixed(2)}%` : undefined,
    },
    {
      icon: Package,
      iconColor: 'text-blue-600',
      bgColor: 'bg-blue-50',
      label: 'Active Products',
      value: activeCount,
      subtitle: `out of ${totalCount} total`,
    },
  ];

  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
      {cards.map((card) => (
        <div
          key={card.label}
          className="rounded-xl border border-gray-200 bg-white p-4 transition-shadow hover:shadow-md"
        >
          <div className="mb-2 flex items-center gap-2">
            <div className={`rounded-lg p-1.5 ${card.bgColor}`}>
              <card.icon className={`h-4 w-4 ${card.iconColor}`} />
            </div>
            <p className="text-xs font-medium uppercase tracking-wider text-gray-500">
              {card.label}
            </p>
          </div>
          <div className="text-xl font-bold text-gray-900">{card.value}</div>
          {card.subtitle && (
            <p className="mt-0.5 text-xs text-gray-500">{card.subtitle}</p>
          )}
        </div>
      ))}
    </div>
  );
}
