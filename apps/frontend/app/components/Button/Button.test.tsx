import { describe, it, expect, vi } from 'vitest';
import { Button } from './Button';

describe('Button Component', () => {
  it('should be defined', () => {
    expect(Button).toBeDefined();
    expect(typeof Button).toBe('function');
  });

  it('should accept basic props', () => {
    const props = {
      children: 'Test Button',
      onClick: vi.fn(),
    };

    expect(() => Button(props)).not.toThrow();
  });

  it('should accept variant props', () => {
    const variants = [
      'primary',
      'secondary',
      'tertiary',
      'destructive',
      'outline',
      'ghost',
    ] as const;

    variants.forEach(variant => {
      const props = { variant, children: 'Test' };
      expect(() => Button(props)).not.toThrow();
    });
  });

  it('should accept size props', () => {
    const sizes = ['sm', 'default', 'lg'] as const;

    sizes.forEach(size => {
      const props = { size, children: 'Test' };
      expect(() => Button(props)).not.toThrow();
    });
  });

  it('should accept disabled prop', () => {
    const props = { disabled: true, children: 'Disabled' };
    expect(() => Button(props)).not.toThrow();
  });

  it('should accept asChild prop', () => {
    const props = { asChild: true, children: 'As Child' };
    expect(() => Button(props)).not.toThrow();
  });

  it('should accept className prop', () => {
    const props = { className: 'custom-class', children: 'Custom' };
    expect(() => Button(props)).not.toThrow();
  });

  it('should accept additional HTML attributes', () => {
    const props = {
      children: 'Test',
      'data-testid': 'test-button',
      'aria-label': 'Test button',
      type: 'submit' as const,
    };

    expect(() => Button(props)).not.toThrow();
  });

  it('should handle all props combinations', () => {
    const props = {
      variant: 'secondary' as const,
      size: 'lg' as const,
      disabled: true,
      asChild: false,
      className: 'extra-class',
      onClick: vi.fn(),
      children: 'Complex Button',
    };

    expect(() => Button(props)).not.toThrow();
  });
});
