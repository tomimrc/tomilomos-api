import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft } from 'lucide-react';
import RawMaterialForm, {
  type RawMaterialFormValues,
} from '../components/RawMaterialForm';
import { useRawMaterial } from '../hooks/useRawMaterial';
import { useUpdateRawMaterial } from '../hooks/useRawMaterialMutations';
import LoadingSkeleton from '@/components/shared/LoadingSkeleton';
import ErrorState from '@/components/shared/ErrorState';

export default function RawMaterialEditPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { data: material, isLoading, isError, refetch } = useRawMaterial(id!);
  const updateMutation = useUpdateRawMaterial();

  const handleSubmit = (values: RawMaterialFormValues) => {
    if (!id) return;
    updateMutation.mutate(
      {
        id,
        payload: {
          name: values.name,
          unit_of_measurement: values.unit_of_measurement,
          cost_per_unit: values.cost_per_unit,
          supplier: values.supplier || null,
        },
      },
      {
        onSuccess: () => navigate(`/app/raw-materials/${id}`),
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
        onClick={() => navigate(`/app/raw-materials/${id}`)}
        className="mb-4 flex items-center gap-1 text-sm text-gray-500 hover:text-gray-700"
      >
        <ArrowLeft className="h-4 w-4" />
        Back to Material
      </button>

      <h2 className="mb-6 text-2xl font-bold text-gray-900">
        Edit Raw Material
      </h2>

      {isLoading && <LoadingSkeleton variant="card" rows={1} />}

      {isError && !isLoading && (
        <ErrorState onRetry={() => refetch()} />
      )}

      {material && (
        <RawMaterialForm
          mode="edit"
          defaultValues={material}
          onSubmit={handleSubmit}
          loading={updateMutation.isPending}
        />
      )}
    </motion.div>
  );
}
