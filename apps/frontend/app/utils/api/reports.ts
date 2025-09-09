import { z } from 'zod';
import { requestAPI } from './base';

// Schema definitions based on backend models
const ChartPointSchema = z.object({
  name: z.string(),
  value: z.number(),
  extra: z.number().optional(),
});

const LicensingStatusSummarySchema = z.object({
  consultation: z.number(),
  initiated: z.number(),
  under_review: z.number(),
  issued: z.number(),
});

const BarListFilterSchema = z.object({
  month: z.number(),
  start_date: z.string(),
  end_date: z.string(),
  municipality_id: z.number().optional(),
});

const BarListItemSchema = z.object({
  folio: z.string(),
  street: z.string(),
  neighborhood: z.string(),
  scian_code: z.string(),
  scian_name: z.string(),
  number_license: z.string().optional(),
  owner: z.string().optional(),
  license_year: z.string().optional(),
});

const ReviewStatusSummarySchema = z.object({
  approved: z.number(),
  under_review: z.number(),
  corrected: z.number(),
  discarded: z.number(),
});

const MunicipalityPiePointSchema = z.object({
  name: z.string(),
  value: z.number(),
  extra: z.number(),
});

const MunicipalityLicenseSummarySchema = z.object({
  id: z.number(),
  name: z.string(),
  total_refrendo: z.number(),
  total_nueva: z.number(),
  total_final: z.number(),
});

const MunicipalityHistoricSummarySchema = z.object({
  id: z.number(),
  name: z.string(),
  total: z.number(),
});

const FullReportResponseSchema = z.object({
  total_current: z.number(),
  total_refrendo_current: z.number(),
  total_nueva_current: z.number(),
  total_historic: z.number(),
  total_combined: z.number(),
  current_by_municipality: z.array(MunicipalityLicenseSummarySchema),
  historic_by_municipality: z.array(MunicipalityHistoricSummarySchema),
});

const TechnicalSheetDownloadSchema = z.object({
  id: z.number(),
  name: z.string(),
  email: z.string(),
  age: z.number(),
  city: z.string(),
  sector: z.string(),
  uses: z.array(z.string()),
  address: z.string(),
  municipality: z.string(),
  created_at: z.string(),
});

const TechnicalSheetReportSummarySchema = z.object({
  sectors_percentage: z.record(z.number()),
  uses_percentage: z.record(z.number()),
  age_distribution: z.record(z.number()),
  top_cities: z.record(z.number()),
  users_per_municipality: z.record(z.number()),
  data: z.array(TechnicalSheetDownloadSchema),
});

// New schemas for calculated analytics
const KPIsSummarySchema = z.object({
  tiempo_promedio: z.number(),
  eficiencia: z.number(),
  total_procesados: z.number(),
  satisfaccion: z.number(),
});

const StatusDistributionSchema = z.object({
  estado: z.string(),
  cantidad: z.number(),
  porcentaje: z.number(),
  color: z.string(),
});

const DependencyMetricsSchema = z.object({
  id: z.string(),
  nombre: z.string(),
  tramites_procesados: z.number(),
  tiempo_promedio: z.number(),
  eficiencia: z.number(),
  estado: z.string(),
});

const CompleteAnalyticsSchema = z.object({
  kpis: KPIsSummarySchema,
  tendencias: z.array(ChartPointSchema),
  distribucion_estados: z.array(StatusDistributionSchema),
  dependencias: z.array(DependencyMetricsSchema),
  licensing_status: LicensingStatusSummarySchema,
  review_status: ReviewStatusSummarySchema,
});

// Type exports
export type ChartPoint = z.infer<typeof ChartPointSchema>;
export type LicensingStatusSummary = z.infer<
  typeof LicensingStatusSummarySchema
