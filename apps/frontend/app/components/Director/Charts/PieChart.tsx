import { useState } from 'react';

interface PieChartData {
  estado: string;
  cantidad: number;
  porcentaje: number;
  color: string;
}

interface PieChartProps {
  data: PieChartData[];
  title: string;
  interactive?: boolean;
}

export function PieChart({ data, title, interactive = true }: PieChartProps) {
  const [hoveredSlice, setHoveredSlice] = useState<number | null>(null);

  const total = data.reduce((sum, item) => sum + item.cantidad, 0);

  // Calculate angles for pie slices
  let cumulativeAngle = 0;
  const slices = data.map((item, index) => {
    const angle = (item.cantidad / total) * 360;
    const startAngle = cumulativeAngle;
    const endAngle = cumulativeAngle + angle;
    cumulativeAngle += angle;

    // Calculate path for SVG arc
    const startAngleRad = (startAngle * Math.PI) / 180;
    const endAngleRad = (endAngle * Math.PI) / 180;
    const largeArcFlag = angle > 180 ? 1 : 0;

    const x1 = 50 + 40 * Math.cos(startAngleRad);
    const y1 = 50 + 40 * Math.sin(startAngleRad);
    const x2 = 50 + 40 * Math.cos(endAngleRad);
    const y2 = 50 + 40 * Math.sin(endAngleRad);

    const pathData = [
      `M 50 50`,
      `L ${x1} ${y1}`,
      `A 40 40 0 ${largeArcFlag} 1 ${x2} ${y2}`,
      'Z',
    ].join(' ');

    return {
      ...item,
      pathData,
      index,
    };
  });

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h3 className="text-lg font-semibold mb-4 text-gray-800">{title}</h3>

      <div className="flex items-center gap-6">
        {/* SVG Pie Chart */}
        <div className="relative">
          <svg
            width="200"
            height="200"
            viewBox="0 0 100 100"
            className="transform -rotate-90"
          >
            {slices.map(slice => (
              <path
                key={slice.index}
                d={slice.pathData}
                fill={slice.color}
                stroke="white"
                strokeWidth="0.5"
                className={`transition-all duration-300 ${
                  interactive ? 'cursor-pointer hover:opacity-80' : ''
                } ${
                  hoveredSlice === slice.index ? 'opacity-90 scale-105' : ''
                }`}
                onMouseEnter={() => interactive && setHoveredSlice(slice.index)}
                onMouseLeave={() => interactive && setHoveredSlice(null)}
              />
            ))}
          </svg>

          {/* Center text */}
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="text-center">
              <div className="text-2xl font-bold text-gray-800">{total}</div>
              <div className="text-xs text-gray-600">Total</div>
            </div>
          </div>
        </div>

        {/* Legend */}
        <div className="flex-1">
          <div className="space-y-2">
            {data.map((item, index) => (
              <div
                key={index}
                className={`flex items-center gap-3 p-2 rounded transition-colors ${
                  hoveredSlice === index ? 'bg-gray-50' : ''
                }`}
                onMouseEnter={() => interactive && setHoveredSlice(index)}
                onMouseLeave={() => interactive && setHoveredSlice(null)}
              >
                <div
                  className="w-4 h-4 rounded-full flex-shrink-0"
                  style={{ backgroundColor: item.color }}
                />
                <div className="flex-1">
                  <div className="text-sm font-medium text-gray-800">
                    {item.estado}
                  </div>
                  <div className="text-xs text-gray-600">
                    {item.cantidad} ({item.porcentaje}%)
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
