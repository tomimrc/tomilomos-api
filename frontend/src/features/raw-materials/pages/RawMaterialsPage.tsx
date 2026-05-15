import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Plus } from 'lucide-react';
import { useRawMaterials } from '../hooks/useRawMaterials';
import { useDeleteRawMaterial } from '../hooks/useRawMaterialMutations';
import RawMaterialTable from '../components/RawMaterialTable';
import Button from '@/components/ui/Button';
import LoadingSkeleton from '@/components/shared/LoadingSkeleton';
import EmptyState from '@/components/shared/EmptyState';
import ErrorState from '@/components/shared/ErrorState';
import ConfirmDialog from '@/components/shared/ConfirmDialog';
import type { RawMaterial } from '@/types/rawMaterial';

export default function RawMaterialsPage() {
  const navigate = useNavigate();
  const { data: materials, isLoading, isError, refetch } = useRawMaterials();
  const deleteMutation = useDeleteRawMaterial();
  const [deleteTarget, setDeleteTarget] = useState<RawMaterial | null>(null);

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -12 }}
      transition={{ duration: 0.2 }}
    >
      {/* Header */}
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Raw Materials</h2>
          <p className="text-sm text-gray-500">
            Manage your raw materials inventory and stock levels
          </p>
        </div>
        <Button onClick={() => navigate('/app/raw-materials/new')}>
          <Plus className="h-4 w-4" />
          New Raw Material
        </Button>
      </div>

      {/* Content states */}
      {isLoading && <LoadingSkeleton variant="table-row" rows={6} />}

      {isError && !isLoading && (
        <ErrorState onRetry={() => refetch()} />
      )}

      {!isLoading && !isError && materials?.length === 0 && (
        <EmptyState
          title="No raw materials yet"
          description="Create your first raw material to start managing your inventory."
          actionLabel="Create your first raw material"
          onAction={() => navigate('/app/raw-materials/new')}
        />
      )}

      {!isLoading && !isError && materials && materials.length > 0 && (
        <RawMaterialTable
          materials={materials}
          onDelete={(material) => setDeleteTarget(material)}
        />
      )}

      {/* Delete confirmation */}
      <ConfirmDialog
        open={!!deleteTarget}
        onClose={() => setDeleteTarget(null)}
        onConfirm={() => {
          if (deleteTarget) {
            deleteMutation.mutate(deleteTarget.id);
            setDeleteTarget(null);
          }
        }}
        title="Delete Raw Material"
        message={`Are you sure you want to delete "${deleteTarget?.name}"? This action cannot be undone.`}
        loading={deleteMutation.isPending}
      />
    </motion.div>
  );
}
