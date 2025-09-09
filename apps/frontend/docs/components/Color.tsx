import { clsx } from 'clsx';

export function Color({
  className,
  name,
}: {
  className: string;
  name: string;
}) {
  return (
    <div className={clsx('p-4 font-bold justify-center flex', className)}>
      {name}
    </div>
  );
}
