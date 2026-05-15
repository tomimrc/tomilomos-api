import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Plus } from 'lucide-react';
import { getRawMaterials } from '@/api/rawMaterials';
import type { RecipeIngredientCreate } from '@/types/recipe';
import { VALID_UNITS } from '@/lib/constants';
import Select, { type SelectOption } from '@/components/ui/Select';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/Input';

interface IngredientFormProps {
  onAdd: (payload: RecipeIngredientCreate) => void;
  adding?: boolean;
}

export default function IngredientForm({
  onAdd,
  adding = false,
}: IngredientFormProps) {
  const [rawMaterialId, setRawMaterialId] = useState('');
  const [quantity, setQuantity] = useState('');
  const [unit, setUnit] = useState('');
  const [quantityError, setQuantityError] = useState('');

  const { data: rawMaterials, isLoading } = useQuery({
    queryKey: ['raw-materials', { skip: 0, limit: 200 }],
    queryFn: () => getRawMaterials(0, 200),
  });

  const materialOptions: SelectOption[] =
    rawMaterials?.map((rm: { id: string; name: string }) => ({
      value: rm.id,
      label: rm.name,
    })) || [];

  const unitOptions: SelectOption[] = VALID_UNITS.map((u) => ({
    value: u,
    label: u,
  }));

  const handleSubmit = () => {
    setQuantityError('');

    if (!rawMaterialId) return;
    if (!quantity || parseFloat(quantity) <= 0) {
      setQuantityError('Quantity must be greater than 0');
      return;
    }
    if (!unit) return;

    onAdd({
      raw_material_id: rawMaterialId,
      quantity,
      unit,
    });

    // Reset form
    setRawMaterialId('');
    setQuantity('');
    setUnit('');
  };

  return (
    <div className="rounded-xl border border-gray-200 bg-white p-4">
      <h4 className="mb-3 text-sm font-semibold text-gray-700">
        Add Ingredient
      </h4>
      <div className="flex items-end gap-3">
        <div className="flex-1">
          <Select
            label="Raw Material"
            options={materialOptions}
            value={rawMaterialId}
            onChange={setRawMaterialId}
            placeholder="Select raw material..."
            loading={isLoading}
            searchable
          />
        </div>
        <div className="w-28">
          <Input
            label="Quantity"
            placeholder="0"
            value={quantity}
            onChange={(e) => setQuantity(e.target.value)}
            error={quantityError}
          />
        </div>
        <div className="w-28">
          <Select
            label="Unit"
            options={unitOptions}
            value={unit}
            onChange={setUnit}
            placeholder="Select..."
          />
        </div>
        <Button
          onClick={handleSubmit}
          disabled={!rawMaterialId || !quantity || !unit}
          loading={adding}
          className="mb-0.5"
        >
          <Plus className="h-4 w-4" />
          Add
        </Button>
      </div>
    </div>
  );
}
