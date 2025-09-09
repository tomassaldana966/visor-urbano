// Export all functions from namespace files to maintain compatibility

// Base utilities
export { UnauthorizedError, requestAPI } from './base';

// Auth functions
export * from './auth';

// Notifications functions
export * from './notifications';

// Procedures functions
export * from './procedures';

// Business licenses functions
export * from './business_licenses';

// Users functions
export * from './users';

// Roles functions
export * from './roles';

// Municipalities functions
export * from './municipalities';

// Business types functions
export * from './business_types';

// Director functions
export * from './director';

// Fields functions
export * from './fields';

// Technical sheets functions
export * from './technical_sheets';

// Map layers functions
export * from './map_layers';

// News functions
export * from './news';

// Requirements functions
export * from './requirements';

// Reports functions
export * from './reports';

// Utility functions
export * from './zoning_impact_levels';

// Utility functions
export async function downloadFile(
  url: string,
  authToken: string
): Promise<Blob> {
  const response = await fetch(url, {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${authToken}`,
    },
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Failed to download file: ${response.status} ${errorText}`);
  }

  return response.blob();
}
