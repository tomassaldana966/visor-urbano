/**
 * Utility functions for folio encoding/decoding
 * Used for secure transmission of folio values in URLs
 */

/**
 * Encode a folio to base64 for URL transmission
 * @param folio - The folio string to encode
 * @returns Base64 encoded folio
 */
export function encodeFolio(folio: string): string {
  if (!folio) return '';
  try {
    return btoa(folio);
  } catch (error) {
    console.error('Error encoding folio:', error);
    return folio; // Return original if encoding fails
  }
}

/**
 * Decode a base64 folio back to original string
 * @param encodedFolio - The base64 encoded folio
 * @returns Decoded folio string
 */
export function decodeFolio(encodedFolio: string): string {
  if (!encodedFolio) return '';
  try {
    return atob(encodedFolio);
  } catch (error) {
    console.error('Error decoding folio:', error);
    return encodedFolio; // Return original if decoding fails
  }
}

/**
 * Validate if a string is a valid base64 encoded folio
 * @param encodedFolio - The string to validate
 * @returns True if valid base64, false otherwise
 */
export function isValidEncodedFolio(encodedFolio: string): boolean {
  if (!encodedFolio) return false;
  try {
    return btoa(atob(encodedFolio)) === encodedFolio;
  } catch (error) {
    return false;
  }
}
