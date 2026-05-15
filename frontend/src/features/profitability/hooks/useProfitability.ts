import { useMemo } from 'react';
import { useQueries } from '@tanstack/react-query';
import { useProducts } from '@/features/products/hooks/useProducts';
import { getProductCost } from '@/api/products';
import type { Product } from '@/types/product';
import type { ProductCost } from '@/types/product';

export interface ProfitabilityRow {
  product: Product;
  cost: ProductCost | null;
  costLoading: boolean;
  costAvailable: boolean;
  marginDollars: number | null;
  marginPercent: number | null;
}

function calcMargin(
  salePrice: number,
  costPrice: number | null
): { marginDollars: number | null; marginPercent: number | null } {
  if (salePrice === 0 || costPrice === null) {
    return { marginDollars: null, marginPercent: null };
  }
  const dollars = salePrice - costPrice;
  const percent = (dollars / salePrice) * 100;
  return {
    marginDollars: Math.round(dollars * 100) / 100,
    marginPercent: Math.round(percent * 100) / 100,
  };
}

export function useProfitability() {
  const {
    data: products,
    isLoading: productsLoading,
    isError: productsError,
    refetch: refetchProducts,
  } = useProducts(0, 1000);

  const activeProducts = useMemo(
    () => (products ?? []).filter((p) => p.is_active),
    [products]
  );

  const costQueries = useQueries({
    queries: activeProducts.map((product) => ({
      queryKey: ['product-cost', product.id],
      queryFn: () => getProductCost(product.id),
      enabled: activeProducts.length > 0,
      retry: false, // 424 means cost unavailable — don't retry
    })),
  });

  const rows: ProfitabilityRow[] = useMemo(() => {
    return activeProducts.map((product, i) => {
      const costQuery = costQueries[i];
      const cost: ProductCost | null =
        costQuery?.status === 'success' ? costQuery.data : null;
      const costAvailable = cost !== null;
      const salePrice = parseFloat(product.sale_price);
      const costPrice = cost ? parseFloat(cost.total_cost) : null;

      const { marginDollars, marginPercent } = calcMargin(salePrice, costPrice);

      return {
        product,
        cost,
        costLoading: costQuery?.status === 'pending',
        costAvailable,
        marginDollars,
        marginPercent,
      };
    });
  }, [activeProducts, costQueries]);

  const isLoading = productsLoading || costQueries.some((q) => q.status === 'pending');
  const isError = productsError;

  return { rows, isLoading, isError, refetch: refetchProducts };
}
