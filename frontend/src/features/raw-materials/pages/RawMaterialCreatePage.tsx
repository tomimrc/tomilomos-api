import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft } from 'lucide-react';
import RawMaterialForm, {
  type RawMaterialFormValues,
} from '../components/RawMaterialForm';
import { useCreateRawMaterial } from '../hooks/useRawMaterialMutations';

export default function RawMaterialCreatePage() {
  const navigate = useNavigate();
  const createMutation = useCreateRawMaterial();

  const handleSubmit = (values: RawMaterialFormValues) => {
    createMutation.mutate(
      {
        name: values.name,
        unit_of_measurement: values.unit_of_measurement,
        cost_per_unit: values.cost_per_unit,
        supplier: values.supplier || undefined,
      },
      {
        onSuccess: () => navigate('/app/raw-materials'),
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
        onClick={() => navigate('/app/raw-materials')}
        className="mb-4 flex items-center gap-1 text-sm text-gray-500 hover:text-gray-700"
      >
        <ArrowLeft className="h-4 w-4" />
        Back to Raw Materials
      </button>

      <h2 className="mb-6 text-2xl font-bold text-gray-900">
        Create New Raw Material
      </h2>

      <RawMaterialForm
        mode="create"
        onSubmit={handleSubmit}
        loading={createMutation.isPending}
      />
    </motion.div>
  );
}
