export interface Sale {
  id: string;
  tenant_id: string;
  product_id: string;
  product_name: string;
  quantity: number;
  unit_price: string; // DECIMAL(10,2)
  total_price: string;
  total_cost: string | null;
  margin: string | null;
  created_at: string;
}

export interface SaleCreate {
  product_id: string;
  quantity: number;
}
