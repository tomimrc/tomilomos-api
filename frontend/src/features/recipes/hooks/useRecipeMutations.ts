import { useMutation, useQueryClient } from '@tanstack/react-query';
import toast from 'react-hot-toast';
import {
  createRecipe,
  updateRecipe,
  deleteRecipe,
} from '@/api/recipes';
import type { RecipeCreate, RecipeUpdate } from '@/types/recipe';

export function useCreateRecipe() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (payload: RecipeCreate) => createRecipe(payload),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['recipes'] });
      toast.success('Recipe created successfully');
    },
    onError: (error: unknown) => {
      const msg =
        (error as { response?: { data?: { detail?: string } } })?.response
          ?.data?.detail || 'Failed to create recipe';
      toast.error(msg);
    },
  });
}

export function useUpdateRecipe() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: RecipeUpdate }) =>
      updateRecipe(id, payload),
    onSuccess: (_, { id }) => {
      qc.invalidateQueries({ queryKey: ['recipes'] });
      qc.invalidateQueries({ queryKey: ['recipe', id] });
      toast.success('Recipe updated');
    },
    onError: (error: unknown) => {
      const msg =
        (error as { response?: { data?: { detail?: string } } })?.response
          ?.data?.detail || 'Failed to update recipe';
      toast.error(msg);
    },
  });
}

export function useDeleteRecipe() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => deleteRecipe(id),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['recipes'] });
      toast.success('Recipe deleted');
    },
    onError: () => {
      toast.error('Failed to delete recipe');
    },
  });
}
