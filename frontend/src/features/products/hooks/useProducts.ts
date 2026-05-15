import { useQuery } from '@tanstack/react-query';
import { getProducts } from '@/api/products';

export function useProducts(skip = 0, limit = 100) {
  return useQuery({
    queryKey: ['products', { skip, limit }],
    queryFn: () => getProducts(skip, limit),
  });
}