>;
export type BarListFilter = z.infer<typeof BarListFilterSchema>;
export type BarListItem = z.infer<typeof BarListItemSchema>;
export type ReviewStatusSummary = z.infer<typeof ReviewStatusSummarySchema>;
export type MunicipalityPiePoint = z.infer<typeof MunicipalityPiePointSchema>;
export type MunicipalityLicenseSummary = z.infer<
  typeof MunicipalityLicenseSummarySchema
>;
export type MunicipalityHistoricSummary = z.infer<
  typeof MunicipalityHistoricSummarySchema
>;
export type FullReportResponse = z.infer<typeof FullReportResponseSchema>;
export type TechnicalSheetDownload = z.infer<
  typeof TechnicalSheetDownloadSchema
>;
export type TechnicalSheetReportSummary = z.infer<
  typeof TechnicalSheetReportSummarySchema
>;

// New types for calculated analytics
export type KPIsSummary = z.infer<typeof KPIsSummarySchema>;
export type StatusDistribution = z.infer<typeof StatusDistributionSchema>;
export type DependencyMetrics = z.infer<typeof DependencyMetricsSchema>;
export type CompleteAnalytics = z.infer<typeof CompleteAnalyticsSchema>;

/**
 * Get annual bar chart data for the current user's municipality
 */
export async function getAnnualBarChart(
  authToken: string
): Promise<ChartPoint[]> {
  const response = await requestAPI({
    endpoint: 'v1/reports/charts/annual-bar',
    method: 'GET',
    authToken,
  });

  const result = z.array(ChartPointSchema).safeParse(response);

  if (result.success) {
    return result.data;
  } else {
    throw new Error('Invalid response format for annual bar chart');
  }
}

/**
 * Get licensing status summary (advanced pie chart) for the current user's municipality
 */
export async function getLicensingStatusSummary(
  authToken: string
): Promise<LicensingStatusSummary> {
  const response = await requestAPI({
    endpoint: 'v1/reports/charts/advanced-pie',
    method: 'GET',
    authToken,
  });

  const result = LicensingStatusSummarySchema.safeParse(response);

  if (result.success) {
    return result.data;
  } else {
    throw new Error('Invalid response format for licensing status summary');
  }
}

/**
 * Get annual bar chart data for a specific municipality (admin function)
 */
export async function getAnnualBarByMunicipality(
  municipalityId: number,
  authToken: string
): Promise<ChartPoint[]> {
  const response = await requestAPI({
    endpoint: `v1/reports/charts/annual-bar/${municipalityId}`,
    method: 'GET',
    authToken,
  });

  const result = z.array(ChartPointSchema).safeParse(response);

  if (result.success) {
    return result.data;
  } else {
    throw new Error(
      'Invalid response format for annual bar chart by municipality'
    );
  }
}

/**
 * Get licensing status summary for admin with optional municipality filter
 */
export async function getLicensingStatusAdmin(
  authToken: string,
  municipalityId?: number
): Promise<LicensingStatusSummary> {
  const response = await requestAPI({
    endpoint: 'v1/reports/charts/advanced-pie-admin',
    method: 'GET',
    data: municipalityId ? { municipality_id: municipalityId } : undefined,
    authToken,
  });

  const result = LicensingStatusSummarySchema.safeParse(response);

  if (result.success) {
    return result.data;
  } else {
    throw new Error('Invalid response format for licensing status admin');
  }
}

/**
 * Get bar list data with filters
 */
export async function getBarList(
  filters: BarListFilter,
  authToken: string
): Promise<BarListItem[]> {
  const response = await requestAPI({
    endpoint: 'v1/reports/charts/bar-list',
    method: 'POST',
    data: filters,
    authToken,
  });

  const result = z.array(BarListItemSchema).safeParse(response);

  if (result.success) {
    return result.data;
  } else {
    throw new Error('Invalid response format for bar list');
  }
}

/**
 * Get review status pie chart data for the current user's municipality
 */
