import {
  createColumnHelper,
  flexRender,
  getCoreRowModel,
  getSortedRowModel,
  useReactTable,
  type SortingState,
} from '@tanstack/react-table';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Pencil, Trash2 } from 'lucide-react';
import type { Product } from '@/types/product';
import { formatCurrency } from '@/lib/formatters';
import Badge from '@/components/ui/Badge';
import Button from '@/components/ui/Button';

const columnHelper = createColumnHelper<Product>();

interface ProductTableProps {
  products: Product[];
  onDelete: (product: Product) => void;
}

export default function ProductTable({
  products,
  onDelete,
}: ProductTableProps) {
  const navigate = useNavigate();
  const [sorting, setSorting] = useState<SortingState>([
    { id: 'name', desc: false },
  ]);

  const columns = [
    columnHelper.accessor('name', {
      header: 'Name',
      cell: (info) => (
        <button
          onClick={() => navigate(`/app/products/${info.row.original.id}`)}
          className="font-medium text-indigo-600 hover:text-indigo-800"
        >
          {info.getValue()}
        </button>
      ),
    }),
    columnHelper.accessor('sale_price', {
      header: 'Sale Price',
      cell: (info) => formatCurrency(info.getValue()),
    }),
    columnHelper.accessor('cost_price', {
      header: 'Cost Price',
      cell: (info) => formatCurrency(info.getValue()),
    }),
    columnHelper.accessor('is_active', {
      header: 'Status',
      cell: (info) => (
        <Badge variant={info.getValue() ? 'active' : 'inactive'} />
      ),
    }),
    columnHelper.display({
      id: 'actions',
      header: 'Actions',
      cell: (info) => (
        <div className="flex items-center gap-1">
          <Button
            variant="ghost"
            onClick={() =>
              navigate(`/app/products/${info.row.original.id}/edit`)
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
    data: products,
    columns,
    state: { sorting },
    onSortingChange: setSorting,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
  });

  return (
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
                <td key={cell.id} className="px-4 py-3 text-sm text-gray-700">
                  {flexRender(cell.column.columnDef.cell, cell.getContext())}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
