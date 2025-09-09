import {
  createColumnHelper,
  flexRender,
  getCoreRowModel,
  useReactTable,
} from '@tanstack/react-table';
import { useMemo } from 'react';

export function Table({
  data,
  columns: columnsFromProps = [],
  noDataMessage = 'No data available',
}: {
  data: Record<string, string>[];
  columns: {
    id: string;
    header: string;
    width?: string; // Add width support
    cell?: ({ row }: { row: Record<string, string> }) => React.ReactNode;
  }[];
  noDataMessage?: string;
}) {
  const columnHelper = createColumnHelper<Record<string, string>>();

  const columns = useMemo(
    () =>
      columnsFromProps.map(column =>
        columnHelper.accessor(column.id, {
          header: column.header,
          cell: info => {
            if (column.cell) {
              return column.cell({ row: info.row.original });
            }
            return info.getValue();
          },
        })
      ),
    [columnsFromProps]
  );

  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });
  return (
    <table className="w-full bg-white min-w-full">
      <thead className="border-b border-b-gray-300 bg-gray-50">
        {table.getHeaderGroups().map(headerGroup => (
          <tr key={headerGroup.id}>
            {headerGroup.headers.map((header, index) => (
              <th
                className="p-3 text-gray-600 text-left font-semibold text-sm whitespace-nowrap"
                key={header.id}
                style={{ width: columnsFromProps[index]?.width || 'auto' }}
              >
                {header.isPlaceholder
                  ? null
                  : flexRender(
                      header.column.columnDef.header,
                      header.getContext()
                    )}
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
                <div className="font-medium">{noDataMessage}</div>
              </div>
            </td>
          </tr>
        )}
      </tbody>

      <tfoot>
        {table.getFooterGroups().map(footerGroup => (
          <tr key={footerGroup.id}>
            {footerGroup.headers.map(header => (
              <th className="p-3" key={header.id}>
                {header.isPlaceholder
                  ? null
                  : flexRender(
                      header.column.columnDef.footer,
                      header.getContext()
                    )}
              </th>
            ))}
          </tr>
        ))}
      </tfoot>
    </table>
  );
}
