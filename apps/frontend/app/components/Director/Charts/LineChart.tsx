interface LineChartData {
  mes: string;
  tramites: number;
  eficiencia: number;
}

interface LineChartProps {
  data: LineChartData[];
  title: string;
  height?: number;
  showZoom?: boolean;
}

export function LineChart({
  data,
  title,
  height = 300,
  showZoom = true,
}: LineChartProps) {
  const maxTramites = Math.max(...data.map(d => d.tramites));
  const maxEficiencia = 100; // Efficiency is always 0-100%

  // Generate path for tramites line
  const tramitesPath = data
    .map((item, index) => {
      const x = 80 + index * (660 / (data.length - 1));
      const y = 250 - (item.tramites / maxTramites) * 190;
      return `${index === 0 ? 'M' : 'L'} ${x} ${y}`;
    })
    .join(' ');

  // Generate path for efficiency line
  const eficienciaPath = data
    .map((item, index) => {
      const x = 80 + index * (660 / (data.length - 1));
      const y = 250 - (item.eficiencia / maxEficiencia) * 190;
      return `${index === 0 ? 'M' : 'L'} ${x} ${y}`;
    })
    .join(' ');

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-800">{title}</h3>
        {showZoom && (
          <div className="flex items-center gap-2">
            <button className="text-xs text-blue-600 hover:text-blue-800">
              Últimos 6 meses
            </button>
            <button className="text-xs text-gray-500 hover:text-gray-700">
              Este año
            </button>
            <button className="text-xs text-gray-500 hover:text-gray-700">
              Todo el tiempo
            </button>
          </div>
        )}
      </div>

      <div className="relative" style={{ height }}>
        <svg
          width="100%"
          height="100%"
          viewBox="0 0 800 300"
          className="overflow-visible"
        >
          {/* Grid lines */}
          {[0, 25, 50, 75, 100].map(y => (
            <line
              key={y}
              x1="80"
              y1={250 - (y * 190) / 100}
              x2="740"
              y2={250 - (y * 190) / 100}
              stroke="#f3f4f6"
              strokeWidth="1"
            />
          ))}

          {/* Y-axis */}
          <line
            x1="80"
            y1="60"
            x2="80"
            y2="250"
            stroke="#9ca3af"
            strokeWidth="2"
          />

          {/* X-axis */}
          <line
            x1="80"
            y1="250"
            x2="740"
            y2="250"
            stroke="#9ca3af"
            strokeWidth="2"
          />

          {/* Tramites line */}
          <path
            d={tramitesPath}
            fill="none"
            stroke="#3b82f6"
            strokeWidth="3"
            className="drop-shadow-sm"
          />

          {/* Efficiency line */}
          <path
            d={eficienciaPath}
            fill="none"
            stroke="#10b981"
            strokeWidth="3"
            strokeDasharray="5,5"
            className="drop-shadow-sm"
          />

          {/* Data points */}
          {data.map((item, index) => {
            const x = 80 + index * (660 / (data.length - 1));
            const yTramites = 250 - (item.tramites / maxTramites) * 190;
            const yEficiencia = 250 - (item.eficiencia / maxEficiencia) * 190;

            return (
              <g key={index}>
                {/* Tramites point */}
                <circle
                  cx={x}
                  cy={yTramites}
                  r="6"
                  fill="#3b82f6"
                  stroke="white"
                  strokeWidth="2"
                  className="hover:r-8 transition-all cursor-pointer"
                />

                {/* Efficiency point */}
                <circle
                  cx={x}
                  cy={yEficiencia}
                  r="6"
                  fill="#10b981"
                  stroke="white"
                  strokeWidth="2"
                  className="hover:r-8 transition-all cursor-pointer"
                />

                {/* Month label */}
                <text
                  x={x}
                  y={270}
                  textAnchor="middle"
                  className="text-xs fill-gray-600"
                >
                  {item.mes}
                </text>
              </g>
            );
          })}

          {/* Y-axis labels - Tramites */}
          {[0, 25, 50, 75, 100].map(value => (
            <text
              key={value}
              x="70"
              y={255 - (value * 190) / 100}
              textAnchor="end"
              className="text-xs fill-blue-600"
            >
              {Math.round((value * maxTramites) / 100)}
            </text>
          ))}

          {/* Secondary Y-axis labels - Efficiency */}
          {[0, 25, 50, 75, 100].map(value => (
            <text
              key={value}
              x="750"
              y={255 - (value * 190) / 100}
              textAnchor="start"
              className="text-xs fill-green-600"
            >
              {value}%
            </text>
          ))}
        </svg>

        {/* Legend */}
        <div className="absolute top-4 right-4 bg-white p-3 rounded shadow-sm border">
          <div className="flex items-center gap-2 mb-2">
            <div className="w-4 h-0.5 bg-blue-500"></div>
            <span className="text-xs text-gray-600">Trámites Procesados</span>
          </div>
          <div className="flex items-center gap-2">
            <div
              className="w-4 h-0.5 bg-green-500 border-dashed border-green-500"
              style={{ borderTopWidth: '1px' }}
            ></div>
            <span className="text-xs text-gray-600">Eficiencia (%)</span>
          </div>
        </div>
      </div>
    </div>
  );
}
