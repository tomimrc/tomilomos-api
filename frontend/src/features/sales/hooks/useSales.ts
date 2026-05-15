import { useQuery } from '@tanstack/react-query';
import { getSales } from '@/api/sales';

export function useSales(skip = 0, limit = 50) {
  return useQuery({
    queryKey: ['sales', { skip, limit }],
    queryFn: () => getSales(skip, limit),
  });
}
