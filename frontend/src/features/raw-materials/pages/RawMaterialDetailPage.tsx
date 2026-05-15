import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft, Pencil, Trash2, Plus, Minus } from 'lucide-react';
import { useRawMaterial } from '../hooks/useRawMaterial';
import {
  useDeleteRawMaterial,
  useAddStock,
  useRemoveStock,
} from '../hooks/useRawMaterialMutations';
import StockLevelBadge from '../components/StockLevelBadge';
import StockAdjustmentModal, {
  type AdjustmentFormValues,
} from '../components/StockAdjustmentModal';
import Button from '@/components/ui/Button';
import ConfirmDialog from '@/components/shared/ConfirmDialog';
import LoadingSkeleton from '@/components/shared/LoadingSkeleton';
import ErrorState from '@/components/shared/ErrorState';
import { formatCurrency } from '@/lib/formatters';

type StockMode = 'add' | 'remove';

export default function RawMaterialDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { data: material, isLoading, isError, refetch } = useRawMaterial(id!);
  const deleteMutation = useDeleteRawMaterial();
  const addStockMutation = useAddStock();
  const removeStockMutation = useRemoveStock();

  const [showDelete, setShowDelete] = useState(false);
  const [stockModalMode, setStockModalMode] = useState<StockMode | null>(null);

  const currentStock = material
    ? parseFloat(material.current_stock)
    : 0;

  // ── Stock adjust handler ──
  const handleStockSubmit = (values: AdjustmentFormValues) => {
    if (!id || !stockModalMode) return;

    const payload = {
      quantity: values.quantity,
      reason: values.reason || null,
    };

    if (stockModalMode === 'add') {
      addStockMutation.mutate(
        { id, payload },
        { onSuccess: () => setStockModalMode(null) }
      );
    } else {
      removeStockMutation.mutate(
        { id, payload },
        { onSuccess: () => setStockModalMode(null) }
      );
    }
  };

  // ── Loading / Error states ──
  if (isLoading) {
    return <LoadingSkeleton variant="card" rows={2} />;
  }

  if (isError || !material) {
    return (
      <ErrorState
        message="Raw material not found"
        onRetry={() => refetch()}
      />
    );
  }

  const handleDelete = () => {
    deleteMutation.mutate(material.id, {
      onSuccess: () => navigate('/app/raw-materials'),
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
          onClick={() => navigate('/app/raw-materials')}
          className="flex items-center gap-1 text-sm text-gray-500 hover:text-gray-700"
        >
          <ArrowLeft className="h-4 w-4" />
          Back to Raw Materials
        </button>
        <div className="flex items-center gap-2">
          <Button
            variant="secondary"
            onClick={() => navigate(`/app/raw-materials/${material.id}/edit`)}
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

      {/* Material Info Card */}
      <div className="mb-6 rounded-xl border border-gray-200 bg-white p-6">
        <div className="mb-2 flex items-center gap-3">
          <h2 className="text-2xl font-bold text-gray-900">{material.name}</h2>
          <StockLevelBadge stock={currentStock} />
        </div>

        <div className="mt-4 grid gap-4 sm:grid-cols-2">
          <div>
            <p className="text-sm text-gray-500">Unit of Measurement</p>
            <p className="text-lg font-semibold text-gray-900">
              {material.unit_of_measurement}
            </p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Cost per Unit</p>
            <p className="text-lg font-semibold text-gray-900">
              {formatCurrency(material.cost_per_unit)}
            </p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Supplier</p>
            <p className="text-lg font-semibold text-gray-900">
              {material.supplier || '\u2014'}
            </p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Current Stock</p>
            <p className="text-lg font-semibold text-gray-900">
              {parseFloat(material.current_stock).toFixed(2)}{' '}
              {material.unit_of_measurement}
            </p>
          </div>
        </div>

        {/* Stock Action Buttons */}
        <div className="mt-6 flex gap-3 border-t pt-4">
          <Button onClick={() => setStockModalMode('add')}>
            <Plus className="h-4 w-4" />
            Add Stock
          </Button>
          <Button
            variant="secondary"
            onClick={() => setStockModalMode('remove')}
          >
            <Minus className="h-4 w-4" />
            Remove Stock
          </Button>
        </div>
      </div>

      {/* Metadata */}
      <div className="rounded-xl border border-gray-200 bg-white p-6">
        <h3 className="mb-3 text-sm font-semibold uppercase tracking-wider text-gray-500">
          Details
        </h3>
        <div className="grid gap-2 text-sm">
          <div className="flex justify-between">
            <span className="text-gray-500">Created</span>
            <span className="text-gray-700">
              {new Date(material.created_at).toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit',
              })}
            </span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-500">Updated</span>
            <span className="text-gray-700">
              {new Date(material.updated_at).toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit',
              })}
            </span>
          </div>
        </div>
      </div>

      {/* Stock Adjustment Modal */}
      <StockAdjustmentModal
        mode={stockModalMode || 'add'}
        materialName={material.name}
        currentStock={currentStock}
        open={stockModalMode !== null}
        onClose={() => setStockModalMode(null)}
        onSubmit={handleStockSubmit}
        loading={
          stockModalMode === 'add'
            ? addStockMutation.isPending
            : removeStockMutation.isPending
        }
      />

      {/* Delete Confirmation */}
      <ConfirmDialog
        open={showDelete}
        onClose={() => setShowDelete(false)}
        onConfirm={handleDelete}
        title="Delete Raw Material"
        message={`Are you sure you want to delete "${material.name}"? This action cannot be undone.`}
        loading={deleteMutation.isPending}
      />
    </motion.div>
  );
}
