import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft } from 'lucide-react';
import RecipeForm, { type RecipeFormValues } from '../components/RecipeForm';
import { useRecipe } from '../hooks/useRecipe';
import { useUpdateRecipe } from '../hooks/useRecipeMutations';
import LoadingSkeleton from '@/components/shared/LoadingSkeleton';
import ErrorState from '@/components/shared/ErrorState';

export default function RecipeEditPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { data: recipe, isLoading, isError, refetch } = useRecipe(id!);
  const updateMutation = useUpdateRecipe();

  const handleSubmit = (values: RecipeFormValues) => {
    if (!id) return;
    updateMutation.mutate(
      {
        id,
        payload: {
          name: values.name,
          description: values.description || undefined,
        },
      },
      {
        onSuccess: () => navigate(`/app/recipes/${id}`),
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
        onClick={() => navigate(`/app/recipes/${id}`)}
        className="mb-4 flex items-center gap-1 text-sm text-gray-500 hover:text-gray-700"
      >
        <ArrowLeft className="h-4 w-4" />
        Back to Recipe
      </button>

      <h2 className="mb-6 text-2xl font-bold text-gray-900">Edit Recipe</h2>

      {isLoading && <LoadingSkeleton variant="card" rows={1} />}

      {isError && !isLoading && <ErrorState onRetry={() => refetch()} />}

      {recipe && (
        <RecipeForm
          mode="edit"
          defaultValues={recipe}
          onSubmit={handleSubmit}
          loading={updateMutation.isPending}
        />
      )}
    </motion.div>
  );
}
