import { useState } from 'react';
import { motion } from 'framer-motion';
import { Pencil, Trash2, Check, X } from 'lucide-react';
import type { RecipeIngredient, RecipeCostIngredient } from '@/types/recipe';
import { formatCurrency } from '@/lib/formatters';
import { VALID_UNITS } from '@/lib/constants';
import Button from '@/components/ui/Button';

interface IngredientRowProps {
  ingredient: RecipeIngredient;
  costInfo?: RecipeCostIngredient;
  onUpdate: (
    ingredientId: string,
    quantity: string,
    unit: string
  ) => void;
  onRemove: (ingredientId: string) => void;
  updating?: boolean;
}

export default function IngredientRow({
  ingredient,
  costInfo,
  onUpdate,
  onRemove,
  updating = false,
}: IngredientRowProps) {
  const [editing, setEditing] = useState(false);
  const [quantity, setQuantity] = useState(ingredient.quantity);
  const [unit, setUnit] = useState(ingredient.unit);

  const handleSave = () => {
    onUpdate(ingredient.id, quantity, unit);
    setEditing(false);
  };

  const handleCancel = () => {
    setQuantity(ingredient.quantity);
    setUnit(ingredient.unit);
    setEditing(false);
  };

  const hasPrice =
    costInfo && parseFloat(costInfo.unit_cost || '0') > 0;

  return (
    <motion.div
      layout
      initial={{ opacity: 0, height: 0 }}
      animate={{ opacity: 1, height: 'auto' }}
      exit={{ opacity: 0, height: 0 }}
      className={`flex items-center gap-4 rounded-lg border px-4 py-3 ${
        costInfo && !hasPrice ? 'border-amber-200 bg-amber-50' : 'border-gray-100'
      }`}
    >
      {/* Name */}
      <div className="min-w-0 flex-1">
        <p className="text-sm font-medium text-gray-900">
          {costInfo?.raw_material_name || ingredient.raw_material_id}
        </p>
        {costInfo && !hasPrice && (
          <p className="text-xs text-amber-600">No price set</p>
        )}
      </div>

      {/* Quantity + Unit */}
      {editing ? (
        <div className="flex items-center gap-2">
          <input
            type="text"
            value={quantity}
            onChange={(e) => setQuantity(e.target.value)}
            className="w-20 rounded-md border border-gray-300 px-2 py-1 text-sm focus:outline-none focus:ring-1 focus:ring-indigo-500"
          />
          <select
            value={unit}
            onChange={(e) => setUnit(e.target.value)}
            className="rounded-md border border-gray-300 px-2 py-1 text-sm focus:outline-none focus:ring-1 focus:ring-indigo-500"
          >
            {VALID_UNITS.map((u) => (
              <option key={u} value={u}>
                {u}
              </option>
            ))}
          </select>
        </div>
      ) : (
        <span className="text-sm text-gray-600">
          {ingredient.quantity} {ingredient.unit}
        </span>
      )}

      {/* Cost */}
      <span className="w-24 text-right text-sm text-gray-700">
        {costInfo ? formatCurrency(costInfo.ingredient_total_cost) : '—'}
      </span>

      {/* Actions */}
      <div className="flex items-center gap-1">
        {editing ? (
          <>
            <Button
              variant="ghost"
              onClick={handleSave}
              className="h-8 w-8 p-0 text-green-600"
              loading={updating}
              title="Save"
            >
              <Check className="h-4 w-4" />
            </Button>
            <Button
              variant="ghost"
              onClick={handleCancel}
              className="h-8 w-8 p-0 text-gray-400"
              title="Cancel"
            >
              <X className="h-4 w-4" />
            </Button>
          </>
        ) : (
          <>
            <Button
              variant="ghost"
              onClick={() => setEditing(true)}
              className="h-8 w-8 p-0"
              title="Edit"
            >
              <Pencil className="h-4 w-4" />
            </Button>
            <Button
              variant="ghost"
              onClick={() => onRemove(ingredient.id)}
              className="h-8 w-8 p-0 text-red-500 hover:text-red-700"
              title="Remove"
            >
              <Trash2 className="h-4 w-4" />
            </Button>
          </>
        )}
      </div>
    </motion.div>
  );
}
