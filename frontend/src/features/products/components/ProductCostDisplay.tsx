import { Link } from 'react-router-dom';
import { AlertTriangle } from 'lucide-react';
import { useProductCost } from '../hooks/useProduct';
import { useQuery } from '@tanstack/react-query';
import { getRecipe } from '@/api/recipes';
import { formatCurrency } from '@/lib/formatters';
import LoadingSkeleton from '@/components/shared/LoadingSkeleton';

interface ProductCostDisplayProps {
  productId: string;
  recipeId: string | null;
}

export default function ProductCostDisplay({
  productId,
  recipeId,
}: ProductCostDisplayProps) {
  const {
    data: cost,
    isLoading,
    isError,
  } = useProductCost(productId);

  const { data: recipe } = useQuery({
    queryKey: ['recipe', recipeId],
    queryFn: () => getRecipe(recipeId!),
    enabled: !!recipeId,
  });

  if (isLoading) {
    return <LoadingSkeleton variant="card" rows={1} />;
  }

  // 424 or other error
  if (isError) {
    return (
      <div className="rounded-lg border border-amber-200 bg-amber-50 p-4">
        <div className="flex items-center gap-2">
          <AlertTriangle className="h-5 w-5 text-amber-500" />
          <p className="text-sm font-medium text-amber-800">
            Cost cannot be fully calculated — some ingredients lack pricing
          </p>
        </div>
      </div>
    );
  }

  if (!cost) return null;

  return (
    <div className="rounded-xl border border-gray-200 bg-white p-6">
      <h3 className="mb-4 text-lg font-semibold text-gray-900">
        Cost Information
      </h3>

      <div className="grid gap-4 sm:grid-cols-2">
        <div>
          <p className="text-sm text-gray-500">Total Cost</p>
          <p className="text-2xl font-bold text-gray-900">
            {formatCurrency(cost.total_cost)}
          </p>
        </div>

        <div>
          <p className="text-sm text-gray-500">Cost Source</p>
          <p className="text-sm font-medium text-gray-700">
            {cost.cost_source === 'recipe' ? (
              <>
                Based on recipe:{' '}
                {recipe ? (
                  <Link
                    to={`/app/recipes/${recipe.id}`}
                    className="text-indigo-600 hover:text-indigo-800"
                  >
                    {recipe.name}
                  </Link>
                ) : (
                  'Unknown recipe'
                )}
              </>
            ) : (
              'Manual pricing — no recipe linked'
            )}
          </p>
        </div>
      </div>

      {/* Ingredient breakdown */}
      {cost.ingredients && cost.ingredients.length > 0 && (
        <div className="mt-4">
          <p className="mb-2 text-sm font-medium text-gray-500">
            Ingredient Breakdown
          </p>
          <div className="space-y-2">
            {cost.ingredients.map((ing) => (
              <div
                key={ing.raw_material_id}
                className="flex items-center justify-between rounded-lg bg-gray-50 px-3 py-2 text-sm"
              >
                <div>
                  <span className="font-medium text-gray-700">
                    {ing.raw_material_name}
                  </span>
                  <span className="ml-2 text-gray-400">
                    {ing.quantity} {ing.unit}
                  </span>
                </div>
                <span className="text-gray-600">
                  {formatCurrency(ing.ingredient_total_cost)}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
