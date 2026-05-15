import apiClient from './client';
import type {
  Product,
  ProductCreate,
  ProductUpdate,
  ProductCost,
} from '@/types/product';

export async function getProducts(
  skip = 0,
  limit = 100
): Promise<Product[]> {
  const { data } = await apiClient.get<Product[]>('/products', {
    params: { skip, limit },
  });
  return data;
}

export async function getProduct(id: string): Promise<Product> {
  const { data } = await apiClient.get<Product>(`/products/${id}`);
  return data;
}

export async function createProduct(
  payload: ProductCreate
): Promise<Product> {
  const { data } = await apiClient.post<Product>('/products', payload);
  return data;
}

export async function updateProduct(
  id: string,
  payload: ProductUpdate
): Promise<Product> {
  const { data } = await apiClient.put<Product>(`/products/${id}`, payload);
  return data;
}

export async function deleteProduct(id: string): Promise<void> {
  await apiClient.delete(`/products/${id}`);
}

export async function getProductCost(id: string): Promise<ProductCost> {
  const { data } = await apiClient.get<ProductCost>(`/products/${id}/cost`);
  return data;
}
