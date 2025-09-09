import i18n from '@root/app/i18n';
import { getArea, getLength } from 'ol/sphere.js';
import type { Geometry, LineString } from 'ol/geom';

export function formatNumberToArea(area?: number | null) {
  if (!area) {
    return null;
  }

  let value;
  let unit;

  if (area > 10000) {
    unit = 'kilometer';
    value = Math.round((area / 1000000) * 100) / 100;
  } else {
    unit = 'meter';
    value = Math.round(area * 100) / 100;
  }

  const language = i18n.language;

  return {
    raw: value,
    sup: 2,
    unit,
    value: new Intl.NumberFormat(language, {
      style: 'unit',
      unit,
    }).format(value),
  };
}

export function formatArea(polygon: Geometry | null) {
  if (!polygon) {
    return null;
  }

  const area = getArea(polygon);

  return formatNumberToArea(area);
}

export function formatLength(line: LineString | null) {
  if (!line) {
    return null;
  }

  const length = getLength(line);
  let value;
  let unit;

  if (length > 100) {
    unit = 'kilometer';
    value = Math.round((length / 1000) * 100) / 100;
  } else {
    unit = 'meter';
    value = Math.round(length * 100) / 100;
  }

  const language = i18n.language;

  return new Intl.NumberFormat(language, {
    style: 'unit',
    unit,
  }).format(value);
}
