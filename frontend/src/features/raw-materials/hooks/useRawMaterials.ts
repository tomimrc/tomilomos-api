import { useQuery } from '@tanstack/react-query';
import { getRawMaterials } from '@/api/rawMaterials';

export function useRawMaterials(skip = 0, limit = 200) {
  return useQuery({
    queryKey: ['raw-materials', { skip, limit }],
    queryFn: () => getRawMaterials(skip, limit),
  });
}
