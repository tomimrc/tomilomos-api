import { useState } from 'react';
import { motion } from 'framer-motion';
import { TrendingUp } from 'lucide-react';
import { useProfitability } from '../hooks/useProfitability';
import ProfitabilitySummary from '../components/ProfitabilitySummary';
import ProfitabilityChart from '../components/ProfitabilityChart';
import ProfitabilityTable from '../components/ProfitabilityTable';
import LoadingSkeleton from '@/components/shared/LoadingSkeleton';
import ErrorState from '@/components/shared/ErrorState';
import EmptyState from '@/components/shared/EmptyState';

type FilterType = 'all' | 'profitable' | 'unprofitable';

export default function ProfitabilityPage() {
  const { rows, isLoading, isError, refetch } = useProfitability();
  const [filter, setFilter] = useState<FilterType>('all');

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -12 }}
      transition={{ duration: 0.2 }}
    >
      {/* Header */}
      <div className="mb-6">
        <div className="flex items-center gap-2">
          <TrendingUp className="h-6 w-6 text-indigo-600" />
          <h2 className="text-2xl font-bold text-gray-900">Profitability</h2>
        </div>
        <p className="mt-1 text-sm text-gray-500">
          Analyze product margins and identify your most and least profitable items
        </p>
      </div>

      {/* Content states */}
      {isLoading && (
        <div className="space-y-6">
          <LoadingSkeleton variant="table-row" rows={1} />
          <LoadingSkeleton variant="table-row" rows={6} />
        </div>
      )}

      {isError && !isLoading && <ErrorState onRetry={() => refetch()} />}

      {!isLoading && !isError && rows.length === 0 && (
        <EmptyState
          title="No products to analyze"
          description="Create products with recipes to see profitability data."
          actionLabel="Create a product"
          onAction={() => (window.location.href = '/app/products/new')}
        />
      )}

      {!isLoading && !isError && rows.length > 0 && (
        <div className="space-y-6">
          {/* Summary Cards */}
          <ProfitabilitySummary rows={rows} />

          {/* Chart */}
          <ProfitabilityChart rows={rows} filter={filter} />

          {/* Table with filters */}
          <ProfitabilityTable
            rows={rows}
            filter={filter}
            onFilterChange={setFilter}
          />
        </div>
      )}
    </motion.div>
  );
}
