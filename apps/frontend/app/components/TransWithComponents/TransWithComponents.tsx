import type { ComponentProps } from 'react';
import { Trans } from 'react-i18next';

export function TransWithComponents(props: ComponentProps<typeof Trans>) {
  return (
    <Trans
      {...props}
      components={{
        h2: <h2 className="text-primary text-xl pt-4" />,
        ol: <ol className="px-6 marker:text-primary list-decimal" />,
        ul: <ul className="px-6 marker:text-primary list-disc" />,
        li: <li />,
        a: (
          <a
            className="text-primary"
            rel="noreferrer noopener"
            target="_blank"
          />
        ),
        p: <p />,
      }}
    />
  );
}
