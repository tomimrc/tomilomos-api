export interface Recipe {
  id: string;
  tenant_id: string;
  name: string;
  description: string | null;
  created_at: string;
  updated_at: string;
}

export interface RecipeCreate {
  name: string;
  description?: string;
}

export interface RecipeUpdate {
  name?: string;
  description?: string;
}

export interface RecipeIngredient {
  id: string;
  recipe_id: string;
  raw_material_id: string;
  quantity: string;
  unit: string;
  created_at: string;
  updated_at: string;
}

export interface RecipeIngredientCreate {
  raw_material_id: string;
  quantity: string;
  unit: string;
}

export interface RecipeIngredientUpdate {
  quantity?: string;
  unit?: string;
}

export interface RecipeCostIngredient {
  raw_material_id: string;
  raw_material_name: string;
  quantity: string;
  unit: string;
  unit_cost: string;
  ingredient_total_cost: string;
}

export interface RecipeCost {
  total_cost: string;
  currency: string;
  ingredients: RecipeCostIngredient[];
  calculated_at: string;
}
