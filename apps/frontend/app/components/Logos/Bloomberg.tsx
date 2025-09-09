import { cn } from '@root/app/lib/utils';
import { Link } from 'react-router';

export function BloombergLogo({ className }: { className?: string }) {
  return (
    <Link
      to="https://www.bloomberg.org/"
      target="_blank"
      rel="noreferrer noopener"
    >
      <img
        alt="Bloomberg Philanthropies"
        src="/logos/bloomberg-philanthropies.svg"
        className={cn('h-8', className)}
      />
    </Link>
  );
}
