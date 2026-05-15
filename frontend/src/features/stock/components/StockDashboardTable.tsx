import {
  createColumnHelper,
  flexRender,
  getCoreRowModel,
  getSortedRowModel,
  getFilteredRowModel,
  useReactTable,
  type SortingState,
} from '@tanstack/react-table';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, AlertTriangle, AlertCircle } from 'lucide-react';
import type { RawMaterial } from '@/types/rawMaterial';
import { formatCurrency } from '@/lib/formatters';
import StockLevelBadge from '@/features/raw-materials/components/StockLevelBadge';

const columnHelper = createColumnHelper<RawMaterial>();

interface StockDashboardTableProps {
  materials: RawMaterial[];
  lowStockCount: number;
  outOfStockCount: number;
}

export default function StockDashboardTable({
  materials,
  lowStockCount,
  outOfStockCount,
}: StockDashboardTableProps) {
  const navigate = useNavigate();
  const [sorting, setSorting] = useState<SortingState>([
    { id: 'current_stock', desc: false },
  ]);
  const [globalFilter, setGlobalFilter] = useState('');

  const columns = [
    columnHelper.accessor('name', {
      header: 'Material',
      cell: (info) => (
        <button
          onClick={() =>
            navigate(`/app/raw-materials/${info.row.original.id}`)
          }
          className="font-medium text-indigo-600 hover:text-indigo-800"
        >
          {info.getValue()}
        </button>
      ),
    }),
    columnHelper.accessor('unit_of_measurement', {
      header: 'Unit',
      cell: (info) => (
        <span className="rounded bg-gray-100 px-1.5 py-0.5 text-xs font-medium text-gray-600">
          {info.getValue()}
        </span>
      ),
    }),
    columnHelper.accessor('current_stock', {
      header: 'Current Stock',
      cell: (info) => {
        const stock = parseFloat(info.getValue());
        return <StockLevelBadge stock={isNaN(stock) ? 0 : stock} />;
      },
      sortingFn: (a, b) => {
        const va = parseFloat(a.original.current_stock);
        const vb = parseFloat(b.original.current_stock);
        return va - vb;
      },
    }),
    columnHelper.accessor('supplier', {
      header: 'Supplier',
      cell: (info) => info.getValue() || '\u2014',
    }),
    columnHelper.accessor('cost_per_unit', {
      header: 'Cost per Unit',
      cell: (info) => formatCurrency(info.getValue()),
    }),
  ];

  const table = useReactTable({
    data: materials,
    columns,
    state: { sorting, globalFilter },
    onSortingChange: setSorting,
    onGlobalFilterChange: setGlobalFilter,
    globalFilterFn: (row, _, filterValue) => {
      const name = row.getValue('name') as string;
      return name.toLowerCase().includes(filterValue.toLowerCase());
    },
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
  });

  return (
    <div className="space-y-4">
      {/* Summary stats */}
      <div className="grid gap-3 sm:grid-cols-2">
        <div className="flex items-center gap-3 rounded-xl border border-amber-200 bg-amber-50 px-4 py-3">
          <AlertTriangle className="h-5 w-5 text-amber-600" />
          <div>
            <p className="text-sm text-amber-700">Low Stock</p>
            <p className="text-xl font-bold text-amber-900">
              {lowStockCount}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-3 rounded-xl border border-red-200 bg-red-50 px-4 py-3">
          <AlertCircle className="h-5 w-5 text-red-600" />
          <div>
            <p className="text-sm text-red-700">Out of Stock</p>
            <p className="text-xl font-bold text-red-900">
              {outOfStockCount}
            </p>
          </div>
        </div>
      </div>

      {/* Search */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
        <input
          type="text"
          value={globalFilter}
          onChange={(e) => setGlobalFilter(e.target.value)}
          placeholder="Search by name..."
          className="w-full rounded-lg border border-gray-300 py-2 pl-10 pr-4 text-sm placeholder-gray-400 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 sm:max-w-xs"
        />
      </div>

      {/* Table */}
      <div className="overflow-hidden overflow-x-auto rounded-xl border border-gray-200 bg-white">
        <table className="w-full">
          <thead className="border-b bg-gray-50">
            {table.getHeaderGroups().map((headerGroup) => (
              <tr key={headerGroup.id}>
                {headerGroup.headers.map((header) => (
                  <th
                    key={header.id}
                    onClick={header.column.getToggleSortingHandler()}
                    className="cursor-pointer px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-gray-500"
                  >
                    {flexRender(
                      header.column.columnDef.header,
                      header.getContext()
                    )}
                  </th>
                ))}
              </tr>
            ))}
          </thead>
          <tbody>
            {table.getRowModel().rows.map((row) => (
              <tr
                key={row.id}
                className="border-b transition-colors hover:bg-gray-50"
              >
                {row.getVisibleCells().map((cell) => (
                  <td
                    key={cell.id}
                    className="px-4 py-3 text-sm text-gray-700"
                  >
                    {flexRender(
                      cell.column.columnDef.cell,
                      cell.getContext()
                    )}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
