import { useEffect } from 'react';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import type { RawMaterial } from '@/types/rawMaterial';
import { VALID_UNITS } from '@/lib/constants';
import Input from '@/components/ui/Input';
import Select from '@/components/ui/Select';
import Button from '@/components/ui/Button';

const unitOptions = VALID_UNITS.map((unit) => ({
  value: unit,
  label: unit,
}));

const rawMaterialSchema = z.object({
  name: z
    .string()
    .min(1, 'Name is required')
    .max(255, 'Name must be 255 characters or less'),
  unit_of_measurement: z
    .string()
    .min(1, 'Unit is required'),
  cost_per_unit: z
    .string()
    .min(1, 'Cost is required')
    .refine(
      (v) => {
        const num = parseFloat(v);
        return !isNaN(num) && num > 0;
      },
      'Cost must be greater than 0'
    )
    .refine(
      (v) => {
        const parts = v.split('.');
        return parts.length === 1 || (parts[1] && parts[1].length <= 2);
      },
      'Cost must have at most 2 decimal places'
    ),
  supplier: z
    .string()
    .max(255, 'Supplier must be 255 characters or less')
    .optional()
    .or(z.literal('')),
});

export type RawMaterialFormValues = z.infer<typeof rawMaterialSchema>;

interface RawMaterialFormProps {
  mode: 'create' | 'edit';
  defaultValues?: RawMaterial;
  onSubmit: (values: RawMaterialFormValues) => void;
  loading?: boolean;
}

export default function RawMaterialForm({
  mode,
  defaultValues,
  onSubmit,
  loading = false,
}: RawMaterialFormProps) {
  const {
    register,
    handleSubmit,
    control,
    reset,
    formState: { errors },
  } = useForm<RawMaterialFormValues>({
    resolver: zodResolver(rawMaterialSchema),
    defaultValues: {
      name: defaultValues?.name || '',
      unit_of_measurement: defaultValues?.unit_of_measurement || '',
      cost_per_unit: defaultValues?.cost_per_unit || '',
      supplier: defaultValues?.supplier || '',
    },
  });

  useEffect(() => {
    if (defaultValues) {
      reset({
        name: defaultValues.name,
        unit_of_measurement: defaultValues.unit_of_measurement,
        cost_per_unit: defaultValues.cost_per_unit,
        supplier: defaultValues.supplier || '',
      });
    }
  }, [defaultValues, reset]);

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      <div className="rounded-xl border border-gray-200 bg-white p-6">
        <h3 className="mb-4 text-lg font-semibold text-gray-900">
          Raw Material Information
        </h3>

        <div className="grid gap-4 sm:grid-cols-2">
          <div className="sm:col-span-2">
            <Input
              label="Name"
              placeholder="e.g. Chicken Breast"
              error={errors.name?.message}
              {...register('name')}
            />
          </div>

          <Controller
            name="unit_of_measurement"
            control={control}
            render={({ field }) => (
              <Select
                label="Unit of Measurement"
                options={unitOptions}
                value={field.value}
                onChange={field.onChange}
                placeholder="Select a unit..."
                error={errors.unit_of_measurement?.message}
              />
            )}
          />

          <Input
            label="Cost per Unit"
            placeholder="0.00"
            error={errors.cost_per_unit?.message}
            {...register('cost_per_unit')}
          />

          <div className="sm:col-span-2">
            <Input
              label="Supplier (optional)"
              placeholder="e.g. Local Market"
              error={errors.supplier?.message}
              {...register('supplier')}
            />
          </div>
        </div>
      </div>

      <div className="flex justify-end gap-3">
        <Button type="submit" loading={loading}>
          {mode === 'create' ? 'Create Raw Material' : 'Save Changes'}
        </Button>
      </div>
    </form>
  );
}
