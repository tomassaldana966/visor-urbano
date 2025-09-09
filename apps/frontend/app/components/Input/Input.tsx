import { useId, type ComponentProps, type ReactNode } from 'react';
import { Label } from '../Label';
import { useTranslation } from 'react-i18next';
import { tv, type VariantProps } from 'tailwind-variants';

const inputVariants = tv({
  slots: {
    container: 'flex flex-col gap-2',
    input:
      'file:text-foreground bg-white placeholder:text-muted-foreground selection:bg-primary selection:text-primary-foreground dark:bg-input/30 border-input flex min-h-[2.5rem] w-full min-w-0 rounded-md border px-3 py-3 text-base shadow-xs transition-[color,box-shadow] outline-none file:inline-flex file:h-7 file:border-0 file:text-sm file:font-medium disabled:pointer-events-none disabled:cursor-not-allowed disabled:opacity-50 md:text-sm focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px]',
    inputContainer: 'flex items-center gap-2',
  },
  variants: {
    error: {
      true: 'aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 aria-invalid:border-destructive',
    },
    readOnly: {
      true: {
        input: 'bg-muted cursor-not-allowed opacity-80',
      },
    },
  },
});

type InputVariants = VariantProps<typeof inputVariants>;

export function Input({
  className,
  type,
  pre,
  post,
  label,
  error,
  ...props
}: React.ComponentProps<'input'> &
  Omit<InputVariants, 'error' | 'type' | 'readOnly'> & {
    pre?: ReactNode;
    post?: ReactNode;
    label?: string | ReactNode;
    error?: string | null;
    type?: Exclude<ComponentProps<'input'>['type'], 'checkbox'>;
  }) {
  const { t: tErrors } = useTranslation('errors');

  const id = useId();

  const { input, container, inputContainer } = inputVariants({
    readOnly: props.readOnly,
  });

  return (
    <div>
      <div className={container()}>
        {label ? (
          <Label htmlFor={id} className="flex">
            {label}
          </Label>
        ) : null}

        <div className={inputContainer()}>
          {pre ? <div>{pre}</div> : null}

          <input
            className={input()}
            id={id}
            type={type}
            data-slot="input"
            aria-invalid={!!error}
            {...props}
          />

          {post ? <div>{post}</div> : null}
        </div>

        {error ? (
          <div className="text-sm text-red-500">{tErrors(error)}</div>
        ) : null}
      </div>
    </div>
  );
}
