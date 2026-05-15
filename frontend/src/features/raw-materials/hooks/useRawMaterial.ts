import { useQuery } from '@tanstack/react-query';
import { getRawMaterial, getStock } from '@/api/rawMaterials';

export function useRawMaterial(id: string) {
  return useQuery({
    queryKey: ['raw-material', id],
    queryFn: () => getRawMaterial(id),
    enabled: !!id,
  });
}

export function useRawMaterialStock(id: string) {
  return useQuery({
    queryKey: ['raw-material-stock', id],
    queryFn: () => getStock(id),
    enabled: !!id,
  });
}
