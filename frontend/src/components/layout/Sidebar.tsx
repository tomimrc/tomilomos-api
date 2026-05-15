import { NavLink } from 'react-router-dom';
import { Package, ChefHat, X, BarChart3, Boxes, ShoppingCart, Eye, TrendingUp } from 'lucide-react';

const navItems = [
  { to: '/app/dashboard', label: 'Dashboard', icon: BarChart3 },
  { to: '/app/raw-materials', label: 'Raw Materials', icon: Boxes },
  { to: '/app/products', label: 'Products', icon: Package },
  { to: '/app/sales', label: 'Sales', icon: ShoppingCart },
  { to: '/app/recipes', label: 'Recipes', icon: ChefHat },
  { to: '/app/profitability', label: 'Profitability', icon: TrendingUp },
  { to: '/app/stock', label: 'Stock Monitor', icon: Eye },
];

interface SidebarProps {
  onClose?: () => void;
}

export default function Sidebar({ onClose }: SidebarProps) {
  return (
    <aside className="flex h-full w-56 flex-col border-r border-gray-200 bg-white">
      {/* Logo / Brand */}
      <div className="flex h-14 items-center gap-2 border-b px-4">
        <ChefHat className="h-6 w-6 text-indigo-600" />
        <span className="text-lg font-bold text-gray-900">TomiLomos</span>
        {onClose && (
          <button
            onClick={onClose}
            className="ml-auto rounded-lg p-1 text-gray-400 hover:bg-gray-100 lg:hidden"
          >
            <X className="h-5 w-5" />
          </button>
        )}
      </div>

      {/* Navigation */}
      <nav className="flex-1 space-y-1 p-3">
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) =>
              `flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors ${
                isActive
                  ? 'bg-indigo-50 text-indigo-700'
                  : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
              }`
            }
          >
            <item.icon className="h-5 w-5" />
            {item.label}
          </NavLink>
        ))}
      </nav>

      {/* Footer */}
      <div className="border-t p-3">
        <p className="text-xs text-gray-400">TomiLomos v1.0</p>
      </div>
    </aside>
  );
}
