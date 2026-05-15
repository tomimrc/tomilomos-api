import { useQuery } from '@tanstack/react-query';
import { getProduct, getProductCost } from '@/api/products';

export function useProduct(id: string) {
  return useQuery({
    queryKey: ['product', id],
    queryFn: () => getProduct(id),
    enabled: !!id,
  });
}

export function useProductCost(id: string) {
  return useQuery({
    queryKey: ['product-cost', id],
    queryFn: () => getProductCost(id),
    enabled: !!id,
  });
}
