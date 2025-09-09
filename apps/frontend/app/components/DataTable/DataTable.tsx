import {
  createColumnHelper,
  flexRender,
  getCoreRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  useReactTable,
  type SortingState,
  type ColumnFiltersState,
} from '@tanstack/react-table';
import { useMemo, useState } from 'react';
import { useTranslation } from 'react-i18next';
import {
  ChevronLeft,
  ChevronRight,
  ChevronsLeft,
  ChevronsRight,
  Search,
} from 'lucide-react';

export interface DataTableColumn {
  header: string;
  accessorKey?: string;
  id?: string;
  width?: string;
  cell?: ({ row }: { row: any }) => React.ReactNode;
}

export interface DataTableProps {
  data: any[];
  columns: DataTableColumn[];
  searchPlaceholder?: string;
  noDataMessage?: string;
  enablePagination?: boolean;
  enableSorting?: boolean;
  enableFiltering?: boolean;
  pageSize?: number;
}

export function DataTable({
  data,
  columns: columnsFromProps = [],
  searchPlaceholder,
  noDataMessage,
  enablePagination = true,
  enableSorting = true,
  enableFiltering = true,
  pageSize = 10,
}: DataTableProps) {
  const { t } = useTranslation('common');
  const [sorting, setSorting] = useState<SortingState>([]);
  const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([]);
  const [globalFilter, setGlobalFilter] = useState('');

  // Use translations as defaults if not provided
  const searchPlaceholderText = searchPlaceholder || t('dataTable.search');
  const noDataMessageText = noDataMessage || t('dataTable.noData');

  const columnHelper = createColumnHelper<any>();

  const columns = useMemo(
    () =>
      columnsFromProps.map(column => {
        const accessorKey = column.accessorKey || column.id || 'unknown';
        return columnHelper.accessor(accessorKey, {
          id: column.id || column.accessorKey || accessorKey,
          header: column.header,
          cell: info => {
            if (column.cell) {
              return column.cell({ row: info.row });
            }
            return info.getValue();
          },
          enableSorting: enableSorting,
        });
      }),
    [columnsFromProps, enableSorting]
  );

  const table = useReactTable({
    data,
    columns,
    state: {
      sorting,
      columnFilters,
      globalFilter,
    },
    enableSorting,
    onSortingChange: setSorting,
    onColumnFiltersChange: setColumnFilters,
    onGlobalFilterChange: setGlobalFilter,
    getCoreRowModel: getCoreRowModel(),
    getFilteredRowModel: enableFiltering ? getFilteredRowModel() : undefined,
    getPaginationRowModel: enablePagination
      ? getPaginationRowModel()
      : undefined,
    getSortedRowModel: enableSorting ? getSortedRowModel() : undefined,
    initialState: {
      pagination: {
        pageSize,
      },
    },
  });

  return (
    <div className="space-y-4">
      {/* Search */}
      {enableFiltering && (
        <div className="flex items-center space-x-2">
          <div className="relative flex-1 max-w-sm">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
            <input
              type="text"
              placeholder={searchPlaceholderText}
              value={globalFilter ?? ''}
              onChange={e => setGlobalFilter(e.target.value)}
              className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
        </div>
      )}

      {/* Table */}
      <div className="overflow-x-auto border border-gray-200 rounded-lg">
        <table className="w-full bg-white min-w-full">
          <thead className="border-b border-b-gray-300 bg-gray-50">
            {table.getHeaderGroups().map(headerGroup => (
              <tr key={headerGroup.id}>
                {headerGroup.headers.map((header, index) => (
                  <th
                    className={`p-3 text-gray-600 text-left font-semibold text-sm whitespace-nowrap ${
                      enableSorting && header.column.getCanSort()
                        ? 'cursor-pointer select-none'
                        : ''
                    }`}
                    key={header.id}
                    style={{ width: columnsFromProps[index]?.width || 'auto' }}
                    onClick={header.column.getToggleSortingHandler()}
                  >
                    <div className="flex items-center space-x-1">
                      {header.isPlaceholder
                        ? null
                        : flexRender(
                            header.column.columnDef.header,
                            header.getContext()
                          )}
                      {enableSorting && header.column.getCanSort() && (
                        <span className="text-gray-400">
                          {header.column.getIsSorted() === 'asc'
                            ? ' ↑'
                            : header.column.getIsSorted() === 'desc'
                              ? ' ↓'
                              : ' ↕'}
                        </span>
                      )}
                    </div>
                  </th>
                ))}
              </tr>
            ))}
          </thead>

          <tbody>
            {table.getRowModel().rows.map((row, rowIndex) => (
              <tr
                key={row.id}
                className={`hover:bg-gray-50 border-b border-gray-100 last:border-b-0 transition-colors ${
                  rowIndex % 2 === 0 ? 'bg-white' : 'bg-gray-25'
                }`}
              >
                {row.getVisibleCells().map(cell => (
                  <td className="p-3 text-left align-top text-sm" key={cell.id}>
                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                  </td>
                ))}
              </tr>
            ))}

            {table.getRowModel().rows.length === 0 && (
              <tr>
                <td
                  colSpan={columns.length}
                  className="p-8 text-center text-gray-500"
                >
                  <div className="flex flex-col items-center gap-2">
                    <div className="text-4xl">📋</div>
                    <div className="font-medium">{noDataMessageText}</div>
                  </div>
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      {enablePagination && (
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <p className="text-sm text-gray-700">
              {t('dataTable.showing')}{' '}
              <span className="font-medium">
                {table.getState().pagination.pageIndex *
                  table.getState().pagination.pageSize +
                  1}
              </span>{' '}
              a{' '}
              <span className="font-medium">
                {Math.min(
                  (table.getState().pagination.pageIndex + 1) *
                    table.getState().pagination.pageSize,
                  table.getFilteredRowModel().rows.length
                )}
              </span>{' '}
              {t('pagination.of')}{' '}
              <span className="font-medium">
                {table.getFilteredRowModel().rows.length}
              </span>{' '}
              {t('pagination.results')}
            </p>
          </div>

          <div className="flex items-center space-x-2">
            <button
              className="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              onClick={() => table.setPageIndex(0)}
              disabled={!table.getCanPreviousPage()}
            >
              <ChevronsLeft className="h-4 w-4" />
            </button>
            <button
              className="relative inline-flex items-center px-2 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              onClick={() => table.previousPage()}
              disabled={!table.getCanPreviousPage()}
            >
              <ChevronLeft className="h-4 w-4" />
            </button>

            <span className="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-700">
              {t('dataTable.page')} {table.getState().pagination.pageIndex + 1}{' '}
              {t('pagination.of')} {table.getPageCount()}
            </span>

            <button
              className="relative inline-flex items-center px-2 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              onClick={() => table.nextPage()}
              disabled={!table.getCanNextPage()}
            >
              <ChevronRight className="h-4 w-4" />
            </button>
            <button
              className="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              onClick={() => table.setPageIndex(table.getPageCount() - 1)}
              disabled={!table.getCanNextPage()}
            >
              <ChevronsRight className="h-4 w-4" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
