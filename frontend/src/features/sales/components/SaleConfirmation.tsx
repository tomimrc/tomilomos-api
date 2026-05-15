import Modal from '@/components/ui/Modal';
import Button from '@/components/ui/Button';
import { formatCurrency } from '@/lib/formatters';

interface SaleConfirmationProps {
  open: boolean;
  onClose: () => void;
  onConfirm: () => void;
  loading?: boolean;
  productName: string;
  quantity: number;
  unitPrice: string;
  costPrice: string | null;
}

export default function SaleConfirmation({
  open,
  onClose,
  onConfirm,
  loading = false,
  productName,
  quantity,
  unitPrice,
  costPrice,
}: SaleConfirmationProps) {
  const unit = parseFloat(unitPrice);
  const total = unit * quantity;
  const cost = costPrice ? parseFloat(costPrice) : null;
  const margin = cost !== null ? total - cost * quantity : null;

  return (
    <Modal
      open={open}
      onClose={onClose}
      title="Confirm Sale"
      footer={
        <>
          <Button variant="secondary" onClick={onClose} disabled={loading}>
            Cancel
          </Button>
          <Button variant="primary" onClick={onConfirm} loading={loading}>
            Confirm Sale
          </Button>
        </>
      }
    >
      <div className="space-y-4">
        <div className="rounded-lg bg-gray-50 p-4">
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-500">Product</span>
            <span className="text-sm font-semibold text-gray-900">
              {productName}
            </span>
          </div>
          <div className="mt-2 flex items-center justify-between">
            <span className="text-sm text-gray-500">Quantity</span>
            <span className="text-sm font-semibold text-gray-900">
              {quantity}
            </span>
          </div>
        </div>

        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-500">Unit Price</span>
            <span className="text-sm text-gray-900">
              {formatCurrency(unitPrice)}
            </span>
          </div>

          <div className="flex items-center justify-between border-t pt-2">
            <span className="text-sm font-semibold text-gray-700">Total</span>
            <span className="text-lg font-bold text-indigo-600">
              {formatCurrency(total)}
            </span>
          </div>

          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-500">Estimated Cost</span>
            <span className="text-sm text-gray-600">
              {cost !== null
                ? formatCurrency(cost * quantity)
                : '\u2014'}
            </span>
          </div>

          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-500">Estimated Margin</span>
            <span
              className={`text-sm font-semibold ${
                margin !== null
                  ? margin >= 0
                    ? 'text-green-600'
                    : 'text-red-600'
                  : 'text-gray-400'
              }`}
            >
              {margin !== null ? formatCurrency(margin) : '\u2014'}
            </span>
          </div>
        </div>
      </div>
    </Modal>
  );
}
