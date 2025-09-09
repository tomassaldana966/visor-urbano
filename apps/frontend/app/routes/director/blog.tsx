import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { useLoaderData, type LoaderFunctionArgs } from 'react-router';
import {
  Plus,
  Edit,
  Trash2,
  Save,
  X,
  BookOpen,
  Calendar,
  User,
  Eye,
  AlertTriangle,
  CheckCircle,
  Loader2,
} from 'lucide-react';
import {
  getAllBlogs,
  createBlog,
  updateBlog,
  deleteBlog,
  type BlogEntry,
  type BlogCreateData,
  type BlogUpdateData,
} from '@root/app/utils/api/blog';
import {
  requireAuth,
  requireAccessToken,
} from '@root/app/utils/auth/auth.server';

export const handle = {
  title: 'director:navigation.blog',
  breadcrumb: 'director:navigation.blog',
};

export async function loader({ request }: LoaderFunctionArgs) {
  const user = await requireAuth(request);
  const accessToken = await requireAccessToken(request);

  return {
    user,
    accessToken,
  };
}

interface BlogModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSave: (data: BlogCreateData | BlogUpdateData) => void;
  blog?: BlogEntry;
  isLoading: boolean;
  municipalityId: number;
}

function BlogModal({
  isOpen,
  onClose,
  onSave,
  blog,
  isLoading,
  municipalityId,
}: BlogModalProps) {
  const { t: tDirector } = useTranslation('director');
  const [formData, setFormData] = useState({
    title: '',
    summary: '',
    image: '',
    link: '',
    body: '',
    news_date: new Date().toISOString().split('T')[0],
    password: '',
  });
  const [errors, setErrors] = useState<Record<string, string>>({});

  useEffect(() => {
    if (blog) {
      setFormData({
        title: blog.title,
        summary: blog.summary,
        image: blog.image,
        link: blog.link,
        body: blog.body || '',
        news_date: blog.news_date.split('T')[0],
        password: '',
      });
    } else {
      setFormData({
        title: '',
        summary: '',
        image: '',
        link: '',
        body: '',
        news_date: new Date().toISOString().split('T')[0],
        password: '',
      });
    }
    setErrors({});
  }, [blog, isOpen]);

  const validateForm = () => {
    const newErrors: Record<string, string> = {};

    if (!formData.title.trim()) {
      newErrors.title = tDirector('blog.form.titleRequired');
    }
    if (!formData.image.trim()) {
      newErrors.image = tDirector('blog.form.imageUrlRequired');
    }
    if (!formData.link.trim()) {
      newErrors.link = tDirector('blog.form.linkRequired');
    }
    if (!formData.summary.trim()) {
      newErrors.summary = tDirector('blog.form.summaryRequired');
    }
    if (!formData.password.trim()) {
      newErrors.password = tDirector('blog.form.adminPasswordRequired');
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    const data = {
      ...formData,
      municipality_id: municipalityId,
    };
    onSave(data);
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-4xl max-h-[90vh] overflow-hidden">
        <div className="flex items-center justify-between p-6 border-b">
          <h2 className="text-xl font-semibold flex items-center gap-2">
            <BookOpen className="w-5 h-5" />
            {blog ? tDirector('blog.editEntry') : tDirector('blog.createEntry')}
          </h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <form
          onSubmit={handleSubmit}
          className="p-6 overflow-y-auto max-h-[calc(90vh-140px)]"
        >
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                {tDirector('blog.form.title')}
              </label>
              <input
                type="text"
                value={formData.title}
                onChange={e =>
                  setFormData({ ...formData, title: e.target.value })
                }
                className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                  errors.title ? 'border-red-500' : 'border-gray-300'
                }`}
                required
              />
              {errors.title && (
                <p className="text-red-500 text-sm mt-1">{errors.title}</p>
              )}
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {tDirector('blog.form.imageUrl')}
                </label>
                <input
                  type="url"
                  value={formData.image}
                  onChange={e =>
                    setFormData({ ...formData, image: e.target.value })
                  }
                  className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                    errors.image ? 'border-red-500' : 'border-gray-300'
                  }`}
                  placeholder={tDirector('blog.form.imageUrlPlaceholder')}
                  required
                />
                {errors.image && (
                  <p className="text-red-500 text-sm mt-1">{errors.image}</p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {tDirector('blog.form.publicationDate')}
                </label>
                <input
                  type="date"
                  value={formData.news_date}
                  onChange={e =>
                    setFormData({ ...formData, news_date: e.target.value })
                  }
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                {tDirector('blog.form.link')}
              </label>
              <input
                type="url"
                value={formData.link}
                onChange={e =>
                  setFormData({ ...formData, link: e.target.value })
                }
                className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                  errors.link ? 'border-red-500' : 'border-gray-300'
                }`}
                placeholder={tDirector('blog.form.linkPlaceholder')}
                required
              />
              {errors.link && (
                <p className="text-red-500 text-sm mt-1">{errors.link}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                {tDirector('blog.form.summary')}
              </label>
              <textarea
                value={formData.summary}
                onChange={e =>
                  setFormData({ ...formData, summary: e.target.value })
                }
                rows={3}
                className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                  errors.summary ? 'border-red-500' : 'border-gray-300'
                }`}
                placeholder={tDirector('blog.form.summaryPlaceholder')}
                required
              />
              {errors.summary && (
                <p className="text-red-500 text-sm mt-1">{errors.summary}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                {tDirector('blog.form.fullContent')}
              </label>
              <textarea
                value={formData.body}
                onChange={e =>
                  setFormData({ ...formData, body: e.target.value })
                }
                rows={8}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder={tDirector('blog.form.fullContentPlaceholder')}
                style={{ direction: 'ltr', textAlign: 'left' }}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                {tDirector('blog.form.adminPassword')}
              </label>
              <input
                type="password"
                value={formData.password}
                onChange={e =>
                  setFormData({ ...formData, password: e.target.value })
                }
                className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                  errors.password ? 'border-red-500' : 'border-gray-300'
                }`}
                required
                placeholder={tDirector('blog.form.adminPasswordPlaceholder')}
              />
              {errors.password && (
                <p className="text-red-500 text-sm mt-1">{errors.password}</p>
              )}
            </div>
          </div>

          <div className="flex justify-end gap-3 mt-8 pt-6 border-t">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-gray-600 hover:text-gray-800 transition-colors"
            >
              {tDirector('blog.cancel')}
            </button>
            <button
              type="submit"
              disabled={isLoading}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              {isLoading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  {blog
                    ? tDirector('blog.updating')
                    : tDirector('blog.creating')}
                </>
              ) : (
                <>
                  <Save className="w-4 h-4" />
                  {blog ? tDirector('blog.update') : tDirector('blog.create')}
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default function BlogManagement() {
  const { t: tDirector, i18n } = useTranslation('director');
  const { user } = useLoaderData<typeof loader>();

  const [blogs, setBlogs] = useState<BlogEntry[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingBlog, setEditingBlog] = useState<BlogEntry | undefined>();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isPasswordLoading, setIsPasswordLoading] = useState(false);
  const [message, setMessage] = useState<{
    type: 'success' | 'error';
    text: string;
  } | null>(null);
  const [adminPassword, setAdminPassword] = useState('');
  const [tempPassword, setTempPassword] = useState('');

  const loadBlogs = async (password?: string) => {
    const passwordToUse = password || adminPassword;
    if (!passwordToUse) return;

    try {
      setIsLoading(true);
      setIsPasswordLoading(true);
      const blogList = await getAllBlogs(passwordToUse);
      setBlogs(blogList);
      setAdminPassword(passwordToUse);
      setTempPassword('');
    } catch (error) {
      setMessage({
        type: 'error',
        text:
          error instanceof Error
            ? error.message
            : tDirector('blog.messages.loadError'),
      });
    } finally {
      setIsLoading(false);
      setIsPasswordLoading(false);
    }
  };

  const handlePasswordSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (tempPassword.trim()) {
      loadBlogs(tempPassword);
    }
  };

  const handleCreateBlog = () => {
    setEditingBlog(undefined);
    setIsModalOpen(true);
  };

  const handleEditBlog = (blog: BlogEntry) => {
    setEditingBlog(blog);
    setIsModalOpen(true);
  };

  const handleSaveBlog = async (data: BlogCreateData | BlogUpdateData) => {
    try {
      setIsSubmitting(true);

      if (editingBlog) {
        await updateBlog(editingBlog.id, data as BlogUpdateData);
        setMessage({
          type: 'success',
          text: tDirector('blog.messages.updateSuccess'),
        });
      } else {
        await createBlog(data as BlogCreateData);
        setMessage({
          type: 'success',
          text: tDirector('blog.messages.createSuccess'),
        });
      }

      setIsModalOpen(false);
      await loadBlogs();
    } catch (error) {
      setMessage({
        type: 'error',
        text:
          error instanceof Error
            ? error.message
            : tDirector('blog.messages.createError'),
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDeleteBlog = async (blog: BlogEntry) => {
    if (!adminPassword) {
      setMessage({
        type: 'error',
        text: tDirector('blog.messages.passwordRequired'),
      });
      return;
    }

    if (!confirm(tDirector('blog.messages.deleteConfirm'))) {
      return;
    }

    try {
      await deleteBlog(blog.id, adminPassword);
      setMessage({
        type: 'success',
        text: tDirector('blog.messages.deleteSuccess'),
      });
      await loadBlogs();
    } catch (error) {
      setMessage({
        type: 'error',
        text:
          error instanceof Error
            ? error.message
            : tDirector('blog.messages.deleteError'),
      });
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString(i18n.language || 'en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
            <BookOpen className="w-6 h-6" />
            {tDirector('navigation.blog')}
          </h1>
          <p className="text-gray-600 mt-1">{tDirector('blog.subtitle')}</p>
        </div>

        {adminPassword && (
          <button
            onClick={handleCreateBlog}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2"
          >
            <Plus className="w-4 h-4" />
            {tDirector('blog.newEntry')}
          </button>
        )}
      </div>

      {/* Admin Password Input */}
      {!adminPassword && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
          <div className="flex items-center gap-2 text-yellow-800 mb-4">
            <AlertTriangle className="w-5 h-5" />
            <h3 className="font-medium">
              {tDirector('blog.adminAccessRequired')}
            </h3>
          </div>
          <p className="text-yellow-700 mb-4">
            {tDirector('blog.adminAccessDescription')}
          </p>
          <form onSubmit={handlePasswordSubmit} className="flex gap-3">
            <input
              type="password"
              placeholder={tDirector('blog.adminPasswordPlaceholder')}
              value={tempPassword}
              onChange={e => setTempPassword(e.target.value)}
              className="flex-1 px-3 py-2 border border-yellow-300 rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-transparent"
              autoComplete="current-password"
            />
            <button
              type="submit"
              disabled={!tempPassword.trim() || isPasswordLoading}
              className="px-4 py-2 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              {isPasswordLoading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  {tDirector('blog.loading')}
                </>
              ) : (
                tDirector('blog.access')
              )}
            </button>
          </form>
        </div>
      )}

      {/* Message */}
      {message && (
        <div
          className={`p-4 rounded-lg flex items-center gap-2 ${
            message.type === 'success'
              ? 'bg-green-50 text-green-800 border border-green-200'
              : 'bg-red-50 text-red-800 border border-red-200'
          }`}
        >
          {message.type === 'success' ? (
            <CheckCircle className="w-5 h-5" />
          ) : (
            <AlertTriangle className="w-5 h-5" />
          )}
          {message.text}
          <button
            onClick={() => setMessage(null)}
            className="ml-auto p-1 hover:bg-white hover:bg-opacity-20 rounded"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      )}

      {/* Blog List */}
      {adminPassword && (
        <div className="bg-white rounded-lg shadow-sm border">
          <div className="p-6 border-b">
            <h2 className="text-lg font-semibold">
              {tDirector('blog.list.title')}
            </h2>
            <p className="text-gray-600 text-sm mt-1">
              {tDirector('blog.list.count', { count: blogs.length })}
            </p>
          </div>

          {isLoading ? (
            <div className="p-8 text-center">
              <Loader2 className="w-8 h-8 animate-spin mx-auto text-gray-400" />
              <p className="text-gray-600 mt-2">{tDirector('blog.loading')}</p>
            </div>
          ) : blogs.length === 0 ? (
            <div className="p-8 text-center">
              <BookOpen className="w-12 h-12 text-gray-400 mx-auto" />
              <p className="text-gray-600 mt-2">
                {tDirector('blog.list.empty')}
              </p>
              <button
                onClick={handleCreateBlog}
                className="mt-4 text-blue-600 hover:text-blue-700 font-medium"
              >
                {tDirector('blog.list.createFirst')}
              </button>
            </div>
          ) : (
            <div className="divide-y">
              {blogs.map(blog => (
                <div
                  key={blog.id}
                  className="p-6 hover:bg-gray-50 transition-colors"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <h3 className="font-semibold text-gray-900 mb-2">
                        {blog.title}
                      </h3>
                      <div className="flex items-center gap-4 text-sm text-gray-600 mb-3">
                        <span className="flex items-center gap-1">
                          <Calendar className="w-4 h-4" />
                          {formatDate(blog.news_date)}
                        </span>
                        {blog.blog_type && (
                          <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-xs">
                            {tDirector('blog.list.type', {
                              type: blog.blog_type,
                            })}
                          </span>
                        )}
                      </div>
                      <p className="text-gray-700 line-clamp-3">
                        {blog.summary}
                      </p>
                      {blog.body && blog.body.length > 0 && (
                        <p className="text-gray-600 text-sm mt-2 line-clamp-2">
                          {blog.body.substring(0, 150)}
                          {blog.body.length > 150 && '...'}
                        </p>
                      )}
                    </div>

                    <div className="flex items-center gap-2 ml-4">
                      <button
                        onClick={() => handleEditBlog(blog)}
                        className="p-2 text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                        title={tDirector('blog.edit')}
                      >
                        <Edit className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => handleDeleteBlog(blog)}
                        className="p-2 text-gray-600 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                        title={tDirector('blog.delete')}
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Blog Modal */}
      <BlogModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSave={handleSaveBlog}
        blog={editingBlog}
        isLoading={isSubmitting}
        municipalityId={user.municipality_id || 1}
      />
    </div>
  );
}
