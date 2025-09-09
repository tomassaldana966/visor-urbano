import { TrendingUp, TrendingDown, Minus } from 'lucide-react';

interface MetricsCardProps {
  title: string;
  value: number | string;
  trend?: 'up' | 'down' | 'stable';
  trendValue?: string;
  color?: 'primary' | 'success' | 'warning' | 'danger';
  onClick?: () => void;
  icon?: React.ReactNode;
}

export function MetricsCard({
  title,
  value,
  trend,
  trendValue,
  color = 'primary',
  onClick,
  icon,
}: MetricsCardProps) {
  const cardColors = {
    primary: 'border-blue-200 bg-blue-50',
    success: 'border-green-200 bg-green-50',
    warning: 'border-yellow-200 bg-yellow-50',
    danger: 'border-red-200 bg-red-50',
  };

  const iconColors = {
    primary: 'text-blue-600 bg-blue-100',
    success: 'text-green-600 bg-green-100',
    warning: 'text-yellow-600 bg-yellow-100',
    danger: 'text-red-600 bg-red-100',
  };

  const trendColors = {
    up: 'text-green-600',
    down: 'text-red-600',
    stable: 'text-gray-600',
  };

  const getTrendIcon = () => {
    switch (trend) {
      case 'up':
        return <TrendingUp className="w-3 h-3" />;
      case 'down':
        return <TrendingDown className="w-3 h-3" />;
      case 'stable':
        return <Minus className="w-3 h-3" />;
      default:
        return null;
    }
  };

  return (
    <div
      className={`
        bg-white border ${cardColors[color]} p-6 rounded-lg shadow-sm
        ${onClick ? 'cursor-pointer hover:shadow-md transition-shadow' : ''}
      `}
      onClick={onClick}
    >
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <p className="text-sm font-medium text-gray-600 mb-1">{title}</p>
          <p className="text-2xl font-semibold text-gray-900">{value}</p>
          {trend && trendValue && (
            <div
              className={`flex items-center mt-2 text-sm ${trendColors[trend]}`}
            >
              {getTrendIcon()}
              <span className="ml-1">{trendValue}</span>
            </div>
          )}
        </div>
        {icon && (
          <div
            className={`w-12 h-12 rounded-lg flex items-center justify-center ${iconColors[color]}`}
          >
            {icon}
          </div>
        )}
      </div>
    </div>
  );
}
