export interface RawMaterial {
  id: string;
  tenant_id: string;
  name: string;
  unit_of_measurement: string;
  cost_per_unit: string; // DECIMAL(10,2) as string to preserve precision
  supplier: string | null;
  current_stock: string;
  created_at: string;
  updated_at: string;
}

export interface RawMaterialCreate {
  name: string;
  unit_of_measurement: string;
  cost_per_unit: string;
  supplier?: string | null;
}

export interface RawMaterialUpdate {
  name?: string;
  unit_of_measurement?: string;
  cost_per_unit?: string;
  supplier?: string | null;
}

export interface StockLevel {
  id: string;
  current_stock: string;
}
