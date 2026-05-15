import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft } from 'lucide-react';
import RecipeForm, { type RecipeFormValues } from '../components/RecipeForm';
import { useCreateRecipe } from '../hooks/useRecipeMutations';

export default function RecipeCreatePage() {
  const navigate = useNavigate();
  const createMutation = useCreateRecipe();

  const handleSubmit = (values: RecipeFormValues) => {
    createMutation.mutate(
      {
        name: values.name,
        description: values.description || undefined,
      },
      {
        onSuccess: (data) => navigate(`/app/recipes/${data.id}`),
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
        onClick={() => navigate('/app/recipes')}
        className="mb-4 flex items-center gap-1 text-sm text-gray-500 hover:text-gray-700"
      >
        <ArrowLeft className="h-4 w-4" />
        Back to Recipes
      </button>

      <h2 className="mb-6 text-2xl font-bold text-gray-900">
        Create New Recipe
      </h2>

      <RecipeForm
        mode="create"
        onSubmit={handleSubmit}
        loading={createMutation.isPending}
      />
    </motion.div>
  );
}
