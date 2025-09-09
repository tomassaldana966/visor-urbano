import { describe, it, expect, vi, beforeEach } from 'vitest';
import * as olSphere from 'ol/sphere.js';
import * as i18nModule from '@root/app/i18n';
import { formatNumberToArea, formatArea, formatLength } from './utils';

vi.mock('@root/app/i18n', () => ({
  default: { language: 'en' },
  __esModule: true,
}));

vi.mock('ol/sphere.js', () => ({
  getArea: vi.fn(),
  getLength: vi.fn(),
}));

describe('formatNumberToArea', () => {
  beforeEach(() => {
    i18nModule.default.language = 'en';
  });

  it('formats area in meters when area <= 10000', () => {
    const result = formatNumberToArea(5000);
    expect(result?.unit).toBe('meter');
    expect(result?.value).toContain('5,000');
    expect(result?.raw).toBe(5000);
    expect(result?.sup).toBe(2);
  });

  it('formats area in kilometers when area > 10000', () => {
    const result = formatNumberToArea(20000);
    expect(result?.unit).toBe('kilometer');
    expect(result?.value).toContain('0.02');
    expect(result?.raw).toBe(0.02);
    expect(result?.sup).toBe(2);
  });

  it('returns null when value is null', () => {
    const result = formatNumberToArea(null);
    expect(result).toBeNull();
  });
});

describe('formatArea', () => {
  it('calls getArea and formats the result', () => {
    const fakeGeom = {} as any;
    const getAreaSpy = vi.spyOn(olSphere, 'getArea').mockReturnValue(12345);
    const result = formatArea(fakeGeom);
    expect(getAreaSpy).toHaveBeenCalledWith(fakeGeom);
    expect(result?.unit).toBe('kilometer');
    expect(result?.sup).toBe(2);
  });

  it('returns null when geometry is null', () => {
    const result = formatArea(null);
    expect(result).toBeNull();
  });
});

describe('formatLength', () => {
  it('formats length in meters when length <= 100', () => {
    vi.spyOn(olSphere, 'getLength').mockReturnValue(50);
    const fakeLine = {} as any;
    const result = formatLength(fakeLine);

    expect(result).toBe('50 m');
  });

  it('formats length in kilometers when length > 100', () => {
    vi.spyOn(olSphere, 'getLength').mockReturnValue(1500);

    const fakeLine = {} as any;
    const result = formatLength(fakeLine);

    expect(result).toBe('1.5 km');
  });

  it('returns null when geometry is null', () => {
    const result = formatLength(null);
    expect(result).toBeNull();
  });
});
