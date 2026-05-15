import { motion } from 'framer-motion';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';

interface ProfitMarginBadgeProps {
  marginPercent: number | null;
  costUnavailable?: boolean;
  showIcon?: boolean;
}

export default function ProfitMarginBadge({
  marginPercent,
  costUnavailable = false,
  showIcon = true,
}: ProfitMarginBadgeProps) {
  if (costUnavailable || marginPercent === null) {
    return (
      <span className="inline-flex items-center gap-1 text-sm text-gray-400">
        {showIcon && <Minus className="h-3.5 w-3.5" />}
        —
      </span>
    );
  }

  const isPositive = marginPercent > 0;
  const isZero = marginPercent === 0;

  return (
    <motion.span
      key={marginPercent}
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      className={`inline-flex items-center gap-1 text-sm font-medium ${
        isPositive
          ? 'text-green-600'
          : isZero
            ? 'text-gray-500'
            : 'text-red-600'
      }`}
    >
      {showIcon &&
        (isPositive ? (
          <TrendingUp className="h-3.5 w-3.5" />
        ) : isZero ? (
          <Minus className="h-3.5 w-3.5" />
        ) : (
          <TrendingDown className="h-3.5 w-3.5" />
        ))}
      {marginPercent.toFixed(2)}%
    </motion.span>
  );
}
