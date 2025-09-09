import { vi } from 'vitest';

// Mock React Router since we're not using it in component tests
vi.mock('@remix-run/react', () => ({
  useNavigate: () => vi.fn(),
  useLocation: () => ({ pathname: '/', search: '', hash: '', state: null }),
  useParams: () => ({}),
  Link: ({ children, to, ...props }: any) => children,
  useLoaderData: () => ({}),
  useSearchParams: () => [new URLSearchParams(), vi.fn()],
  useFetcher: () => ({
    Form: 'form',
    submit: vi.fn(),
    state: 'idle',
    data: null,
  }),
  Form: 'form',
}));

// Mock react-i18next
vi.mock('react-i18next', () => ({
  useTranslation: () => ({
    t: (key: string) => key,
    i18n: {
      language: 'en',
      changeLanguage: vi.fn(),
    },
  }),
  Trans: ({ children }: any) => children,
}));

// Mock lib/utils
vi.mock('@/lib/utils', () => ({
  cn: (...classes: any[]) => classes.filter(Boolean).join(' '),
  capitalizeWords: (str: string) => str,
}));

// Mock lucide-react icons
vi.mock('lucide-react', () => {
  const MockIcon = ({ className, ...props }: any) => ({
    type: 'svg',
    props: { className, ...props, children: 'MockIcon' },
  });

  return new Proxy(
    {},
    {
      get: () => MockIcon,
    }
  );
});

// Setup DOM environment
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
});

// Mock IntersectionObserver
Object.defineProperty(window, 'IntersectionObserver', {
  writable: true,
  value: vi.fn().mockImplementation(() => ({
    observe: vi.fn(),
    unobserve: vi.fn(),
    disconnect: vi.fn(),
  })),
});

// Mock ResizeObserver
Object.defineProperty(window, 'ResizeObserver', {
  writable: true,
  value: vi.fn().mockImplementation(() => ({
    observe: vi.fn(),
    unobserve: vi.fn(),
    disconnect: vi.fn(),
  })),
});
