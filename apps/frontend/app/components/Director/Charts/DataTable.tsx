import { useState } from 'react';
import { Download, Filter, Search, ChevronUp, ChevronDown } from 'lucide-react';

interface DataTableColumn<T> {
  key: keyof T;
  label: string;
  sortable?: boolean;
  render?: (value: any, item: T) => React.ReactNode;
}

interface DataTableProps<T> {
  data: T[];
  columns: DataTableColumn<T>[];
  title: string;
  exportable?: boolean;
  searchable?: boolean;
  filterable?: boolean;
  itemsPerPage?: number;
  initialSort?: {
    key: keyof T;
    direction: 'asc' | 'desc';
  };
}

export function DataTable<T extends Record<string, any>>({
  data,
  columns,
  title,
  exportable = false,
  searchable = false,
  filterable = false,
  itemsPerPage = 15,
  initialSort,
}: DataTableProps<T>) {
  const [sortConfig, setSortConfig] = useState<{
    key: keyof T | null;
    direction: 'asc' | 'desc';
  }>({
    key: initialSort?.key ?? null,
    direction: initialSort?.direction ?? 'asc',
  });

  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);

  // Handle sorting
  const handleSort = (key: keyof T) => {
    let direction: 'asc' | 'desc' = 'asc';
    if (sortConfig.key === key && sortConfig.direction === 'asc') {
      direction = 'desc';
    }
    setSortConfig({ key, direction });
  };

  // Filter and sort data
  const filteredData = data.filter(
    item =>
      searchTerm === '' ||
      Object.values(item).some(value =>
        String(value).toLowerCase().includes(searchTerm.toLowerCase())
      )
  );

  const sortedData = [...filteredData].sort((a, b) => {
    if (!sortConfig.key) return 0;

    const aValue = a[sortConfig.key];
    const bValue = b[sortConfig.key];

    if (aValue < bValue) {
      return sortConfig.direction === 'asc' ? -1 : 1;
    }
    if (aValue > bValue) {
      return sortConfig.direction === 'asc' ? 1 : -1;
    }
    return 0;
  });

  // Pagination
  const totalPages = Math.ceil(sortedData.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const paginatedData = sortedData.slice(startIndex, startIndex + itemsPerPage);

  // Export function
  const handleExport = () => {
    const csv = [
      columns.map(col => col.label).join(','),
      ...sortedData.map(item =>
        columns
          .map(col => {
            const value = item[col.key];
            return typeof value === 'string' && value.includes(',')
              ? `"${value}"`
              : String(value);
          })
          .join(',')
      ),
    ].join('\n');

    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${title.toLowerCase().replace(/\s+/g, '_')}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="bg-white rounded-lg shadow-md">
      {/* Header */}
      <div className="p-6 border-b border-gray-200">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-800">{title}</h3>
          <div className="flex items-center gap-2">
            {filterable && (
              <button className="flex items-center gap-1 px-3 py-1.5 text-sm text-gray-600 hover:text-gray-800 border border-gray-300 rounded">
                <Filter size={14} />
                Filtros
              </button>
            )}
            {exportable && (
              <button
                onClick={handleExport}
                className="flex items-center gap-1 px-3 py-1.5 text-sm text-white bg-blue-600 hover:bg-blue-700 rounded"
              >
                <Download size={14} />
                Exportar
              </button>
            )}
          </div>
        </div>

        {searchable && (
          <div className="relative">
            <Search
              className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400"
              size={16}
            />
            <input
              type="text"
              placeholder="Buscar en la tabla..."
              value={searchTerm}
              onChange={e => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        )}
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full table-auto">
          <thead className="bg-gray-50">
            <tr>
              {columns.map(column => (
                <th
                  key={String(column.key)}
                  className={`px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider ${
                    column.sortable ? 'cursor-pointer hover:bg-gray-100' : ''
                  }`}
                  onClick={() => column.sortable && handleSort(column.key)}
                >
                  <div className="flex items-center gap-1">
                    {column.label}
                    {column.sortable && (
                      <div className="flex flex-col">
                        <ChevronUp
                          size={12}
                          className={`${
                            sortConfig.key === column.key &&
                            sortConfig.direction === 'asc'
                              ? 'text-blue-600'
                              : 'text-gray-400'
                          }`}
                        />
                        <ChevronDown
                          size={12}
                          className={`-mt-1 ${
                            sortConfig.key === column.key &&
                            sortConfig.direction === 'desc'
                              ? 'text-blue-600'
                              : 'text-gray-400'
                          }`}
                        />
                      </div>
                    )}
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {paginatedData.map((item, index) => (
              <tr key={index} className="hover:bg-gray-50">
                {columns.map(column => (
                  <td
                    key={String(column.key)}
                    className="px-3 py-2 text-sm text-gray-900 overflow-hidden"
                  >
                    {column.render
                      ? column.render(item[column.key], item)
                      : String(item[column.key])}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="px-6 py-3 border-t border-gray-200">
          <div className="flex items-center justify-between">
            <div className="text-sm text-gray-700">
              Mostrando {startIndex + 1} a{' '}
              {Math.min(startIndex + itemsPerPage, sortedData.length)} de{' '}
              {sortedData.length} resultados
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
                disabled={currentPage === 1}
                className="px-3 py-1 text-sm text-gray-600 hover:text-gray-800 disabled:text-gray-400 disabled:cursor-not-allowed"
              >
                Anterior
              </button>
              <div className="flex items-center gap-1">
                {Array.from({ length: totalPages }, (_, i) => i + 1)
                  .filter(
                    page =>
                      page === 1 ||
                      page === totalPages ||
                      Math.abs(page - currentPage) <= 2
                  )
                  .map((page, index, array) => (
                    <span key={page}>
                      {index > 0 && array[index - 1] !== page - 1 && (
                        <span className="text-gray-400">...</span>
                      )}
                      <button
                        onClick={() => setCurrentPage(page)}
                        className={`px-3 py-1 text-sm rounded ${
                          currentPage === page
                            ? 'bg-blue-600 text-white'
                            : 'text-gray-600 hover:text-gray-800'
                        }`}
                      >
                        {page}
                      </button>
                    </span>
                  ))}
              </div>
              <button
                onClick={() =>
                  setCurrentPage(Math.min(totalPages, currentPage + 1))
                }
                disabled={currentPage === totalPages}
                className="px-3 py-1 text-sm text-gray-600 hover:text-gray-800 disabled:text-gray-400 disabled:cursor-not-allowed"
              >
                Siguiente
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
