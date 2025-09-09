import { z } from 'zod';
import { requestAPI } from './base';

export async function getTechnicalSheetURL(data: {
  address: string;
  square_meters: string;
  coordinates: string;
  image: string;
  municipality_id: number;
  technical_sheet_download_id: number | null;
}) {
  return requestAPI({
    endpoint: 'v1/technical_sheets',
    method: 'POST',
    data,
  }).then(response => {
    const schema = z.object({
      uuid: z.string(),
    });

    const result = schema.safeParse(response);

    if (result.success) {
      return `/technical-sheet/${result.data.uuid}`;
    } else {
      return null;
    }
  });
}
