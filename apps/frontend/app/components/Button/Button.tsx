import type { ComponentProps } from 'react';
import { Slot } from '@radix-ui/react-slot';
import { cva, type VariantProps } from 'class-variance-authority';

import { cn } from '@/lib/utils';

const buttonVariants = cva(
  'inline-flex items-center justify-center rounded-lg whitespace-nowrap gap-2 shadow-xs cursor-pointer transition-colors',
  {
    variants: {
      variant: {
        primary: 'bg-primary text-white hover:bg-primary/90',
        secondary: 'bg-secondary text-white hover:bg-secondary/90',
        tertiary: 'bg-primary/30 text-primary hover:bg-primary/20',
        destructive:
          'bg-destructive-foreground text-white hover:bg-destructive/90',
        outline:
          'border border-gray-300 bg-white text-gray-700 hover:bg-gray-50',
        ghost: 'bg-transparent hover:bg-gray-100 text-gray-700',
      },
      size: {
        sm: 'px-3 py-1.5 text-sm',
        default: 'px-4 py-2',
        lg: 'px-6 py-3 text-lg',
      },
      disabled: {
        true: 'bg-gray-200 text-gray-400 cursor-not-allowed hover:bg-gray-200',
      },
    },
    defaultVariants: {
      variant: 'primary',
      size: 'default',
    },
  }
);

export function Button({
  className,
  variant,
  size,
  asChild = false,
  disabled,
  ...props
}: ComponentProps<'button'> &
  VariantProps<typeof buttonVariants> & {
    asChild?: boolean;
  }) {
  const Comp = asChild ? Slot : 'button';

  return (
    <Comp
      data-slot="button"
      className={cn(buttonVariants({ variant, size, className, disabled }))}
      disabled={disabled}
      {...props}
    />
  );
}
