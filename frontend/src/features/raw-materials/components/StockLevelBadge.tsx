import { CheckCircle, AlertTriangle, AlertCircle } from 'lucide-react';

interface StockLevelBadgeProps {
  stock: number;
  showLabel?: boolean;
}

export default function StockLevelBadge({
  stock,
  showLabel = true,
}: StockLevelBadgeProps) {
  if (stock > 10) {
    return (
      <span className="inline-flex items-center gap-1.5 rounded-full bg-green-50 px-2.5 py-1 text-xs font-medium text-green-700">
        <CheckCircle className="h-3.5 w-3.5" />
        <span>{stock.toFixed(2)}</span>
        {showLabel && <span className="opacity-75">In stock</span>}
      </span>
    );
  }

  if (stock > 0) {
    return (
      <span className="inline-flex items-center gap-1.5 rounded-full bg-amber-50 px-2.5 py-1 text-xs font-medium text-amber-700">
        <AlertTriangle className="h-3.5 w-3.5" />
        <span>{stock.toFixed(2)}</span>
        {showLabel && <span className="opacity-75">Low stock</span>}
      </span>
    );
  }

  return (
    <span className="inline-flex items-center gap-1.5 rounded-full bg-red-50 px-2.5 py-1 text-xs font-medium text-red-700">
      <AlertCircle className="h-3.5 w-3.5" />
      <span>0</span>
      {showLabel && <span className="opacity-75">Out of stock</span>}
    </span>
  );
}
