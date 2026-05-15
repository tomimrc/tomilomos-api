import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Plus } from 'lucide-react';
import { useSales } from '../hooks/useSales';
import SalesTable from '../components/SalesTable';
import Button from '@/components/ui/Button';
import LoadingSkeleton from '@/components/shared/LoadingSkeleton';
import EmptyState from '@/components/shared/EmptyState';
import ErrorState from '@/components/shared/ErrorState';

export default function SalesHistoryPage() {
  const navigate = useNavigate();
  const { data: sales, isLoading, isError, refetch } = useSales();

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -12 }}
      transition={{ duration: 0.2 }}
    >
      {/* Header */}
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Sales History</h2>
          <p className="text-sm text-gray-500">
            Review past sales and track revenue
          </p>
        </div>
        <Button onClick={() => navigate('/app/sales')}>
          <Plus className="h-4 w-4" />
          New Sale
        </Button>
      </div>

      {/* Content states */}
      {isLoading && <LoadingSkeleton variant="table-row" rows={6} />}

      {isError && !isLoading && (
        <ErrorState onRetry={() => refetch()} />
      )}

      {!isLoading && !isError && sales?.length === 0 && (
        <EmptyState
          title="No sales recorded yet"
          description="Register your first sale to start tracking revenue."
          actionLabel="Register your first sale"
          onAction={() => navigate('/app/sales')}
        />
      )}

      {!isLoading && !isError && sales && sales.length > 0 && (
        <SalesTable sales={sales} />
      )}
    </motion.div>
  );
}
