import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import Modal from '@/components/ui/Modal';
import Input from '@/components/ui/Input';
import Button from '@/components/ui/Button';

const adjustmentSchema = z.object({
  quantity: z
    .string()
    .min(1, 'Quantity is required')
    .refine(
      (v) => {
        const num = parseFloat(v);
        return !isNaN(num) && num > 0;
      },
      'Quantity must be greater than 0'
    ),
  reason: z
    .string()
    .max(255, 'Reason must be 255 characters or less')
    .optional()
    .or(z.literal('')),
});

export type AdjustmentFormValues = z.infer<typeof adjustmentSchema>;

interface StockAdjustmentModalProps {
  mode: 'add' | 'remove';
  materialName: string;
  currentStock: number;
  open: boolean;
  onClose: () => void;
  onSubmit: (values: AdjustmentFormValues) => void;
  loading?: boolean;
}

export default function StockAdjustmentModal({
  mode,
  materialName,
  currentStock,
  open,
  onClose,
  onSubmit,
  loading = false,
}: StockAdjustmentModalProps) {
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<AdjustmentFormValues>({
    resolver: zodResolver(adjustmentSchema),
    defaultValues: {
      quantity: '',
      reason: '',
    },
  });

  const handleFormSubmit = (values: AdjustmentFormValues) => {
    onSubmit(values);
    reset();
  };

  const handleClose = () => {
    reset();
    onClose();
  };

  const title =
    mode === 'add'
      ? `Add Stock \u2014 ${materialName}`
      : `Remove Stock \u2014 ${materialName}`;

  return (
    <Modal
      open={open}
      onClose={handleClose}
      title={title}
      footer={
        <>
          <Button variant="secondary" onClick={handleClose} disabled={loading}>
            Cancel
          </Button>
          <Button
            variant={mode === 'add' ? 'primary' : 'danger'}
            onClick={handleSubmit(handleFormSubmit)}
            loading={loading}
          >
            {mode === 'add' ? 'Add Stock' : 'Remove Stock'}
          </Button>
        </>
      }
    >
      <div className="space-y-4">
        {mode === 'remove' && (
          <p className="rounded-lg bg-gray-50 px-3 py-2 text-sm text-gray-600">
            Available:{' '}
            <span className="font-semibold text-gray-900">
              {currentStock.toFixed(2)}
            </span>
          </p>
        )}

        <Input
          label="Quantity"
          placeholder="0.00"
          error={errors.quantity?.message}
          {...register('quantity')}
        />

        <Input
          label="Reason (optional)"
          placeholder="e.g. Weekly purchase"
          error={errors.reason?.message}
          {...register('reason')}
        />
      </div>
    </Modal>
  );
}
