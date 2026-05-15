import { useQuery } from '@tanstack/react-query';
import { getRecipes } from '@/api/recipes';

export function useRecipes(skip = 0, limit = 100) {
  return useQuery({
    queryKey: ['recipes', { skip, limit }],
    queryFn: () => getRecipes(skip, limit),
  });
}
