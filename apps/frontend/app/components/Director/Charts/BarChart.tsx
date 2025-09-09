interface BarChartData {
  mes: string;
  tramites: number;
  eficiencia: number;
}

interface BarChartProps {
  data: BarChartData[];
  title: string;
  height?: number;
}

export function BarChart({ data, title, height = 300 }: BarChartProps) {
  const maxTramites = Math.max(...data.map(d => d.tramites));
  const maxEficiencia = Math.max(...data.map(d => d.eficiencia));

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h3 className="text-lg font-semibold mb-4 text-gray-800">{title}</h3>

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
              x1="60"
              y1={250 - (y * 190) / 100}
              x2="740"
              y2={250 - (y * 190) / 100}
              stroke="#f3f4f6"
              strokeWidth="1"
            />
          ))}

          {/* Y-axis */}
          <line
            x1="60"
            y1="60"
            x2="60"
            y2="250"
            stroke="#9ca3af"
            strokeWidth="2"
          />

          {/* X-axis */}
          <line
            x1="60"
            y1="250"
            x2="740"
            y2="250"
            stroke="#9ca3af"
            strokeWidth="2"
          />

          {/* Bars */}
          {data.map((item, index) => {
            const barWidth = 80;
            const x = 80 + index * 100;
            const barHeight = (item.tramites / maxTramites) * 190;
            const y = 250 - barHeight;

            return (
              <g key={index}>
                {/* Bar */}
                <rect
                  x={x}
                  y={y}
                  width={barWidth}
                  height={barHeight}
                  fill="#3b82f6"
                  className="hover:fill-blue-700 transition-colors cursor-pointer"
                />

                {/* Value label */}
                <text
                  x={x + barWidth / 2}
                  y={y - 5}
                  textAnchor="middle"
                  className="text-xs fill-gray-700 font-medium"
                >
                  {item.tramites}
                </text>

                {/* Month label */}
                <text
                  x={x + barWidth / 2}
                  y={270}
                  textAnchor="middle"
                  className="text-xs fill-gray-600"
                >
                  {item.mes}
                </text>

                {/* Efficiency indicator */}
                <circle
                  cx={x + barWidth / 2}
                  cy={250 - (item.eficiencia / maxEficiencia) * 190}
                  r="4"
                  fill="#10b981"
                  className="hover:r-6 transition-all"
                />
              </g>
            );
          })}

          {/* Y-axis labels */}
          {[0, 25, 50, 75, 100].map(value => (
            <text
              key={value}
              x="50"
              y={255 - (value * 190) / 100}
              textAnchor="end"
              className="text-xs fill-gray-600"
            >
              {Math.round((value * maxTramites) / 100)}
            </text>
          ))}
        </svg>

        {/* Legend */}
        <div className="absolute top-4 right-4 bg-white p-2 rounded shadow-sm border">
          <div className="flex items-center gap-2 mb-1">
            <div className="w-3 h-3 bg-blue-500 rounded"></div>
            <span className="text-xs text-gray-600">Trámites</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-green-500 rounded-full"></div>
            <span className="text-xs text-gray-600">Eficiencia</span>
          </div>
        </div>
      </div>
    </div>
  );
}
