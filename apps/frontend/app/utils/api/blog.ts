import { requestAPI } from './base';

export interface BlogEntry {
  id: number;
  title: string;
  slug?: string;
  image: string;
  link: string;
  summary: string;
  news_date: string;
  blog_type?: number;
  body?: string;
  municipality_id?: number;
  created_at?: string;
  updated_at?: string;
}

export interface BlogCreateData {
  title: string;
  image: string;
  link: string;
  summary: string;
  news_date: string;
  slug?: string;
  blog_type?: number;
  body?: string;
  municipality_id?: number;
  password: string;
}

export interface BlogUpdateData {
  title?: string;
  image?: string;
  link?: string;
  summary?: string;
  news_date?: string;
  slug?: string;
  blog_type?: number;
  body?: string;
  municipality_id?: number;
  password: string;
}

// Get all published blog entries (limited to 6)
export async function getPublishedBlogs(): Promise<BlogEntry[]> {
  return requestAPI({
    endpoint: 'v1/blog/',
  });
}

// Get all blog entries for management (requires password)
export async function getAllBlogs(password: string): Promise<BlogEntry[]> {
  return requestAPI({
    endpoint: `v1/blog/user/${password}`,
  });
}

// Get a specific blog entry by ID
export async function getBlogById(id: number): Promise<BlogEntry> {
  return requestAPI({
    endpoint: `v1/blog/${id}`,
  });
}

// Create a new blog entry
export async function createBlog(data: BlogCreateData): Promise<BlogEntry> {
  return requestAPI({
    endpoint: 'v1/blog/',
    method: 'POST',
    data,
  });
}

// Update an existing blog entry
export async function updateBlog(
  id: number,
  data: BlogUpdateData
): Promise<BlogEntry> {
  return requestAPI({
    endpoint: `v1/blog/${id}`,
    method: 'PUT',
    data,
  });
}

// Delete a blog entry
export async function deleteBlog(
  id: number,
  password: string
): Promise<number> {
  // Encode password in base64 as required by the backend
  const encodedPassword = btoa(password);

  return requestAPI({
    endpoint: `v1/blog/${id}/${encodedPassword}`,
    method: 'DELETE',
  });
}
