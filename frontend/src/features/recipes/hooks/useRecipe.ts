import { useQuery } from '@tanstack/react-query';
import {
  getRecipe,
  getRecipeIngredients,
  getRecipeCost,
} from '@/api/recipes';

export function useRecipe(id: string) {
  return useQuery({
    queryKey: ['recipe', id],
    queryFn: () => getRecipe(id),
    enabled: !!id,
  });
}

export function useRecipeIngredients(recipeId: string) {
  return useQuery({
    queryKey: ['recipe-ingredients', recipeId],
    queryFn: () => getRecipeIngredients(recipeId),
    enabled: !!recipeId,
  });
}

export function useRecipeCost(recipeId: string) {
  return useQuery({
    queryKey: ['recipe-cost', recipeId],
    queryFn: () => getRecipeCost(recipeId),
    enabled: !!recipeId,
  });
}
