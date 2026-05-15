import { useQuery, useQueries } from '@tanstack/react-query';
import { getProducts } from '@/api/products';
import { getProductCost } from '@/api/products';
import type { ProfitabilityItem } from '../types';

export type FilterType = 'all' | 'profitable' | 'unprofitable';

export function useProfitabilityData() {
  // 1. Fetch all products
  const {
    data: products,
    isLoading: productsLoading,
    isError: productsError,
    error: productsErr,
    refetch: refetchProducts,
  } = useQuery({
    queryKey: ['products', { skip: 0, limit: 200 }],
    queryFn: () => getProducts(0, 200),
  });

  // 2. Batch-fetch costs for each product
  const costQueries = useQueries({
    queries: (products || []).map((p) => ({
      queryKey: ['product-cost', p.id] as const,
      queryFn: () => getProductCost(p.id),
      enabled: !!products,
      staleTime: 30_000,
      retry: 1,
    })),
  });

  const costsLoading = costQueries.some((q) => q.isLoading);
  const isLoading = productsLoading || costsLoading;

  // 3. Combine into ProfitabilityItems
  const items: ProfitabilityItem[] = (products || []).map((product, idx) => {
    const costQuery = costQueries[idx];
    const cost = costQuery?.data ?? null;
    const costUnavailable = costQuery?.isError ?? false;

    const costPrice = cost
      ? parseFloat(cost.total_cost)
      : 0;
    const salePrice = parseFloat(product.sale_price);
    const margin = salePrice - costPrice;
    const marginPercent = salePrice > 0 ? (margin / salePrice) * 100 : null;

    return {
      product,
      cost,
      margin,
      marginPercent,
      costUnavailable,
    };
  });

  // 4. Compute summary KPIs
  const withValidCosts = items.filter(
    (i) => !i.costUnavailable && i.marginPercent !== null
  );
  const avgMargin =
    withValidCosts.length > 0
      ? withValidCosts.reduce((sum, i) => sum + (i.marginPercent ?? 0), 0) /
        withValidCosts.length
      : null;

  const sorted = [...items].sort(
    (a, b) => (b.marginPercent ?? -Infinity) - (a.marginPercent ?? -Infinity)
  );
  const mostProfitable = sorted[0] ?? null;
  const leastProfitable = sorted[sorted.length - 1] ?? null;

  const activeProducts = items.filter((i) => i.product.is_active).length;
  const excludedCount = items.length - withValidCosts.length;

  return {
    items,
    isLoading,
    isError: productsError,
    error: productsErr as Error | null,
    refetch: refetchProducts,
    summary: {
      avgMargin,
      mostProfitable,
      leastProfitable,
      activeProducts,
      totalProducts: items.length,
      excludedCount,
    },
  };
}
