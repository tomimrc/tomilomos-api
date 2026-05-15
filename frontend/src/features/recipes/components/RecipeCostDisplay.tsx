import { AlertTriangle } from 'lucide-react';
import { useRecipeCost } from '../hooks/useRecipe';
import { formatCurrency } from '@/lib/formatters';

interface RecipeCostDisplayProps {
  recipeId: string;
}

export default function RecipeCostDisplay({
  recipeId,
}: RecipeCostDisplayProps) {
  const { data: cost, isLoading, isError } = useRecipeCost(recipeId);

  if (isLoading) {
    return (
      <div className="rounded-xl border border-gray-200 bg-white p-6">
        <div className="h-8 w-32 animate-pulse rounded bg-gray-200" />
      </div>
    );
  }

  // 424 — partial data
  if (isError) {
    return (
      <div className="mb-4 rounded-lg border border-amber-200 bg-amber-50 p-3">
        <div className="flex items-center gap-2">
          <AlertTriangle className="h-5 w-5 text-amber-500" />
          <p className="text-sm font-medium text-amber-800">
            Cost may be incomplete — some ingredients have no price
          </p>
        </div>
      </div>
    );
  }

  if (!cost) return null;

  return (
    <div className="mb-6 flex items-center justify-between rounded-xl border border-gray-200 bg-white p-4">
      <div>
        <p className="text-sm text-gray-500">Total Recipe Cost</p>
        <p className="text-2xl font-bold text-gray-900">
          {formatCurrency(cost.total_cost)}
        </p>
      </div>
      <div className="text-right text-xs text-gray-400">
        {cost.currency} · {cost.ingredients.length} ingredients
      </div>
    </div>
  );
}
