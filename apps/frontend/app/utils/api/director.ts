import { z } from 'zod';
import { requestAPI } from './base';

// Schemas for director dashboard
const RecentActivityItemSchema = z.object({
  id: z.string(),
  type: z.string(),
  title: z.string(),
  description: z.string(),
  timestamp: z.string().transform(str => new Date(str)),
  folio: z.string().nullable().optional(),
  user_name: z.string().nullable().optional(),
  priority: z.string().nullable().optional(),
});

const DirectorDashboardResponseSchema = z.object({
  total_procedures_this_month: z.number(),
  pending_procedures: z.number(),
  licenses_issued_today: z.number(), // Changed from procedures_completed_today
  licenses_trend: z.number(), // New field for trend comparison
  average_processing_time: z.number(),
  procedures_by_type: z.object({
    construction: z.number(),
    commercial: z.number(),
    others: z.number(),
  }),
  recent_activities: z.array(RecentActivityItemSchema),
  pending_reviews: z.number(),
  alerts: z.number(),
});

const DirectorFacetsResponseSchema = z.object({
  total_procedures_this_month: z.number(),
  pending_procedures: z.number(),
  procedures_completed_today: z.number(),
  procedures_by_type: z.object({
    construction: z.number(),
    commercial: z.number(),
    others: z.number(),
  }),
});

// Type exports
export type RecentActivityItem = z.infer<typeof RecentActivityItemSchema>;
export type DirectorDashboardResponse = z.infer<
  typeof DirectorDashboardResponseSchema
>;
export type DirectorFacetsResponse = z.infer<
  typeof DirectorFacetsResponseSchema
>;

/**
 * Get complete director dashboard data including metrics and recent activities
 */
export async function getDirectorDashboard(
  authToken: string
): Promise<DirectorDashboardResponse> {
  try {
    const response = await requestAPI({
      endpoint: 'v1/director/dashboard',
      method: 'GET',
      authToken,
    });

    const result = DirectorDashboardResponseSchema.safeParse(response);

    if (result.success) {
      return result.data;
    } else {
      console.error(
        'Invalid response format for director dashboard:',
        result.error
      );
      throw new Error('Invalid response format for director dashboard');
    }
  } catch (error) {
    console.error('Error fetching director dashboard:', error);
    throw new Error('Failed to fetch director dashboard data');
  }
}

/**
 * Get director facets data (simplified metrics)
 */
export async function getDirectorFacets(
  authToken: string
): Promise<DirectorFacetsResponse> {
  try {
    const response = await requestAPI({
      endpoint: 'v1/director/facets',
      method: 'GET',
      authToken,
    });

    const result = DirectorFacetsResponseSchema.safeParse(response);

    if (result.success) {
      return result.data;
    } else {
      console.error(
        'Invalid response format for director facets:',
        result.error
      );
      throw new Error('Invalid response format for director facets');
    }
  } catch (error) {
    console.error('Error fetching director facets:', error);
    throw new Error('Failed to fetch director facets data');
  }
}
