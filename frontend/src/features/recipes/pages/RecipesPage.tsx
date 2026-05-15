import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Plus } from 'lucide-react';
import { useRecipes } from '../hooks/useRecipes';
import { useDeleteRecipe } from '../hooks/useRecipeMutations';
import RecipeTable from '../components/RecipeTable';
import Button from '@/components/ui/Button';
import LoadingSkeleton from '@/components/shared/LoadingSkeleton';
import EmptyState from '@/components/shared/EmptyState';
import ErrorState from '@/components/shared/ErrorState';
import ConfirmDialog from '@/components/shared/ConfirmDialog';
import type { Recipe } from '@/types/recipe';

export default function RecipesPage() {
  const navigate = useNavigate();
  const { data: recipes, isLoading, isError, refetch } = useRecipes();
  const deleteMutation = useDeleteRecipe();
  const [deleteTarget, setDeleteTarget] = useState<Recipe | null>(null);

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -12 }}
      transition={{ duration: 0.2 }}
    >
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Recipes</h2>
          <p className="text-sm text-gray-500">
            Manage your recipes and ingredient lists
          </p>
        </div>
        <Button onClick={() => navigate('/app/recipes/new')}>
          <Plus className="h-4 w-4" />
          New Recipe
        </Button>
      </div>

      {isLoading && <LoadingSkeleton variant="table-row" rows={6} />}

      {isError && !isLoading && <ErrorState onRetry={() => refetch()} />}

      {!isLoading && !isError && recipes?.length === 0 && (
        <EmptyState
          title="No recipes yet"
          description="Create your first recipe to start building your menu."
          actionLabel="Create your first recipe"
          onAction={() => navigate('/app/recipes/new')}
        />
      )}

      {!isLoading && !isError && recipes && recipes.length > 0 && (
        <RecipeTable
          recipes={recipes}
          onDelete={(recipe) => setDeleteTarget(recipe)}
        />
      )}

      <ConfirmDialog
        open={!!deleteTarget}
        onClose={() => setDeleteTarget(null)}
        onConfirm={() => {
          if (deleteTarget) {
            deleteMutation.mutate(deleteTarget.id);
            setDeleteTarget(null);
          }
        }}
        title="Delete Recipe"
        message={`Are you sure you want to delete "${deleteTarget?.name}"? Products linked to this recipe will have their recipe unlinked.`}
        loading={deleteMutation.isPending}
      />
    </motion.div>
  );
}
