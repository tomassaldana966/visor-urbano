import * as RadioGroupPrimitive from '@radix-ui/react-radio-group';
import { CircleIcon } from 'lucide-react';
import { useId, type ComponentProps, type ReactNode } from 'react';

import { cn } from '@/lib/utils';
import { Label } from '../Label';

export function RadioGroup({
  className,
  label,
  options,
  ...props
}: ComponentProps<typeof RadioGroupPrimitive.Root> & {
  label?: string;
  options: Array<Parameters<typeof RadioGroupItem>[0]>;
}) {
  const id = useId();

  return (
    <RadioGroupPrimitive.Root
      data-slot="radio-group"
      className={cn('grid gap-3', className)}
      id={id}
      {...props}
    >
      {label ? <Label htmlFor={id}>{label}</Label> : null}

      <div className="grid gap-3 px-4">
        {options.map(option => (
          <RadioGroupItem
            key={option.value}
            data-slot="radio-group-item"
            {...option}
          />
        ))}
      </div>
    </RadioGroupPrimitive.Root>
  );
}

function RadioGroupItem({
  className,
  label,
  description,
  ...props
}: ComponentProps<typeof RadioGroupPrimitive.Item> & {
  label: string;
  description?: string | ReactNode;
}) {
  return (
    <label className="flex gap-2 items-center">
      <RadioGroupPrimitive.Item
        data-slot="radio-group-item"
        className={cn(
          'border-input text-primary focus-visible:border-ring focus-visible:ring-ring/50 aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 aria-invalid:border-destructive dark:bg-input/30 aspect-square size-4 shrink-0 rounded-full border shadow-xs transition-[color,box-shadow] outline-none focus-visible:ring-[3px] disabled:cursor-not-allowed disabled:opacity-50',
          className
        )}
        {...props}
      >
        <RadioGroupPrimitive.Indicator
          data-slot="radio-group-indicator"
          className="relative flex items-center justify-center"
        >
          <CircleIcon className="fill-primary absolute top-1/2 left-1/2 size-2 -translate-x-1/2 -translate-y-1/2" />
        </RadioGroupPrimitive.Indicator>
      </RadioGroupPrimitive.Item>

      <div
        className={cn('flex flex-col gap-1', {
          'opacity-50': props.disabled,
        })}
      >
        {label ? <span>{label}</span> : null}

        {description ? (
          typeof description === 'string' ? (
            <p className="text-xs text-muted-foreground">{description}</p>
          ) : (
            description
          )
        ) : null}
      </div>
    </label>
  );
}
