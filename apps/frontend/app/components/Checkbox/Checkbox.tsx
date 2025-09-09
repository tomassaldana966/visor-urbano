import * as CheckboxPrimitive from '@radix-ui/react-checkbox';
import { CheckIcon } from 'lucide-react';

import { cn } from '@/lib/utils';
import type { ReactNode } from 'react';
import { useTranslation } from 'react-i18next';

function Checkbox({
  className,
  label,
  error,
  ...props
}: React.ComponentProps<typeof CheckboxPrimitive.Root> & {
  label: string | ReactNode;
  error?: string;
}) {
  const { t: tErrors } = useTranslation('errors');

  return (
    <label className="flex flex-col gap-2">
      <div className="flex gap-2 items-center">
        <CheckboxPrimitive.Root
          data-slot="checkbox"
          className={cn(
            'peer border-input dark:bg-input/30 data-[state=checked]:bg-primary data-[state=checked]:text-primary-foreground dark:data-[state=checked]:bg-primary data-[state=checked]:border-primary focus-visible:border-ring focus-visible:ring-ring/50 aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 aria-invalid:border-destructive size-4 shrink-0 rounded-[4px] border shadow-xs transition-shadow outline-none focus-visible:ring-[3px] disabled:cursor-not-allowed disabled:opacity-50',
            className
          )}
          {...props}
        >
          <CheckboxPrimitive.Indicator
            data-slot="checkbox-indicator"
            className="flex items-center justify-center text-current transition-none"
          >
            <CheckIcon className="size-3.5" />
          </CheckboxPrimitive.Indicator>
        </CheckboxPrimitive.Root>

        <span>{label}</span>
      </div>

      {error ? (
        <div className="text-sm text-red-500">{tErrors(error)}</div>
      ) : null}
    </label>
  );
}

export { Checkbox };
