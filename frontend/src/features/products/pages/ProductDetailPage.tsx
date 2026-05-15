import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft, Pencil, Trash2 } from 'lucide-react';
import { useProduct } from '../hooks/useProduct';
import { useDeleteProduct } from '../hooks/useProductMutations';
import ProductCostDisplay from '../components/ProductCostDisplay';
import Badge from '@/components/ui/Badge';
import Button from '@/components/ui/Button';
import ConfirmDialog from '@/components/shared/ConfirmDialog';
import LoadingSkeleton from '@/components/shared/LoadingSkeleton';
import ErrorState from '@/components/shared/ErrorState';
import { formatCurrency } from '@/lib/formatters';

export default function ProductDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { data: product, isLoading, isError, refetch } = useProduct(id!);
  const deleteMutation = useDeleteProduct();
  const [showDelete, setShowDelete] = useState(false);

  if (isLoading) {
    return <LoadingSkeleton variant="card" rows={2} />;
  }

  if (isError || !product) {
    return (
      <ErrorState
        message="Product not found"
        onRetry={() => refetch()}
      />
    );
  }

  const handleDelete = () => {
    deleteMutation.mutate(product.id, {
      onSuccess: () => navigate('/app/products'),
    });
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -12 }}
      className="mx-auto max-w-2xl"
    >
      {/* Back + Actions */}
      <div className="mb-4 flex items-center justify-between">
        <button
          onClick={() => navigate('/app/products')}
          className="flex items-center gap-1 text-sm text-gray-500 hover:text-gray-700"
        >
          <ArrowLeft className="h-4 w-4" />
          Back to Products
        </button>
        <div className="flex items-center gap-2">
          <Button
            variant="secondary"
            onClick={() => navigate(`/app/products/${product.id}/edit`)}
          >
            <Pencil className="h-4 w-4" />
            Edit
          </Button>
          <Button variant="danger" onClick={() => setShowDelete(true)}>
            <Trash2 className="h-4 w-4" />
            Delete
          </Button>
        </div>
      </div>

      {/* Product Info Card */}
      <div className="mb-6 rounded-xl border border-gray-200 bg-white p-6">
        <div className="mb-2 flex items-center gap-3">
          <h2 className="text-2xl font-bold text-gray-900">{product.name}</h2>
          <Badge variant={product.is_active ? 'active' : 'inactive'} />
        </div>

        <div className="mt-4 grid gap-4 sm:grid-cols-2">
          <div>
            <p className="text-sm text-gray-500">Sale Price</p>
            <p className="text-xl font-semibold text-gray-900">
              {formatCurrency(product.sale_price)}
            </p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Cost Price</p>
            <p className="text-xl font-semibold text-gray-900">
              {formatCurrency(product.cost_price)}
            </p>
          </div>
        </div>
      </div>

      {/* Cost Breakdown */}
      <ProductCostDisplay
        productId={product.id}
        recipeId={product.recipe_id}
      />

      {/* Delete Confirmation */}
      <ConfirmDialog
        open={showDelete}
        onClose={() => setShowDelete(false)}
        onConfirm={handleDelete}
        title="Delete Product"
        message={`Are you sure you want to delete "${product.name}"? This action cannot be undone.`}
        loading={deleteMutation.isPending}
      />
    </motion.div>
  );
}
