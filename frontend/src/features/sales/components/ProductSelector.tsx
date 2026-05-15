import Select, { type SelectOption } from '@/components/ui/Select';

interface ProductSelectorProps {
  value: string;
  onChange: (productId: string) => void;
  options: SelectOption[];
  loading?: boolean;
  error?: string;
  disabled?: boolean;
}

export default function ProductSelector({
  value,
  onChange,
  options,
  loading = false,
  error,
  disabled = false,
}: ProductSelectorProps) {
  if (disabled && options.length === 0 && !loading) {
    return (
      <div className="flex flex-col gap-1">
        <label className="text-sm font-medium text-gray-700">Product</label>
        <p className="text-sm text-gray-400">
          No active products available.{' '}
          <a href="/app/products/new" className="text-indigo-600 hover:underline">
            Create one
          </a>
        </p>
      </div>
    );
  }

  return (
    <Select
      label="Product"
      options={options}
      value={value}
      onChange={onChange}
      placeholder="Select a product..."
      searchable
      loading={loading}
      error={error}
      disabled={disabled}
    />
  );
}
