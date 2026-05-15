import type { Product, ProductCost } from '@/types/product';

export interface ProfitabilityItem {
  product: Product;
  cost: ProductCost | null;
  /** Gross margin in dollars: sale_price - cost_price */
  margin: number;
  /** Margin percentage: (margin / sale_price) * 100, null if sale_price is 0 */
  marginPercent: number | null;
  /** True when cost data couldn't be fetched (424 or error) */
  costUnavailable: boolean;
}
