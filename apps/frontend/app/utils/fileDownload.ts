/**
 * Utility functions for handling file downloads and URLs
 */

const API_URL =
  typeof window !== 'undefined'
    ? (window as any).ENV?.API_URL || 'http://localhost:8000'
    : import.meta.env.VITE_API_URL || 'http://localhost:8000';

/**
 * Generate a download URL for a procedure file
 */
export function getFileDownloadUrl(
  procedureId: number,
  fieldName: string
): string {
  return `${API_URL}/v1/procedures/${procedureId}/download/${encodeURIComponent(fieldName)}`;
}

/**
 * Generate a view URL for a procedure file (opens in new tab)
 */
export function getFileViewUrl(procedureId: number, fieldName: string): string {
  return getFileDownloadUrl(procedureId, fieldName);
}

/**
 * Extract file info from a stored file value (JSON string or object)
 */
export function parseFileValue(value: unknown): {
  filename: string;
  originalName?: string;
  size?: number;
  contentType?: string;
  filePath?: string;
} | null {
  try {
    if (!value) return null;

    let parsedValue = value;

    // Handle string values
    if (typeof value === 'string') {
      // Try to parse as JSON first
      if (value.startsWith('{') && value.endsWith('}')) {
        try {
          parsedValue = JSON.parse(value);
        } catch (e) {
          try {
            // Convert Python dict format to JSON format
            const jsonStr = value
              .replace(/'/g, '"') // Replace single quotes with double quotes
              .replace(/(\w+):/g, '"$1":'); // Quote unquoted keys
            parsedValue = JSON.parse(jsonStr);
          } catch (e2) {
            parsedValue = value;
          }
        }
      } else {
        // If it doesn't look like JSON/dict, treat as plain filename
        parsedValue = value;
      }
    }

    // Extract filename
    const filename =
      typeof parsedValue === 'object' &&
      parsedValue !== null &&
      'filename' in parsedValue
        ? (parsedValue as { filename: string }).filename
        : typeof parsedValue === 'object' &&
            parsedValue !== null &&
            'name' in parsedValue
          ? (parsedValue as { name: string }).name
          : typeof parsedValue === 'string'
            ? parsedValue
            : 'Unknown file';

    const originalName =
      typeof parsedValue === 'object' &&
      parsedValue !== null &&
      'original_name' in parsedValue
        ? (parsedValue as { original_name: string }).original_name
        : filename;

    const size =
      typeof parsedValue === 'object' &&
      parsedValue !== null &&
      'size' in parsedValue
        ? (parsedValue as { size: number }).size
        : undefined;

    const contentType =
      typeof parsedValue === 'object' &&
      parsedValue !== null &&
      'content_type' in parsedValue
        ? (parsedValue as { content_type: string }).content_type
        : typeof parsedValue === 'object' &&
            parsedValue !== null &&
            'type' in parsedValue
          ? (parsedValue as { type: string }).type
          : '';

    const filePath =
      typeof parsedValue === 'object' &&
      parsedValue !== null &&
      'file_path' in parsedValue
        ? (parsedValue as { file_path: string }).file_path
        : undefined;

    const result = {
      filename,
      originalName,
      size,
      contentType,
      filePath,
    };

    return result;
  } catch (error) {
    console.error('Error parsing file value:', error);
    return null;
  }
}
