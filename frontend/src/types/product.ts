export interface Product {
  id: string;
  tenant_id: string;
  name: string;
  sale_price: string; // DECIMAL(10,2) as string to preserve precision
  is_active: boolean;
  recipe_id: string | null;
  cost_price: string | null;
  created_at: string;
  updated_at: string;
}

export interface ProductCreate {
  name: string;
  sale_price: string;
  is_active?: boolean;
  recipe_id?: string | null;
}

export interface ProductUpdate {
  name?: string;
  sale_price?: string;
  is_active?: boolean;
  recipe_id?: string | null;
}

export interface ProductCostIngredient {
  raw_material_id: string;
  raw_material_name: string;
  quantity: string;
  unit: string;
  unit_cost: string;
  ingredient_total_cost: string;
}

export interface ProductCost {
  product_id: string;
  total_cost: string;
  currency: string;
  cost_source: 'recipe' | 'manual';
  ingredients: ProductCostIngredient[] | null;
  calculated_at: string;
}
