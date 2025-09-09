import { useState, useEffect, useCallback } from 'react';
import { getMunicipalitySignatures } from '@root/app/utils/api/municipalities';

export interface Signature {
  id: number;
  municipality_id: number;
  signer_name: string;
  position_title: string;
  order_index: number;
  signature_image: string | null;
  is_active: string;
  created_at: string;
  updated_at: string;
}

export function useSignatures(municipalityId?: number) {
  const [signatures, setSignatures] = useState<Signature[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchSignatures = useCallback(async () => {
    if (!municipalityId) {
      setSignatures([]);
      setIsLoading(false);
      return;
    }

    try {
      setIsLoading(true);
      setError(null);
      const data = await getMunicipalitySignatures(municipalityId);

      // Fix signature image URLs
      const processedSignatures = data.map(signature => {
        if (
          signature.signature_image &&
          !signature.signature_image.startsWith('http')
        ) {
          const apiUrl =
            import.meta.env.VITE_API_URL || 'http://localhost:8000';
          const newUrl = `${apiUrl}/${signature.signature_image}`;

          return {
            ...signature,
            signature_image: newUrl,
          };
        }
        return signature;
      });

      setSignatures(processedSignatures);
    } catch (err) {
      console.error('Error fetching signatures:', err);
      setError(err instanceof Error ? err.message : 'Unknown error');
      setSignatures([]);
    } finally {
      setIsLoading(false);
    }
  }, [municipalityId]);

  useEffect(() => {
    fetchSignatures();
  }, [fetchSignatures]);

  return {
    signatures,
    isLoading,
    error,
    refetch: fetchSignatures,
  };
}
