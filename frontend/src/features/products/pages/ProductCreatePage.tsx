import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft } from 'lucide-react';
import ProductForm, { type ProductFormValues } from '../components/ProductForm';
import { useCreateProduct } from '../hooks/useProductMutations';
import Button from '@/components/ui/Button';

export default function ProductCreatePage() {
  const navigate = useNavigate();
  const createMutation = useCreateProduct();

  const handleSubmit = (values: ProductFormValues) => {
    createMutation.mutate(
      {
        name: values.name,
        sale_price: values.sale_price,
        recipe_id: values.recipe_id || undefined,
        is_active: values.is_active,
      },
      {
        onSuccess: () => navigate('/app/products'),
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
        onClick={() => navigate('/app/products')}
        className="mb-4 flex items-center gap-1 text-sm text-gray-500 hover:text-gray-700"
      >
        <ArrowLeft className="h-4 w-4" />
        Back to Products
      </button>

      <h2 className="mb-6 text-2xl font-bold text-gray-900">
        Create New Product
      </h2>

      <ProductForm
        mode="create"
        onSubmit={handleSubmit}
        loading={createMutation.isPending}
      />
    </motion.div>
  );
}
