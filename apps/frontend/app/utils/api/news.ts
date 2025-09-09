import { requestAPI } from './base';

export async function getNewsList(data?: { page?: number; per_page?: number }) {
  return requestAPI({
    endpoint: 'v1/news/',
    method: 'GET',
    data,
  });
}

export async function getNewsByFriendlyUrl(
  year: number,
  month: number,
  slug: string
) {
  return requestAPI({
    endpoint: `v1/news/${year}/${month}/${slug}`,
    method: 'GET',
  });
}

export async function getNewsById(id: number) {
  return requestAPI({
    endpoint: `v1/news/${id}`,
    method: 'GET',
  });
}
