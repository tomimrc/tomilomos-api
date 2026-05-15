import { useMutation, useQueryClient } from '@tanstack/react-query';
import toast from 'react-hot-toast';
import {
  addRecipeIngredient,
  updateRecipeIngredient,
  removeRecipeIngredient,
} from '@/api/recipes';
import type {
  RecipeIngredientCreate,
  RecipeIngredientUpdate,
} from '@/types/recipe';

export function useAddIngredient(recipeId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (payload: RecipeIngredientCreate) =>
      addRecipeIngredient(recipeId, payload),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['recipe-ingredients', recipeId] });
      qc.invalidateQueries({ queryKey: ['recipe-cost', recipeId] });
      qc.invalidateQueries({ queryKey: ['products'] });
      toast.success('Ingredient added');
    },
    onError: (error: unknown) => {
      const msg =
        (error as { response?: { data?: { detail?: string } } })?.response
          ?.data?.detail || 'Failed to add ingredient';
      toast.error(msg);
    },
  });
}

export function useUpdateIngredient(recipeId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({
      ingredientId,
      payload,
    }: {
      ingredientId: string;
      payload: RecipeIngredientUpdate;
    }) => updateRecipeIngredient(recipeId, ingredientId, payload),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['recipe-ingredients', recipeId] });
      qc.invalidateQueries({ queryKey: ['recipe-cost', recipeId] });
      qc.invalidateQueries({ queryKey: ['products'] });
      toast.success('Ingredient updated');
    },
    onError: () => {
      toast.error('Failed to update ingredient');
    },
  });
}

export function useRemoveIngredient(recipeId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (ingredientId: string) =>
      removeRecipeIngredient(recipeId, ingredientId),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['recipe-ingredients', recipeId] });
      qc.invalidateQueries({ queryKey: ['recipe-cost', recipeId] });
      qc.invalidateQueries({ queryKey: ['products'] });
      toast.success('Ingredient removed');
    },
    onError: () => {
      toast.error('Failed to remove ingredient');
    },
  });
}
