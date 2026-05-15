import { useQuery } from '@tanstack/react-query';
import { getRecipes } from '@/api/recipes';
import Select, { type SelectOption } from '@/components/ui/Select';

interface RecipeSelectorProps {
  label?: string;
  value: string;
  onChange: (value: string) => void;
  error?: string;
}

export default function RecipeSelector({
  label = 'Recipe',
  value,
  onChange,
  error,
}: RecipeSelectorProps) {
  const { data: recipes, isLoading } = useQuery({
    queryKey: ['recipes', { skip: 0, limit: 100 }],
    queryFn: () => getRecipes(0, 100),
  });

  const options: SelectOption[] = [
    { value: '', label: 'None (manual pricing)' },
    ...(recipes?.map((r) => ({ value: r.id, label: r.name })) || []),
  ];

  return (
    <Select
      label={label}
      options={options}
      value={value}
      onChange={onChange}
      placeholder="Select a recipe..."
      loading={isLoading}
      searchable
      error={error}
    />
  );
}
