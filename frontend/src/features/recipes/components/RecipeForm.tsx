import { useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import type { Recipe } from '@/types/recipe';
import Input from '@/components/ui/Input';
import Button from '@/components/ui/Button';

const recipeSchema = z.object({
  name: z
    .string()
    .min(1, 'Name is required')
    .max(255, 'Name must be 255 characters or less'),
  description: z
    .string()
    .max(1000, 'Description must be 1000 characters or less')
    .optional()
    .or(z.literal('')),
});

export type RecipeFormValues = z.infer<typeof recipeSchema>;

interface RecipeFormProps {
  mode: 'create' | 'edit';
  defaultValues?: Recipe;
  onSubmit: (values: RecipeFormValues) => void;
  loading?: boolean;
}

export default function RecipeForm({
  mode,
  defaultValues,
  onSubmit,
  loading = false,
}: RecipeFormProps) {
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<RecipeFormValues>({
    resolver: zodResolver(recipeSchema),
    defaultValues: {
      name: defaultValues?.name || '',
      description: defaultValues?.description || '',
    },
  });

  useEffect(() => {
    if (defaultValues) {
      reset({
        name: defaultValues.name,
        description: defaultValues.description || '',
      });
    }
  }, [defaultValues, reset]);

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      <div className="rounded-xl border border-gray-200 bg-white p-6">
        <h3 className="mb-4 text-lg font-semibold text-gray-900">
          Recipe Information
        </h3>

        <div className="space-y-4">
          <Input
            label="Name"
            placeholder="e.g. Lomito Completo"
            error={errors.name?.message}
            {...register('name')}
          />

          <div className="flex flex-col gap-1">
            <label
              htmlFor="description"
              className="text-sm font-medium text-gray-700"
            >
              Description (optional)
            </label>
            <textarea
              id="description"
              rows={3}
              placeholder="Brief description of the recipe..."
              className="rounded-lg border border-gray-300 px-3 py-2 text-sm transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-500"
              {...register('description')}
            />
            {errors.description && (
              <p className="text-xs text-red-600">
                {errors.description.message}
              </p>
            )}
          </div>
        </div>
      </div>

      <div className="flex justify-end gap-3">
        <Button type="submit" loading={loading}>
          {mode === 'create' ? 'Create Recipe' : 'Save Changes'}
        </Button>
      </div>
    </form>
  );
}
