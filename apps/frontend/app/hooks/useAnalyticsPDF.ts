import { useCallback } from 'react';
import { useTranslation } from 'react-i18next';
import { generateAnalyticsPDF, type AnalyticsData } from '../utils/pdf';

export function useAnalyticsPDF() {
  const { t } = useTranslation('director');

  const generatePDF = useCallback(
    async (analytics: AnalyticsData, selectedPeriod: string) => {
      try {
        await generateAnalyticsPDF(analytics, t, selectedPeriod);

        return { success: true };
      } catch (error) {
        console.error('Error generating analytics PDF:', error);
        return {
          success: false,
          error: error instanceof Error ? error.message : 'Unknown error',
        };
      }
    },
    [t]
  );

  return { generatePDF };
}
