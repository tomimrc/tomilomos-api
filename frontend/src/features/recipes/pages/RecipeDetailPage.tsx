import { useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { ArrowLeft, Pencil, Trash2 } from 'lucide-react';
import { useQuery } from '@tanstack/react-query';
import { getProducts } from '@/api/products';
import {
  useRecipe,
  useRecipeIngredients,
  useRecipeCost,
} from '../hooks/useRecipe';
import {
  useAddIngredient,
  useUpdateIngredient,
  useRemoveIngredient,
} from '../hooks/useIngredientMutations';
import { useDeleteRecipe } from '../hooks/useRecipeMutations';
import RecipeCostDisplay from '../components/RecipeCostDisplay';
import IngredientForm from '../components/IngredientForm';
import IngredientRow from '../components/IngredientRow';
import Button from '@/components/ui/Button';
import ConfirmDialog from '@/components/shared/ConfirmDialog';
import LoadingSkeleton from '@/components/shared/LoadingSkeleton';
import ErrorState from '@/components/shared/ErrorState';
import EmptyState from '@/components/shared/EmptyState';
import type { RecipeIngredientCreate } from '@/types/recipe';

export default function RecipeDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const { data: recipe, isLoading, isError, refetch } = useRecipe(id!);
  const { data: ingredients, isLoading: ingLoading } =
    useRecipeIngredients(id!);
  const { data: cost } = useRecipeCost(id!);

  // Products linked to this recipe
  const { data: allProducts } = useQuery({
    queryKey: ['products', { skip: 0, limit: 200 }],
    queryFn: () => getProducts(0, 200),
  });
  const linkedProducts =
    allProducts?.filter((p) => p.recipe_id === id) || [];

  const addIngredient = useAddIngredient(id!);
  const updateIngredient = useUpdateIngredient(id!);
  const removeIngredient = useRemoveIngredient(id!);
  const deleteRecipe = useDeleteRecipe();
  const [showDelete, setShowDelete] = useState(false);

  if (isLoading) {
    return <LoadingSkeleton variant="card" rows={3} />;
  }

  if (isError || !recipe) {
    return (
      <ErrorState
        message="Recipe not found"
        onRetry={() => refetch()}
      />
    );
  }

  const handleAdd = (payload: RecipeIngredientCreate) => {
    addIngredient.mutate(payload);
  };

  const handleUpdate = (
    ingredientId: string,
    quantity: string,
    unit: string
  ) => {
    updateIngredient.mutate({ ingredientId, payload: { quantity, unit } });
  };

  const handleRemove = (ingredientId: string) => {
    removeIngredient.mutate(ingredientId);
  };

  const handleDelete = () => {
    deleteRecipe.mutate(recipe.id, {
      onSuccess: () => navigate('/app/recipes'),
    });
  };

  // Match ingredients with cost data
  const getCostForIngredient = (ingId: string) =>
    cost?.ingredients?.find(
      (c) =>
        c.raw_material_id ===
        ingredients?.find((i) => i.id === ingId)?.raw_material_id
    );

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -12 }}
      className="mx-auto max-w-3xl"
    >
      {/* Back + Actions */}
      <div className="mb-4 flex items-center justify-between">
        <button
          onClick={() => navigate('/app/recipes')}
          className="flex items-center gap-1 text-sm text-gray-500 hover:text-gray-700"
        >
          <ArrowLeft className="h-4 w-4" />
          Back to Recipes
        </button>
        <div className="flex items-center gap-2">
          <Button
            variant="secondary"
            onClick={() => navigate(`/app/recipes/${recipe.id}/edit`)}
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

      {/* Recipe Info */}
      <div className="mb-6 rounded-xl border border-gray-200 bg-white p-6">
        <h2 className="text-2xl font-bold text-gray-900">{recipe.name}</h2>
        {recipe.description && (
          <p className="mt-2 text-sm text-gray-500">{recipe.description}</p>
        )}

        {/* Linked Products */}
        {linkedProducts.length > 0 && (
          <div className="mt-4 border-t pt-4">
            <p className="mb-2 text-sm font-medium text-gray-500">
              Used in {linkedProducts.length} product{linkedProducts.length > 1 ? 's' : ''}
            </p>
            <div className="flex flex-wrap gap-2">
              {linkedProducts.map((p) => (
                <Link
                  key={p.id}
                  to={`/app/products/${p.id}`}
                  className="rounded-full bg-indigo-50 px-3 py-1 text-sm text-indigo-700 transition-colors hover:bg-indigo-100"
                >
                  {p.name}
                </Link>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Cost Display */}
      <RecipeCostDisplay recipeId={recipe.id} />

      {/* Add Ingredient Form */}
      <IngredientForm onAdd={handleAdd} adding={addIngredient.isPending} />

      {/* Ingredients List */}
      <div className="mt-4 space-y-2">
        {ingLoading && (
          <LoadingSkeleton variant="card" rows={3} />
        )}

        {!ingLoading && ingredients?.length === 0 && (
          <EmptyState
            title="No ingredients yet"
            description="Add your first ingredient above to build this recipe."
          />
        )}

        <AnimatePresence>
          {ingredients?.map((ing) => (
            <IngredientRow
              key={ing.id}
              ingredient={ing}
              costInfo={getCostForIngredient(ing.id)}
              onUpdate={handleUpdate}
              onRemove={handleRemove}
              updating={updateIngredient.isPending}
            />
          ))}
        </AnimatePresence>
      </div>

      <ConfirmDialog
        open={showDelete}
        onClose={() => setShowDelete(false)}
        onConfirm={handleDelete}
        title="Delete Recipe"
        message={`Are you sure you want to delete "${recipe.name}"? Products linked to this recipe will have their recipe unlinked.`}
        loading={deleteRecipe.isPending}
      />
    </motion.div>
  );
}
