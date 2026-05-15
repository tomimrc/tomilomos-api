import { useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  createColumnHelper,
  flexRender,
  getCoreRowModel,
  getSortedRowModel,
  useReactTable,
  type SortingState,
} from '@tanstack/react-table';
import { AlertCircle } from 'lucide-react';
import type { ProfitabilityItem, FilterType } from '../types';
import { formatCurrency } from '@/lib/formatters';
import ProfitMarginBadge from './ProfitMarginBadge';
import Button from '@/components/ui/Button';

const columnHelper = createColumnHelper<ProfitabilityItem>();

interface ProfitabilityTableProps {
  items: ProfitabilityItem[];
  filter: FilterType;
  onFilterChange: (filter: FilterType) => void;
}

export default function ProfitabilityTable({
  items,
  filter,
  onFilterChange,
}: ProfitabilityTableProps) {
  const navigate = useNavigate();
  const [sorting, setSorting] = useState<SortingState>([
    { id: 'marginPercent', desc: true },
  ]);

  // Apply filter
  const filtered = useMemo(() => {
    if (filter === 'profitable')
      return items.filter(
        (i) => i.marginPercent !== null && i.marginPercent > 0
      );
    if (filter === 'unprofitable')
      return items.filter(
        (i) => i.marginPercent !== null && i.marginPercent < 0
      );
    return items;
  }, [items, filter]);

  const columns = useMemo(
    () => [
      columnHelper.accessor('product.name', {
        id: 'name',
        header: 'Product Name',
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
      }),
      columnHelper.accessor('cost', {
        id: 'costPrice',
        header: 'Cost Price',
        cell: (info) => {
          const cost = info.getValue();
          if (!cost || info.row.original.costUnavailable) {
            return (
              <span className="inline-flex items-center gap-1 text-gray-400">
                <AlertCircle className="h-3.5 w-3.5" />
                —
              </span>
            );
          }
          return formatCurrency(cost.total_cost);
        },
      }),
      columnHelper.accessor('margin', {
        id: 'grossMargin',
        header: 'Gross Margin',
        cell: (info) => {
          if (info.row.original.costUnavailable) {
            return <span className="text-gray-400">—</span>;
          }
          const m = info.getValue();
          return (
            <span className={m < 0 ? 'text-red-600' : 'text-gray-900'}>
              {formatCurrency(m)}
            </span>
          );
        },
      }),
      columnHelper.accessor('marginPercent', {
        id: 'marginPercent',
        header: 'Margin %',
        cell: (info) => (
          <ProfitMarginBadge
            marginPercent={info.getValue()}
            costUnavailable={info.row.original.costUnavailable}
          />
        ),
      }),
    ],
    [navigate]
  );

  const table = useReactTable({
    data: filtered,
    columns,
    state: { sorting },
    onSortingChange: setSorting,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
  });

  return (
    <div>
      {/* Filter controls */}
      <div className="mb-4 flex items-center gap-2">
        <span className="text-sm text-gray-500">Filter:</span>
        <div className="flex rounded-lg border border-gray-200 bg-white p-0.5">
          {(['all', 'profitable', 'unprofitable'] as FilterType[]).map((f) => (
            <button
              key={f}
              onClick={() => onFilterChange(f)}
              className={`rounded-md px-3 py-1.5 text-xs font-medium transition-colors ${
                filter === f
                  ? 'bg-indigo-600 text-white'
                  : 'text-gray-600 hover:bg-gray-50'
              }`}
            >
              {f === 'all' ? 'All' : f === 'profitable' ? 'Profitable' : 'Unprofitable'}
            </button>
          ))}
        </div>
      </div>

      {/* Table */}
      {filtered.length === 0 ? (
        <div className="rounded-xl border border-gray-200 bg-white py-12 text-center">
          <p className="text-sm text-gray-500">No products match this filter</p>
        </div>
      ) : (
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
      )}
    </div>
  );
}
