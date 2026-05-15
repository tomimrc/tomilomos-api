import { useMutation, useQueryClient } from '@tanstack/react-query';
import toast from 'react-hot-toast';
import {
  createRawMaterial,
  updateRawMaterial,
  deleteRawMaterial,
  addStock,
  removeStock,
  type StockAdjustmentPayload,
} from '@/api/rawMaterials';
import type { RawMaterialCreate, RawMaterialUpdate } from '@/types/rawMaterial';

// ── Create ────────────────────────────────────────────
export function useCreateRawMaterial() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (payload: RawMaterialCreate) => createRawMaterial(payload),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['raw-materials'] });
      toast.success('Raw material created');
    },
    onError: (error: unknown) => {
      const msg =
        (error as { response?: { data?: { detail?: string } } })?.response?.data
          ?.detail || 'Failed to create raw material';
      toast.error(msg);
    },
  });
}

// ── Update ────────────────────────────────────────────
export function useUpdateRawMaterial() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({
      id,
      payload,
    }: {
      id: string;
      payload: RawMaterialUpdate;
    }) => updateRawMaterial(id, payload),
    onSuccess: (_, { id }) => {
      qc.invalidateQueries({ queryKey: ['raw-materials'] });
      qc.invalidateQueries({ queryKey: ['raw-material', id] });
      // Cost change → invalidate recipe and product costs
      qc.invalidateQueries({ queryKey: ['recipe-cost'] });
      qc.invalidateQueries({ queryKey: ['product-cost'] });
      toast.success('Raw material updated');
    },
    onError: (error: unknown) => {
      const msg =
        (error as { response?: { data?: { detail?: string } } })?.response?.data
          ?.detail || 'Failed to update raw material';
      toast.error(msg);
    },
  });
}

// ── Delete ────────────────────────────────────────────
export function useDeleteRawMaterial() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => deleteRawMaterial(id),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['raw-materials'] });
      toast.success('Raw material deleted');
    },
    onError: (error: unknown) => {
      const msg =
        (error as { response?: { data?: { detail?: string } } })?.response?.data
          ?.detail || 'Cannot delete — this material is used in recipes';
      toast.error(msg);
    },
  });
}

// ── Add Stock ─────────────────────────────────────────
export function useAddStock() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({
      id,
      payload,
    }: {
      id: string;
      payload: StockAdjustmentPayload;
    }) => addStock(id, payload),
    onSuccess: (_, { id }) => {
      qc.invalidateQueries({ queryKey: ['raw-materials'] });
      qc.invalidateQueries({ queryKey: ['raw-material', id] });
      qc.invalidateQueries({ queryKey: ['raw-material-stock', id] });
      toast.success('Stock added successfully');
    },
    onError: (error: unknown) => {
      const msg =
        (error as { response?: { data?: { detail?: string } } })?.response?.data
          ?.detail || 'Failed to add stock';
      toast.error(msg);
    },
  });
}

// ── Remove Stock ──────────────────────────────────────
export function useRemoveStock() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({
      id,
      payload,
    }: {
      id: string;
      payload: StockAdjustmentPayload;
    }) => removeStock(id, payload),
    onSuccess: (_, { id }) => {
      qc.invalidateQueries({ queryKey: ['raw-materials'] });
      qc.invalidateQueries({ queryKey: ['raw-material', id] });
      qc.invalidateQueries({ queryKey: ['raw-material-stock', id] });
      toast.success('Stock removed successfully');
    },
    onError: (error: unknown) => {
      const msg =
        (error as { response?: { data?: { detail?: string } } })?.response?.data
          ?.detail || 'Failed to remove stock';
      toast.error(msg);
    },
  });
}
