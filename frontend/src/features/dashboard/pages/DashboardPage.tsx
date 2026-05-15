import { useState } from 'react';
import { motion } from 'framer-motion';
import { useProfitabilityData, type FilterType } from '../hooks/useProfitabilityData';
import ProfitSummaryCards from '../components/ProfitSummaryCards';
import ProfitabilityChart from '../components/ProfitabilityChart';
import ProfitabilityTable from '../components/ProfitabilityTable';
import LoadingSkeleton from '@/components/shared/LoadingSkeleton';
import ErrorState from '@/components/shared/ErrorState';
import EmptyState from '@/components/shared/EmptyState';

export default function DashboardPage() {
  const { items, isLoading, isError, error, refetch, summary } =
    useProfitabilityData();
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
        <h2 className="text-2xl font-bold text-gray-900">
          Profitability Dashboard
        </h2>
        <p className="text-sm text-gray-500">
          Product-level profit margins calculated from recipe costs and sale
          prices
        </p>
      </div>

      {/* Global loading */}
      {isLoading && !items.length && (
        <>
          <ProfitSummaryCards summary={summary} loading />
          <LoadingSkeleton variant="table-row" rows={6} />
        </>
      )}

      {/* Global error */}
      {isError && !isLoading && (
        <ErrorState
          message={error?.message || 'Failed to load profitability data'}
          onRetry={() => refetch()}
        />
      )}

      {/* Empty state */}
      {!isLoading && !isError && items.length === 0 && (
        <EmptyState
          title="No products yet"
          description="Create products with recipes to see profitability data here."
        />
      )}

      {/* Data loaded */}
      {!isLoading && !isError && items.length > 0 && (
        <>
          <ProfitSummaryCards summary={summary} loading={isLoading} />

          <div className="grid gap-6 lg:grid-cols-5">
            <div className="lg:col-span-2">
              <ProfitabilityChart
                items={items}
                filter={filter}
                loading={isLoading}
              />
            </div>
            <div className="lg:col-span-3">
              <ProfitabilityTable
                items={items}
                filter={filter}
                onFilterChange={setFilter}
              />
            </div>
          </div>
        </>
      )}
    </motion.div>
  );
}
