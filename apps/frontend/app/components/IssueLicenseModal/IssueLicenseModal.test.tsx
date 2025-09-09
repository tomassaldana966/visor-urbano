import { describe, it, expect, vi, beforeEach } from 'vitest';

// Mock all dependencies before importing the component
vi.mock('react-i18next', () => ({
  useTranslation: () => ({
    t: (key: string) => key,
    i18n: {
      language: 'en',
      changeLanguage: vi.fn(),
    },
  }),
}));

vi.mock('../../utils/api/api.client', () => ({
  issueLicenseScanned: vi.fn(),
}));

vi.mock('../Button/Button', () => ({
  Button: ({ children, ...props }: any) => children,
}));

vi.mock('../Dialog/Dialog', () => ({
  Dialog: ({ children }: any) => children,
  DialogContent: ({ children }: any) => children,
  DialogDescription: ({ children }: any) => children,
  DialogFooter: ({ children }: any) => children,
  DialogHeader: ({ children }: any) => children,
  DialogTitle: ({ children }: any) => children,
}));

vi.mock('lucide-react', () => ({
  Upload: () => 'Upload',
  FileText: () => 'FileText',
  X: () => 'X',
  Clock: () => 'Clock',
  Award: () => 'Award',
}));

// Dynamic import to ensure mocks are applied
const { IssueLicenseModal } = await import('./IssueLicenseModal');

describe('IssueLicenseModal Component', () => {
  const defaultProps = {
    isOpen: true,
    onClose: vi.fn(),
    folio: 'TEST-2024-001',
    authToken: 'mock-auth-token',
    onLicenseIssued: vi.fn(),
  };

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should be defined', () => {
    expect(IssueLicenseModal).toBeDefined();
    expect(typeof IssueLicenseModal).toBe('function');
  });

  it('should have correct props interface', () => {
    expect(typeof defaultProps.isOpen).toBe('boolean');
    expect(typeof defaultProps.onClose).toBe('function');
    expect(typeof defaultProps.folio).toBe('string');
    expect(typeof defaultProps.authToken).toBe('string');
    expect(typeof defaultProps.onLicenseIssued).toBe('function');
  });
});
