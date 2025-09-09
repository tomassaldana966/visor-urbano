import { useState, useEffect } from 'react';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from '@root/app/components/Dialog/Dialog';
import { Button } from '@root/app/components/Button/Button';
import { useTranslation } from 'react-i18next';
import { FileText, Download, ExternalLink, Loader2 } from 'lucide-react';

// Define the file type locally since we can't import from server file
type FileTypeData = {
  id: number;
  file_path: string;
  file_name: string;
  file_type: string;
  file_size: number;
  uploaded_at: string;
  created_at: string;
  updated_at: string;
};

interface ProcedureFilesModalProps {
  isOpen: boolean;
  onClose: () => void;
  procedureId: number | null;
  authToken: string;
}

export function ProcedureFilesModal({
  isOpen,
  onClose,
  procedureId,
  authToken,
}: ProcedureFilesModalProps) {
  const { t: tProcedures } = useTranslation('procedures');
  const [files, setFiles] = useState<FileTypeData[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (isOpen && procedureId && authToken) {
      loadFiles();
    }
  }, [isOpen, procedureId, authToken]);

  const loadFiles = async () => {
    if (!procedureId) return;

    setLoading(true);
    setError(null);

    try {
      // Make direct API call to get procedure files
      const response = await fetch(
        `/v1/notifications/procedure/${procedureId}/files`,
        {
          method: 'GET',
          headers: {
            Authorization: `Bearer ${authToken}`,
            'Content-Type': 'application/json',
          },
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const filesData: FileTypeData[] = await response.json();
      setFiles(filesData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error loading files');
    } finally {
      setLoading(false);
    }
  };

  // Helper function to format date
  const formatDate = (dateString: string | null | undefined) => {
    if (!dateString) return '--';
    try {
      return new Date(dateString).toLocaleDateString('es-MX', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
      });
    } catch {
      return '--';
    }
  };

  // Helper function to get file type icon
  const getFileTypeIcon = (fileType: string | null | undefined) => {
    const type = fileType?.toLowerCase();
    if (type?.includes('pdf')) return '📄';
    if (
      type?.includes('image') ||
      type?.includes('jpg') ||
      type?.includes('png')
    )
      return '🖼️';
    if (type?.includes('doc') || type?.includes('word')) return '📝';
    if (type?.includes('excel') || type?.includes('sheet')) return '📊';
    return '📁';
  };

  const handleDownload = (file: FileTypeData) => {
    // TODO: Implement file download logic
  };

  const handleView = (file: FileTypeData) => {
    // TODO: Implement file view logic
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-3xl max-h-[80vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <FileText size={20} />
            {tProcedures('filesModal.title')}
          </DialogTitle>
        </DialogHeader>

        <div className="space-y-4">
          {loading && (
            <div className="flex items-center justify-center py-8">
              <Loader2 className="h-6 w-6 animate-spin" />
              <span className="ml-2">{tProcedures('filesModal.loading')}</span>
            </div>
          )}

          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <p className="text-red-800 text-sm">{error}</p>
              <Button variant="secondary" onClick={loadFiles} className="mt-2">
                {tProcedures('filesModal.retry')}
              </Button>
            </div>
          )}

          {!loading && !error && files.length === 0 && (
            <div className="text-center py-8 text-gray-500">
              <FileText size={48} className="mx-auto mb-4 opacity-50" />
              <p>{tProcedures('filesModal.noFiles')}</p>
            </div>
          )}

          {!loading && !error && files.length > 0 && (
            <div className="space-y-3">
              {files.map(file => (
                <div
                  key={file.id}
                  className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition-colors"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex items-start gap-3 flex-1">
                      <span className="text-2xl">
                        {getFileTypeIcon(file.file_type)}
                      </span>

                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-1">
                          <p className="font-medium text-sm truncate">
                            {file.file_path?.split('/').pop() ||
                              `${tProcedures('filesModal.file')} ${file.id}`}
                          </p>
                          {file.file_type && (
                            <span className="text-xs bg-gray-100 px-2 py-1 rounded">
                              {file.file_type}
                            </span>
                          )}
                        </div>

                        <div className="text-xs text-gray-500 space-y-1">
                          <p>
                            {tProcedures('filesModal.uploadDate')}:{' '}
                            {formatDate(file.created_at)}
                          </p>
                          {file.updated_at !== file.created_at && (
                            <p>
                              {tProcedures('filesModal.modifiedDate')}:{' '}
                              {formatDate(file.updated_at)}
                            </p>
                          )}
                        </div>
                      </div>
                    </div>

                    <div className="flex items-center gap-2 ml-4">
                      <Button
                        variant="tertiary"
                        onClick={() => handleView(file)}
                        className="px-2 py-1"
                        title={tProcedures('filesModal.view')}
                      >
                        <ExternalLink size={14} />
                      </Button>

                      <Button
                        variant="tertiary"
                        onClick={() => handleDownload(file)}
                        className="px-2 py-1"
                        title={tProcedures('filesModal.download')}
                      >
                        <Download size={14} />
                      </Button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}

          <div className="flex justify-end pt-4 border-t">
            <Button variant="tertiary" onClick={onClose}>
              {tProcedures('filesModal.close')}
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
