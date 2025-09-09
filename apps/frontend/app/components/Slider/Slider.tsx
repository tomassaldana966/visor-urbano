import * as React from 'react';
import * as SliderPrimitive from '@radix-ui/react-slider';
import { useId, type ReactNode } from 'react';
import { useTranslation } from 'react-i18next';

import { cn } from '@/lib/utils';
import { Label } from '../Label';

function Slider({
  className,
  defaultValue,
  value,
  min = 0,
  max = 100,
  label,
  error,
  ...props
}: React.ComponentProps<typeof SliderPrimitive.Root> & {
  label?: string | ReactNode;
  error?: string | null;
}) {
  const { t: tErrors } = useTranslation('errors');
  const id = useId();

  const _values = React.useMemo(
    () =>
      Array.isArray(value)
        ? value
        : Array.isArray(defaultValue)
          ? defaultValue
          : Array.isArray(min) && Array.isArray(max)
            ? [min, max]
            : [],
    [value, defaultValue, min, max]
  );

  return (
    <div>
      <div className="flex flex-col gap-2">
        {label ? (
          <Label htmlFor={id} className="flex">
            {label}
          </Label>
        ) : null}

        <div className="bg-white border-input flex min-h-[2.9rem] w-full min-w-0 rounded-md border px-3 py-3 shadow-xs items-center">
          <SliderPrimitive.Root
            data-slot="slider"
            defaultValue={defaultValue}
            value={value}
            min={min}
            max={max}
            id={id}
            className={cn(
              'relative flex w-full touch-none items-center select-none data-[disabled]:opacity-50 data-[orientation=vertical]:h-full data-[orientation=vertical]:min-h-44 data-[orientation=vertical]:w-auto data-[orientation=vertical]:flex-col',
              className
            )}
            {...props}
          >
            <SliderPrimitive.Track
              data-slot="slider-track"
              className={cn(
                'bg-muted relative grow overflow-hidden rounded-full data-[orientation=horizontal]:h-1.5 data-[orientation=horizontal]:w-full data-[orientation=vertical]:h-full data-[orientation=vertical]:w-1.5'
              )}
            >
              <SliderPrimitive.Range
                data-slot="slider-range"
                className={cn(
                  'bg-primary absolute data-[orientation=horizontal]:h-full data-[orientation=vertical]:w-full'
                )}
              />
            </SliderPrimitive.Track>
            {Array.from({ length: _values.length }, (_, index) => (
              <SliderPrimitive.Thumb
                data-slot="slider-thumb"
                key={index}
                className="border-primary bg-background ring-ring/50 block size-4 shrink-0 rounded-full border shadow-sm transition-[color,box-shadow] hover:ring-4 focus-visible:ring-4 focus-visible:outline-hidden disabled:pointer-events-none disabled:opacity-50"
              />
            ))}
          </SliderPrimitive.Root>
        </div>

        {error ? (
          <div className="text-sm text-red-500">{tErrors(error)}</div>
        ) : null}
      </div>
    </div>
  );
}

export { Slider };
