import apiClient from './client';
import type {
  Recipe,
  RecipeCreate,
  RecipeUpdate,
  RecipeIngredient,
  RecipeIngredientCreate,
  RecipeIngredientUpdate,
  RecipeCost,
} from '@/types/recipe';

// Recipe CRUD
export async function getRecipes(
  skip = 0,
  limit = 100
): Promise<Recipe[]> {
  const { data } = await apiClient.get<Recipe[]>('/recipes', {
    params: { skip, limit },
  });
  return data;
}

export async function getRecipe(id: string): Promise<Recipe> {
  const { data } = await apiClient.get<Recipe>(`/recipes/${id}`);
  return data;
}

export async function createRecipe(
  payload: RecipeCreate
): Promise<Recipe> {
  const { data } = await apiClient.post<Recipe>('/recipes', payload);
  return data;
}

export async function updateRecipe(
  id: string,
  payload: RecipeUpdate
): Promise<Recipe> {
  const { data } = await apiClient.put<Recipe>(`/recipes/${id}`, payload);
  return data;
}

export async function deleteRecipe(id: string): Promise<void> {
  await apiClient.delete(`/recipes/${id}`);
}

// Recipe Ingredients
export async function getRecipeIngredients(
  recipeId: string
): Promise<RecipeIngredient[]> {
  const { data } = await apiClient.get<RecipeIngredient[]>(
    `/recipes/${recipeId}/ingredients`
  );
  return data;
}

export async function addRecipeIngredient(
  recipeId: string,
  payload: RecipeIngredientCreate
): Promise<RecipeIngredient> {
  const { data } = await apiClient.post<RecipeIngredient>(
    `/recipes/${recipeId}/ingredients`,
    payload
  );
  return data;
}

export async function updateRecipeIngredient(
  recipeId: string,
  ingredientId: string,
  payload: RecipeIngredientUpdate
): Promise<RecipeIngredient> {
  const { data } = await apiClient.put<RecipeIngredient>(
    `/recipes/${recipeId}/ingredients/${ingredientId}`,
    payload
  );
  return data;
}

export async function removeRecipeIngredient(
  recipeId: string,
  ingredientId: string
): Promise<void> {
  await apiClient.delete(
    `/recipes/${recipeId}/ingredients/${ingredientId}`
  );
}

// Recipe Cost
export async function getRecipeCost(
  recipeId: string
): Promise<RecipeCost> {
  const { data } = await apiClient.get<RecipeCost>(
    `/recipes/${recipeId}/cost`
  );
  return data;
}
