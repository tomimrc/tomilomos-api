import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Plus } from 'lucide-react';
import { useProducts } from '../hooks/useProducts';
import { useDeleteProduct } from '../hooks/useProductMutations';
import ProductTable from '../components/ProductTable';
import Button from '@/components/ui/Button';
import LoadingSkeleton from '@/components/shared/LoadingSkeleton';
import EmptyState from '@/components/shared/EmptyState';
import ErrorState from '@/components/shared/ErrorState';
import ConfirmDialog from '@/components/shared/ConfirmDialog';
import type { Product } from '@/types/product';

export default function ProductsPage() {
  const navigate = useNavigate();
  const { data: products, isLoading, isError, refetch } = useProducts();
  const deleteMutation = useDeleteProduct();
  const [deleteTarget, setDeleteTarget] = useState<Product | null>(null);

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
          <h2 className="text-2xl font-bold text-gray-900">Products</h2>
          <p className="text-sm text-gray-500">
            Manage your product catalog and pricing
          </p>
        </div>
        <Button onClick={() => navigate('/app/products/new')}>
          <Plus className="h-4 w-4" />
          New Product
        </Button>
      </div>

      {/* Content states */}
      {isLoading && <LoadingSkeleton variant="table-row" rows={6} />}

      {isError && !isLoading && (
        <ErrorState onRetry={() => refetch()} />
      )}

      {!isLoading && !isError && products?.length === 0 && (
        <EmptyState
          title="No products yet"
          description="Create your first product to start managing your catalog."
          actionLabel="Create your first product"
          onAction={() => navigate('/app/products/new')}
        />
      )}

      {!isLoading && !isError && products && products.length > 0 && (
        <ProductTable
          products={products}
          onDelete={(product) => setDeleteTarget(product)}
        />
      )}

      {/* Delete confirmation */}
      <ConfirmDialog
        open={!!deleteTarget}
        onClose={() => setDeleteTarget(null)}
        onConfirm={() => {
          if (deleteTarget) {
            deleteMutation.mutate(deleteTarget.id);
            setDeleteTarget(null);
          }
        }}
        title="Delete Product"
        message={`Are you sure you want to delete "${deleteTarget?.name}"? This action cannot be undone.`}
        loading={deleteMutation.isPending}
      />
    </motion.div>
  );
}
