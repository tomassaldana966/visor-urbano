import { z } from 'zod';
import { requestAPI } from './base';

export type NotificationData = {
  id: number;
  user_id: number;
  applicant_email: string;
  comment: string;
  file?: string | null;
  folio: string;
  creation_date: string;
  seen_date?: string | null;
  dependency_file?: string | null;
  notified?: number | null;
  notifying_department: number;
  notification_type: number;
  resolution_id: number;
  created_at: string;
  updated_at: string;
};

export type NotificationsResponse = {
  notifications: NotificationData[];
  total_count: number;
  page: number;
  per_page: number;
  has_next: boolean;
  has_prev: boolean;
};

export type FileTypeData = {
  id: number;
  procedure_id: number;
  file_path?: string | null;
  file_type?: string | null;
  created_at?: string | null;
  updated_at?: string | null;
};

export async function getNotifications(
  authToken: string,
  params: { page?: number; per_page?: number } = {}
): Promise<NotificationsResponse> {
  const response = await requestAPI({
    endpoint: 'v1/notifications/',
    method: 'GET',
    data: params,
    authToken,
  });

  const schema = z.object({
    notifications: z.array(
      z.object({
        id: z.number(),
        user_id: z.number(),
        applicant_email: z.string(),
        comment: z.string(),
        file: z.string().nullable().optional(),
        folio: z.string(),
        creation_date: z.string(),
        seen_date: z.string().nullable().optional(),
        dependency_file: z.string().nullable().optional(),
        notified: z.number().nullable().optional(),
        notifying_department: z.number(),
        notification_type: z.number(),
        resolution_id: z.number(),
        created_at: z.string(),
        updated_at: z.string(),
      })
    ),
    total_count: z.number(),
    page: z.number(),
    per_page: z.number(),
    has_next: z.boolean(),
    has_prev: z.boolean(),
  });

  const result = schema.safeParse(response);

  if (result.success) {
    return result.data as NotificationsResponse;
  } else {
    console.error('Validation error:', result.error.issues);
    console.error('Received response:', JSON.stringify(response, null, 2));
    throw new Error(
      `Invalid response format for notifications: ${result.error.issues.map(i => `${i.path.join('.')}: ${i.message}`).join(', ')}`
    );
  }
}

export async function markNotificationAsRead(
  authToken: string,
  notificationId: number
): Promise<{ message: string; status_code: number }> {
  const response = await requestAPI({
    endpoint: `v1/notifications/${notificationId}/read` as const,
    method: 'PATCH',
    data: {},
    authToken,
  });

  const schema = z.object({
    message: z.string(),
    status_code: z.number(),
  });

  const result = schema.safeParse(response);

  if (result.success) {
    return result.data as { message: string; status_code: number };
  } else {
    throw new Error('Invalid response format for mark as read');
  }
}

export async function getProcedureFiles(
  authToken: string,
  procedureId: number
): Promise<FileTypeData[]> {
  const response = await requestAPI({
    endpoint: `v1/notifications/procedure/${procedureId}/files` as const,
    method: 'GET',
    data: {},
    authToken,
  });

  const schema = z.array(
    z.object({
      id: z.number(),
      procedure_id: z.number(),
      file_path: z.string().nullable().optional(),
      file_type: z.string().nullable().optional(),
      created_at: z.string().nullable().optional(),
      updated_at: z.string().nullable().optional(),
    })
  );

  const result = schema.safeParse(response);

  if (result.success) {
    return result.data as FileTypeData[];
  } else {
    throw new Error('Invalid response format for procedure files');
  }
}
