import { createBrowserRouter, RouterProvider, Navigate } from 'react-router-dom';
import AppLayout from '@/components/layout/AppLayout';
import ProtectedRoute from '@/components/layout/ProtectedRoute';
import DashboardPage from '@/features/dashboard/pages/DashboardPage';
import RawMaterialsPage from '@/features/raw-materials/pages/RawMaterialsPage';
import RawMaterialCreatePage from '@/features/raw-materials/pages/RawMaterialCreatePage';
import RawMaterialEditPage from '@/features/raw-materials/pages/RawMaterialEditPage';
import RawMaterialDetailPage from '@/features/raw-materials/pages/RawMaterialDetailPage';
import ProductsPage from '@/features/products/pages/ProductsPage';
import ProductCreatePage from '@/features/products/pages/ProductCreatePage';
import ProductEditPage from '@/features/products/pages/ProductEditPage';
import ProductDetailPage from '@/features/products/pages/ProductDetailPage';
import RecipesPage from '@/features/recipes/pages/RecipesPage';
import RecipeCreatePage from '@/features/recipes/pages/RecipeCreatePage';
import RecipeEditPage from '@/features/recipes/pages/RecipeEditPage';
import RecipeDetailPage from '@/features/recipes/pages/RecipeDetailPage';
import SalesPage from '@/features/sales/pages/SalesPage';
import SalesHistoryPage from '@/features/sales/pages/SalesHistoryPage';
import StockDashboardPage from '@/features/stock/pages/StockDashboardPage';
import ProfitabilityPage from '@/features/profitability/pages/ProfitabilityPage';
import LoginPage from '@/features/auth/pages/LoginPage';

const router = createBrowserRouter([
  {
    path: '/login',
    element: <LoginPage />,
  },
  {
    path: '/app',
    element: <ProtectedRoute />,
    children: [
      {
        element: <AppLayout />,
        children: [
          { index: true, element: <Navigate to="/app/dashboard" replace /> },
          {
            path: 'dashboard',
            element: <DashboardPage />,
          },
          {
            path: 'raw-materials',
            children: [
              { index: true, element: <RawMaterialsPage /> },
              { path: 'new', element: <RawMaterialCreatePage /> },
              { path: ':id', element: <RawMaterialDetailPage /> },
              { path: ':id/edit', element: <RawMaterialEditPage /> },
            ],
          },
          {
            path: 'products',
            children: [
              { index: true, element: <ProductsPage /> },
              { path: 'new', element: <ProductCreatePage /> },
              { path: ':id', element: <ProductDetailPage /> },
              { path: ':id/edit', element: <ProductEditPage /> },
            ],
          },
          {
            path: 'recipes',
            children: [
              { index: true, element: <RecipesPage /> },
              { path: 'new', element: <RecipeCreatePage /> },
              { path: ':id', element: <RecipeDetailPage /> },
              { path: ':id/edit', element: <RecipeEditPage /> },
            ],
          },
          {
            path: 'sales',
            children: [
              { index: true, element: <SalesPage /> },
              { path: 'history', element: <SalesHistoryPage /> },
            ],
          },
          {
            path: 'stock',
            element: <StockDashboardPage />,
          },
          {
            path: 'profitability',
            element: <ProfitabilityPage />,
          },
        ],
      },
    ],
  },
  {
    path: '*',
    element: <Navigate to="/app" replace />,
  },
]);

export default function App() {
  return <RouterProvider router={router} />;
}
