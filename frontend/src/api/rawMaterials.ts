import apiClient from './client';
import type {
  RawMaterial,
  RawMaterialCreate,
  RawMaterialUpdate,
  StockLevel,
} from '@/types/rawMaterial';

// ── List ──────────────────────────────────────────────
export async function getRawMaterials(
  skip = 0,
  limit = 200
): Promise<RawMaterial[]> {
  const { data } = await apiClient.get<RawMaterial[]>('/raw-materials', {
    params: { skip, limit },
  });
  return data;
}

// ── Single ────────────────────────────────────────────
export async function getRawMaterial(id: string): Promise<RawMaterial> {
  const { data } = await apiClient.get<RawMaterial>(`/raw-materials/${id}`);
  return data;
}

// ── Create ────────────────────────────────────────────
export async function createRawMaterial(
  payload: RawMaterialCreate
): Promise<RawMaterial> {
  const { data } = await apiClient.post<RawMaterial>(
    '/raw-materials',
    payload
  );
  return data;
}

// ── Update ────────────────────────────────────────────
export async function updateRawMaterial(
  id: string,
  payload: RawMaterialUpdate
): Promise<RawMaterial> {
  const { data } = await apiClient.put<RawMaterial>(
    `/raw-materials/${id}`,
    payload
  );
  return data;
}

// ── Delete ────────────────────────────────────────────
export async function deleteRawMaterial(id: string): Promise<void> {
  await apiClient.delete(`/raw-materials/${id}`);
}

// ── Stock ─────────────────────────────────────────────
export interface StockAdjustmentPayload {
  quantity: string;
  reason?: string | null;
}

export async function addStock(
  id: string,
  payload: StockAdjustmentPayload
): Promise<{ id: string; current_stock: string }> {
  const { data } = await apiClient.post<{ id: string; current_stock: string }>(
    `/raw-materials/${id}/add-stock`,
    payload
  );
  return data;
}

export async function removeStock(
  id: string,
  payload: StockAdjustmentPayload
): Promise<{ id: string; current_stock: string }> {
  const { data } = await apiClient.post<{ id: string; current_stock: string }>(
    `/raw-materials/${id}/remove-stock`,
    payload
  );
  return data;
}

export async function getStock(id: string): Promise<StockLevel> {
  const { data } = await apiClient.get<StockLevel>(
    `/raw-materials/${id}/stock`
  );
  return data;
}
