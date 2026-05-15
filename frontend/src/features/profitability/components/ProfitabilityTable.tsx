import { useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  createColumnHelper,
  flexRender,
  getCoreRowModel,
  getSortedRowModel,
  getFilteredRowModel,
  useReactTable,
  type SortingState,
} from '@tanstack/react-table';
import { TrendingUp, TrendingDown, Minus, Search, AlertTriangle } from 'lucide-react';
import type { ProfitabilityRow } from '../hooks/useProfitability';
import { formatCurrency } from '@/lib/formatters';

const columnHelper = createColumnHelper<ProfitabilityRow>();

type FilterType = 'all' | 'profitable' | 'unprofitable';

interface ProfitabilityTableProps {
  rows: ProfitabilityRow[];
  filter: FilterType;
  onFilterChange: (f: FilterType) => void;
}

export default function ProfitabilityTable({
  rows,
  filter,
  onFilterChange,
}: ProfitabilityTableProps) {
  const navigate = useNavigate();
  const [sorting, setSorting] = useState<SortingState>([
    { id: 'marginPercent', desc: true },
  ]);
  const [globalFilter, setGlobalFilter] = useState('');

  const filteredRows = useMemo(() => {
    if (filter === 'all') return rows;
    if (filter === 'profitable')
      return rows.filter((r) => r.marginPercent !== null && r.marginPercent > 0);
    return rows.filter((r) => r.marginPercent !== null && r.marginPercent < 0);
  }, [rows, filter]);

  const columns = useMemo(
    () => [
      columnHelper.accessor('product.name', {
        id: 'name',
        header: 'Product',
        cell: (info) => (
          <button
            onClick={() =>
              navigate(`/app/products/${info.row.original.product.id}`)
            }
            className="font-medium text-indigo-600 hover:text-indigo-800"
          >
            {info.getValue()}
          </button>
        ),
      }),
      columnHelper.accessor('product.sale_price', {
        id: 'salePrice',
        header: 'Sale Price',
        cell: (info) => formatCurrency(info.getValue()),
        sortingFn: (a, b) =>
          parseFloat(a.original.product.sale_price) -
          parseFloat(b.original.product.sale_price),
      }),
      columnHelper.accessor('cost', {
        id: 'costPrice',
        header: 'Cost Price',
        cell: (info) => {
          const cost = info.getValue();
          if (!cost) {
            return (
              <span className="inline-flex items-center gap-1 text-gray-400">
                <AlertTriangle className="h-3.5 w-3.5" />
                Unavailable
              </span>
            );
          }
          return formatCurrency(cost.total_cost);
        },
        sortingFn: (a, b) => {
          const ca = a.original.cost ? parseFloat(a.original.cost.total_cost) : -Infinity;
          const cb = b.original.cost ? parseFloat(b.original.cost.total_cost) : -Infinity;
          return ca - cb;
        },
      }),
      columnHelper.accessor('marginDollars', {
        id: 'marginDollars',
        header: 'Gross Margin',
        cell: (info) => {
          const val = info.getValue();
          if (val === null) return '\u2014';
          return (
            <span className={val >= 0 ? 'text-green-600' : 'text-red-600'}>
              {formatCurrency(val)}
            </span>
          );
        },
        sortingFn: (a, b) => {
          const ma = a.original.marginDollars ?? -Infinity;
          const mb = b.original.marginDollars ?? -Infinity;
          return ma - mb;
        },
      }),
      columnHelper.accessor('marginPercent', {
        id: 'marginPercent',
        header: 'Margin %',
        cell: (info) => {
          const val = info.getValue();
          if (val === null) return '\u2014';
          const color =
            val > 0 ? 'text-green-600' : val < 0 ? 'text-red-600' : 'text-gray-500';
          return (
            <span className={`font-semibold ${color}`}>
              {val.toFixed(2)}%
            </span>
          );
        },
      }),
      columnHelper.display({
        id: 'indicator',
        header: '',
        cell: (info) => {
          const val = info.row.original.marginPercent;
          if (val === null)
            return <Minus className="h-4 w-4 text-gray-300" />;
          if (val > 0)
            return <TrendingUp className="h-4 w-4 text-green-500" />;
          if (val < 0)
            return <TrendingDown className="h-4 w-4 text-red-500" />;
          return <Minus className="h-4 w-4 text-gray-300" />;
        },
      }),
    ],
    [navigate]
  );

  const table = useReactTable({
    data: filteredRows,
    columns,
    state: { sorting, globalFilter },
    onSortingChange: setSorting,
    onGlobalFilterChange: setGlobalFilter,
    globalFilterFn: (row, _, filterValue) => {
      const name = row.original.product.name;
      return name.toLowerCase().includes(filterValue.toLowerCase());
    },
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
  });

  const filters: { key: FilterType; label: string }[] = [
    { key: 'all', label: 'All' },
    { key: 'profitable', label: 'Profitable' },
    { key: 'unprofitable', label: 'Unprofitable' },
  ];

  return (
    <div className="space-y-3">
      {/* Filter tabs + Search */}
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex gap-1 rounded-lg bg-gray-100 p-1">
          {filters.map((f) => (
            <button
              key={f.key}
              onClick={() => onFilterChange(f.key)}
              className={`rounded-md px-3 py-1.5 text-xs font-medium transition-colors ${
                filter === f.key
                  ? 'bg-white text-gray-900 shadow-sm'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              {f.label}
            </button>
          ))}
        </div>
        <div className="relative">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
          <input
            type="text"
            value={globalFilter}
            onChange={(e) => setGlobalFilter(e.target.value)}
            placeholder="Search by name..."
            className="w-full rounded-lg border border-gray-300 py-2 pl-10 pr-4 text-sm placeholder-gray-400 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 sm:w-56"
          />
        </div>
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
                    {flexRender(header.column.columnDef.header, header.getContext())}
                  </th>
                ))}
              </tr>
            ))}
          </thead>
          <tbody>
            {table.getRowModel().rows.length === 0 ? (
              <tr>
                <td
                  colSpan={columns.length}
                  className="px-4 py-8 text-center text-sm text-gray-400"
                >
                  No products match this filter
                </td>
              </tr>
            ) : (
              table.getRowModel().rows.map((row) => (
                <tr
                  key={row.id}
                  className="border-b transition-colors hover:bg-gray-50"
                >
                  {row.getVisibleCells().map((cell) => (
                    <td key={cell.id} className="px-4 py-3 text-sm text-gray-700">
                      {flexRender(cell.column.columnDef.cell, cell.getContext())}
                    </td>
                  ))}
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
