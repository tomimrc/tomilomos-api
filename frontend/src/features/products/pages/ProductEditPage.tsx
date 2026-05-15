import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft } from 'lucide-react';
import ProductForm, { type ProductFormValues } from '../components/ProductForm';
import { useProduct } from '../hooks/useProduct';
import { useUpdateProduct } from '../hooks/useProductMutations';
import Button from '@/components/ui/Button';
import LoadingSkeleton from '@/components/shared/LoadingSkeleton';
import ErrorState from '@/components/shared/ErrorState';

export default function ProductEditPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { data: product, isLoading, isError, refetch } = useProduct(id!);
  const updateMutation = useUpdateProduct();

  const handleSubmit = (values: ProductFormValues) => {
    if (!id) return;
    updateMutation.mutate(
      {
        id,
        payload: {
          name: values.name,
          sale_price: values.sale_price,
          recipe_id: values.recipe_id || null,
          is_active: values.is_active,
        },
      },
      {
        onSuccess: () => navigate(`/app/products/${id}`),
      }
    );
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -12 }}
      className="mx-auto max-w-2xl"
    >
      <button
        onClick={() => navigate(`/app/products/${id}`)}
        className="mb-4 flex items-center gap-1 text-sm text-gray-500 hover:text-gray-700"
      >
        <ArrowLeft className="h-4 w-4" />
        Back to Product
      </button>

      <h2 className="mb-6 text-2xl font-bold text-gray-900">Edit Product</h2>

      {isLoading && <LoadingSkeleton variant="card" rows={1} />}

      {isError && !isLoading && (
        <ErrorState onRetry={() => refetch()} />
      )}

      {product && (
        <ProductForm
          mode="edit"
          defaultValues={product}
          onSubmit={handleSubmit}
          loading={updateMutation.isPending}
        />
      )}
    </motion.div>
  );
}
