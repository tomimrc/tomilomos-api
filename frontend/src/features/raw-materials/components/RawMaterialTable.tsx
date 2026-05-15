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
import { motion, AnimatePresence } from 'framer-motion';
import { Pencil, Trash2, Search } from 'lucide-react';
import type { RawMaterial } from '@/types/rawMaterial';
import { formatCurrency } from '@/lib/formatters';
import StockLevelBadge from './StockLevelBadge';
import Button from '@/components/ui/Button';

const columnHelper = createColumnHelper<RawMaterial>();

interface RawMaterialTableProps {
  materials: RawMaterial[];
  onDelete: (material: RawMaterial) => void;
}

export default function RawMaterialTable({
  materials,
  onDelete,
}: RawMaterialTableProps) {
  const navigate = useNavigate();
  const [sorting, setSorting] = useState<SortingState>([
    { id: 'name', desc: false },
  ]);
  const [globalFilter, setGlobalFilter] = useState('');

  const columns = [
    columnHelper.accessor('name', {
      header: 'Name',
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
    columnHelper.accessor('cost_per_unit', {
      header: 'Cost per Unit',
      cell: (info) => formatCurrency(info.getValue()),
      sortingFn: (a, b) => {
        const va = parseFloat(a.original.cost_per_unit);
        const vb = parseFloat(b.original.cost_per_unit);
        return va - vb;
      },
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
    columnHelper.display({
      id: 'actions',
      header: 'Actions',
      cell: (info) => (
        <div className="flex items-center gap-1">
          <Button
            variant="ghost"
            onClick={() =>
              navigate(`/app/raw-materials/${info.row.original.id}/edit`)
            }
            className="h-8 w-8 p-0"
            title="Edit"
          >
            <Pencil className="h-4 w-4" />
          </Button>
          <Button
            variant="ghost"
            onClick={() => onDelete(info.row.original)}
            className="h-8 w-8 p-0 text-red-500 hover:text-red-700"
            title="Delete"
          >
            <Trash2 className="h-4 w-4" />
          </Button>
        </div>
      ),
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
    <div className="space-y-3">
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
            <AnimatePresence>
              {table.getRowModel().rows.map((row) => (
                <motion.tr
                  key={row.id}
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }}
                  transition={{ duration: 0.2 }}
                  className="border-b hover:bg-gray-50"
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
                </motion.tr>
              ))}
            </AnimatePresence>
          </tbody>
        </table>
      </div>
    </div>
  );
}
