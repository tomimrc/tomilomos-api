import { useEffect } from 'react';
import { useForm, Controller, type Control, type FieldPath } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import type { SelectOption } from '@/components/ui/Select';
import Input from '@/components/ui/Input';
import ProductSelector from './ProductSelector';
import { formatCurrency } from '@/lib/formatters';

const saleFormSchema = z.object({
  product_id: z.string().min(1, 'Please select a product'),
  quantity: z
    .string()
    .min(1, 'Quantity is required')
    .refine(
      (v) => {
        const num = parseInt(v, 10);
        return !isNaN(num) && num > 0;
      },
      'Quantity must be greater than 0'
    )
    .refine(
      (v) => {
        const num = parseInt(v, 10);
        return !isNaN(num) && Number.isInteger(num) && num === parseFloat(v);
      },
      'Quantity must be a whole number'
    ),
});

export type SaleFormValues = z.infer<typeof saleFormSchema>;

interface SaleFormProps {
  productOptions: SelectOption[];
  productsLoading: boolean;
  unitPrice: string;
  onReview: (values: SaleFormValues) => void;
  resetKey?: number;
}

export default function SaleForm({
  productOptions,
  productsLoading,
  unitPrice,
  onReview,
  resetKey = 0,
}: SaleFormProps) {
  const {
    register,
    handleSubmit,
    control,
    watch,
    reset,
    formState: { errors },
  } = useForm<SaleFormValues>({
    resolver: zodResolver(saleFormSchema),
    defaultValues: {
      product_id: '',
      quantity: '',
    },
  });

  const quantity = watch('quantity');
  const hasProduct = watch('product_id') !== '';

  useEffect(() => {
    reset({ product_id: '', quantity: '' });
  }, [resetKey, reset]);

  const quantityNum = parseInt(quantity, 10);
  const priceNum = parseFloat(unitPrice);
  const total =
    !isNaN(quantityNum) && !isNaN(priceNum) && quantityNum > 0
      ? priceNum * quantityNum
      : null;

  return (
    <form onSubmit={handleSubmit(onReview)} className="space-y-6">
      <div className="rounded-xl border border-gray-200 bg-white p-6">
        <h3 className="mb-4 text-lg font-semibold text-gray-900">
          New Sale
        </h3>

        <div className="grid gap-4 sm:grid-cols-2">
          <div className="sm:col-span-2">
            <Controller
              control={control}
              name="product_id"
              render={({ field }) => (
                <ProductSelector
                  value={field.value}
                  onChange={field.onChange}
                  options={productOptions}
                  loading={productsLoading}
                  error={errors.product_id?.message}
                />
              )}
            />
          </div>

          <Input
            label="Quantity"
            placeholder="e.g. 2"
            error={errors.quantity?.message}
            disabled={!hasProduct}
            {...register('quantity')}
          />
        </div>

        {/* Calculated total */}
        {total !== null && (
          <div className="mt-4 rounded-lg bg-indigo-50 px-4 py-3">
            <p className="text-sm text-indigo-600">Total</p>
            <p className="text-2xl font-bold text-indigo-900">
              {formatCurrency(total)}
            </p>
          </div>
        )}
      </div>

      <div className="flex justify-end">
        <button
          type="submit"
          disabled={!hasProduct || total === null}
          className="inline-flex items-center gap-2 rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
        >
          Review Sale
        </button>
      </div>
    </form>
  );
}
