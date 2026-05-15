import { useEffect } from 'react';
import { motion } from 'framer-motion';
import { Eye } from 'lucide-react';
import { useRawMaterials } from '@/features/raw-materials/hooks/useRawMaterials';
import StockDashboardTable from '../components/StockDashboardTable';
import LoadingSkeleton from '@/components/shared/LoadingSkeleton';
import EmptyState from '@/components/shared/EmptyState';
import ErrorState from '@/components/shared/ErrorState';

export default function StockDashboardPage() {
  const { data: materials, isLoading, isError, refetch } = useRawMaterials();

  // Ensure fresh data on mount (e.g., returning from stock adjustment)
  useEffect(() => {
    refetch();
  }, [refetch]);

  const materialList = materials ?? [];

  const lowStockCount = materialList.filter((m) => {
    const stock = parseFloat(m.current_stock);
    return !isNaN(stock) && stock > 0 && stock <= 10;
  }).length;

  const outOfStockCount = materialList.filter((m) => {
    const stock = parseFloat(m.current_stock);
    return !isNaN(stock) && stock === 0;
  }).length;

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
          <Eye className="h-6 w-6 text-indigo-600" />
          <h2 className="text-2xl font-bold text-gray-900">Stock Monitor</h2>
        </div>
        <p className="mt-1 text-sm text-gray-500">
          Track raw material levels and identify what needs restocking
        </p>
      </div>

      {/* Content states */}
      {isLoading && <LoadingSkeleton variant="table-row" rows={6} />}

      {isError && !isLoading && (
        <ErrorState onRetry={() => refetch()} />
      )}

      {!isLoading && !isError && materialList.length === 0 && (
        <EmptyState
          title="No raw materials to monitor"
          description="Create raw materials first to start tracking stock levels."
          actionLabel="Create raw materials"
          onAction={() => (window.location.href = '/app/raw-materials/new')}
        />
      )}

      {!isLoading && !isError && materialList.length > 0 && (
        <StockDashboardTable
          materials={materialList}
          lowStockCount={lowStockCount}
          outOfStockCount={outOfStockCount}
        />
      )}
    </motion.div>
  );
}
