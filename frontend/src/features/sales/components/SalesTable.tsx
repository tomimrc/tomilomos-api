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
import { Search } from 'lucide-react';
import type { Sale } from '@/types/sale';
import { formatCurrency } from '@/lib/formatters';

const columnHelper = createColumnHelper<Sale>();

interface SalesTableProps {
  sales: Sale[];
}

export default function SalesTable({ sales }: SalesTableProps) {
  const [sorting, setSorting] = useState<SortingState>([
    { id: 'created_at', desc: true },
  ]);
  const [globalFilter, setGlobalFilter] = useState('');

  const columns = [
    columnHelper.accessor('created_at', {
      header: 'Date',
      cell: (info) =>
        new Date(info.getValue()).toLocaleDateString('en-US', {
          year: 'numeric',
          month: 'short',
          day: 'numeric',
          hour: '2-digit',
          minute: '2-digit',
        }),
    }),
    columnHelper.accessor('product_name', {
      header: 'Product',
      cell: (info) => (
        <span className="font-medium text-gray-900">{info.getValue()}</span>
      ),
    }),
    columnHelper.accessor('quantity', {
      header: 'Qty',
      cell: (info) => info.getValue(),
    }),
    columnHelper.accessor('unit_price', {
      header: 'Unit Price',
      cell: (info) => formatCurrency(info.getValue()),
    }),
    columnHelper.accessor('total_price', {
      header: 'Total',
      cell: (info) => (
        <span className="font-semibold text-gray-900">
          {formatCurrency(info.getValue())}
        </span>
      ),
    }),
    columnHelper.accessor('total_cost', {
      header: 'Cost',
      cell: (info) => {
        const val = info.getValue();
        return val ? formatCurrency(val) : '\u2014';
      },
    }),
    columnHelper.accessor('margin', {
      header: 'Margin',
      cell: (info) => {
        const val = info.getValue();
        if (val === null || val === undefined) return '\u2014';
        const num = parseFloat(val);
        return (
          <span
            className={num >= 0 ? 'text-green-600' : 'text-red-600'}
          >
            {formatCurrency(val)}
          </span>
        );
      },
    }),
  ];

  const table = useReactTable({
    data: sales,
    columns,
    state: { sorting, globalFilter },
    onSortingChange: setSorting,
    onGlobalFilterChange: setGlobalFilter,
    globalFilterFn: (row, _, filterValue) => {
      const name = row.getValue('product_name') as string;
      return name.toLowerCase().includes(filterValue.toLowerCase());
    },
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
  });

  return (
    <div className="space-y-3">
      {/* Search */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
        <input
          type="text"
          value={globalFilter}
          onChange={(e) => setGlobalFilter(e.target.value)}
          placeholder="Search by product name..."
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
