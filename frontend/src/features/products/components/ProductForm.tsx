import { useEffect } from 'react';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import type { Product } from '@/types/product';
import Input from '@/components/ui/Input';
import Button from '@/components/ui/Button';
import RecipeSelector from './RecipeSelector';

const productSchema = z.object({
  name: z
    .string()
    .min(1, 'Name is required')
    .max(255, 'Name must be 255 characters or less'),
  sale_price: z
    .string()
    .min(1, 'Sale price is required')
    .refine(
      (v) => {
        const num = parseFloat(v);
        return !isNaN(num) && num > 0;
      },
      'Price must be greater than 0'
    )
    .refine(
      (v) => {
        const parts = v.split('.');
        return parts.length === 1 || (parts[1] && parts[1].length <= 2);
      },
      'Price must have at most 2 decimal places'
    ),
  recipe_id: z.string().optional().nullable(),
  is_active: z.boolean().default(true),
});

export type ProductFormValues = z.infer<typeof productSchema>;

interface ProductFormProps {
  mode: 'create' | 'edit';
  defaultValues?: Product;
  onSubmit: (values: ProductFormValues) => void;
  loading?: boolean;
}

export default function ProductForm({
  mode,
  defaultValues,
  onSubmit,
  loading = false,
}: ProductFormProps) {
  const {
    register,
    handleSubmit,
    control,
    reset,
    formState: { errors },
  } = useForm<ProductFormValues>({
    resolver: zodResolver(productSchema),
    defaultValues: {
      name: defaultValues?.name || '',
      sale_price: defaultValues?.sale_price || '',
      recipe_id: defaultValues?.recipe_id || null,
      is_active: defaultValues?.is_active ?? true,
    },
  });

  useEffect(() => {
    if (defaultValues) {
      reset({
        name: defaultValues.name,
        sale_price: defaultValues.sale_price,
        recipe_id: defaultValues.recipe_id || null,
        is_active: defaultValues.is_active,
      });
    }
  }, [defaultValues, reset]);

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      <div className="rounded-xl border border-gray-200 bg-white p-6">
        <h3 className="mb-4 text-lg font-semibold text-gray-900">
          Product Information
        </h3>

        <div className="grid gap-4 sm:grid-cols-2">
          <div className="sm:col-span-2">
            <Input
              label="Name"
              placeholder="e.g. Lomito Completo"
              error={errors.name?.message}
              {...register('name')}
            />
          </div>

          <Input
            label="Sale Price"
            placeholder="0.00"
            error={errors.sale_price?.message}
            {...register('sale_price')}
          />

          <Controller
            name="recipe_id"
            control={control}
            render={({ field }) => (
              <RecipeSelector
                label="Recipe (optional)"
                value={field.value || ''}
                onChange={(v) => field.onChange(v || null)}
                error={errors.recipe_id?.message}
              />
            )}
          />

          <div className="flex items-center gap-2">
            <Controller
              name="is_active"
              control={control}
              render={({ field }) => (
                <label className="flex items-center gap-2 text-sm text-gray-700">
                  <input
                    type="checkbox"
                    checked={field.value}
                    onChange={(e) => field.onChange(e.target.checked)}
                    className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                  />
                  Active
                </label>
              )}
            />
          </div>
        </div>
      </div>

      <div className="flex justify-end gap-3">
        <Button type="submit" loading={loading}>
          {mode === 'create' ? 'Create Product' : 'Save Changes'}
        </Button>
      </div>
    </form>
  );
}