export async function getReviewStatusPie(
  authToken: string
): Promise<ReviewStatusSummary> {
  const response = await requestAPI({
    endpoint: 'v1/reports/charts/review-pie',
    method: 'GET',
    authToken,
  });

  const result = ReviewStatusSummarySchema.safeParse(response);

  if (result.success) {
    return result.data;
  } else {
    throw new Error('Invalid response format for review status pie');
  }
}

/**
 * Get pie chart data by municipality within a date range
 */
export async function getPieByMunicipality(
  startDate: string,
  endDate: string,
  authToken: string
): Promise<MunicipalityPiePoint[]> {
  const response = await requestAPI({
    endpoint: 'v1/reports/charts/pie-by-municipality',
    method: 'GET',
    data: { start_date: startDate, end_date: endDate },
    authToken,
  });

  const result = z.array(MunicipalityPiePointSchema).safeParse(response);

  if (result.success) {
    return result.data;
  } else {
    throw new Error('Invalid response format for pie by municipality');
  }
}

/**
 * Get monthly bar chart data for a specific municipality
 */
export async function getMonthlyBarByMunicipality(
  municipalityId: number,
  startDate: string,
  endDate: string,
  authToken: string
): Promise<ChartPoint[]> {
  const response = await requestAPI({
    endpoint: `v1/reports/charts/monthly-bar/${municipalityId}`,
    method: 'GET',
    data: { start_date: startDate, end_date: endDate },
    authToken,
  });

  const result = z.array(ChartPointSchema).safeParse(response);

  if (result.success) {
    return result.data;
  } else {
    throw new Error('Invalid response format for monthly bar chart');
  }
}

/**
 * Get full license report
 */
export async function getFullLicenseReport(
  authToken: string
): Promise<FullReportResponse> {
  const response = await requestAPI({
    endpoint: 'v1/reports/charts/full-report',
    method: 'GET',
    authToken,
  });

  const result = FullReportResponseSchema.safeParse(response);

  if (result.success) {
    return result.data;
  } else {
    throw new Error('Invalid response format for full license report');
  }
}

/**
 * Get technical sheets summary report
 */
export async function getTechnicalSheetsReport(
  authToken: string
): Promise<TechnicalSheetReportSummary> {
  const response = await requestAPI({
    endpoint: 'v1/reports/charts/technical-sheets-summary',
    method: 'GET',
    authToken,
  });

  const result = TechnicalSheetReportSummarySchema.safeParse(response);

  if (result.success) {
    return result.data;
  } else {
    throw new Error('Invalid response format for technical sheets report');
  }
}

/**
 * Get complete analytics data with all calculations done in backend
 * This replaces the previous getDirectorAnalytics with calculated KPIs
 */
export async function getCompleteAnalytics(
  authToken: string
): Promise<CompleteAnalytics> {
  try {
    const response = await requestAPI({
      endpoint: 'v1/reports/charts/complete-analytics',
      method: 'GET',
      authToken,
    });

    const result = CompleteAnalyticsSchema.safeParse(response);

    if (result.success) {
      return result.data;
    } else {
      console.error(
        'Invalid response format for complete analytics:',
        result.error
      );
      throw new Error('Invalid response format for complete analytics');
    }
  } catch (error) {
    console.error('Error fetching complete analytics:', error);
    throw new Error('Failed to fetch complete analytics data');
  }
}

/**
 * Get detailed analytics data for a specific municipality
 * This includes trends, status distribution, and dependency metrics
 */
export async function getMunicipalityAnalytics(
  municipalityId: number,
  authToken: string
): Promise<CompleteAnalytics> {
  const response = await requestAPI({
    endpoint: `v1/reports/charts/complete-analytics/${municipalityId}`,
    method: 'GET',
    authToken,
  });

  const result = CompleteAnalyticsSchema.safeParse(response);

  if (result.success) {
    return result.data;
  } else {
    throw new Error('Invalid response format for municipality analytics');
  }
}
