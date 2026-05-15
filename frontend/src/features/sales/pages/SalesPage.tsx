import { useState, useCallback, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { ShoppingCart, History, CheckCircle } from 'lucide-react';
import { useProducts } from '@/features/products/hooks/useProducts';
import { useCreateSale } from '../hooks/useSaleMutations';
import SaleForm, { type SaleFormValues } from '../components/SaleForm';
import SaleConfirmation from '../components/SaleConfirmation';
import Button from '@/components/ui/Button';
import ErrorState from '@/components/shared/ErrorState';
import LoadingSkeleton from '@/components/shared/LoadingSkeleton';
import { formatCurrency } from '@/lib/formatters';

export default function SalesPage() {
  const navigate = useNavigate();
  const {
    data: products,
    isLoading: productsLoading,
    isError: productsError,
    refetch: refetchProducts,
  } = useProducts();

  const createSaleMutation = useCreateSale();

  const [formKey, setFormKey] = useState(0);
  const [showSuccess, setShowSuccess] = useState(false);
  const [reviewValues, setReviewValues] = useState<{
    values: SaleFormValues;
    productName: string;
    unitPrice: string;
    costPrice: string | null;
  } | null>(null);

  const activeProducts = products?.filter((p) => p.is_active) ?? [];

  const productOptions = activeProducts.map((p) => ({
    value: p.id,
    label: `${p.name} \u2014 ${formatCurrency(p.sale_price)}`,
  }));

  const selectedProductId = reviewValues?.values.product_id;
  const selectedProduct = selectedProductId
    ? activeProducts.find((p) => p.id === selectedProductId)
    : null;

  const unitPrice = selectedProduct?.sale_price ?? '0';

  const handleReview = useCallback(
    (values: SaleFormValues) => {
      const product = activeProducts.find((p) => p.id === values.product_id);
      if (!product) return;

      setReviewValues({
        values,
        productName: product.name,
        unitPrice: product.sale_price,
        costPrice: product.cost_price,
      });
    },
    [activeProducts]
  );

  const handleConfirm = useCallback(() => {
    if (!reviewValues) return;

    createSaleMutation.mutate(
      {
        product_id: reviewValues.values.product_id,
        quantity: parseInt(reviewValues.values.quantity, 10),
      },
      {
        onSuccess: () => {
          setReviewValues(null);
          setFormKey((k) => k + 1);
          setShowSuccess(true);
        },
      }
    );
  }, [reviewValues, createSaleMutation]);

  // Auto-hide success banner
  useEffect(() => {
    if (showSuccess) {
      const timer = setTimeout(() => setShowSuccess(false), 2500);
      return () => clearTimeout(timer);
    }
  }, [showSuccess]);

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -12 }}
      className="mx-auto max-w-2xl"
    >
      {/* Header */}
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">New Sale</h2>
          <p className="text-sm text-gray-500">
            Register a sale and automatically deduct stock
          </p>
        </div>
        <Button
          variant="secondary"
          onClick={() => navigate('/app/sales/history')}
        >
          <History className="h-4 w-4" />
          Sales History
        </Button>
      </div>

      {/* Success feedback */}
      <AnimatePresence>
        {showSuccess && (
          <motion.div
            initial={{ opacity: 0, y: -8, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -8, scale: 0.95 }}
            className="mb-6 flex items-center gap-3 rounded-xl border border-green-200 bg-green-50 px-4 py-3"
          >
            <CheckCircle className="h-5 w-5 text-green-600" />
            <div>
              <p className="text-sm font-semibold text-green-800">
                Sale registered successfully!
              </p>
              <p className="text-xs text-green-600">
                Stock has been deducted automatically
              </p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Content */}
      {productsLoading && <LoadingSkeleton variant="card" rows={1} />}

      {productsError && !productsLoading && (
        <ErrorState onRetry={() => refetchProducts()} />
      )}

      {!productsLoading && !productsError && (
        <SaleForm
          productOptions={productOptions}
          productsLoading={false}
          unitPrice={unitPrice}
          onReview={handleReview}
          resetKey={formKey}
        />
      )}

      {/* Confirmation Modal */}
      <SaleConfirmation
        open={reviewValues !== null}
        onClose={() => setReviewValues(null)}
        onConfirm={handleConfirm}
        loading={createSaleMutation.isPending}
        productName={reviewValues?.productName ?? ''}
        quantity={reviewValues ? parseInt(reviewValues.values.quantity, 10) : 0}
        unitPrice={reviewValues?.unitPrice ?? '0'}
        costPrice={reviewValues?.costPrice ?? null}
      />
    </motion.div>
  );
}
