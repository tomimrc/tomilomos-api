import apiClient from './client';
import type { Sale, SaleCreate } from '@/types/sale';

export async function createSale(payload: SaleCreate): Promise<Sale> {
  const { data } = await apiClient.post<Sale>('/sales', payload);
  return data;
}

export async function getSales(skip = 0, limit = 50): Promise<Sale[]> {
  const { data } = await apiClient.get<Sale[]>('/sales', {
    params: { skip, limit },
  });
  return data;
}

export async function getSale(id: string): Promise<Sale> {
  const { data } = await apiClient.get<Sale>(`/sales/${id}`);
  return data;
}
