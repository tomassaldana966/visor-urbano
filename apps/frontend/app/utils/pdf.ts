import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

export interface ProcedureData {
  folio: string;
  status: string;
  procedure_type?: string;
  official_applicant_name?: string;
  street?: string;
  exterior_number?: string;
  interior_number?: string;
  neighborhood?: string;
  municipality?: string;
  establishment_name?: string;
  establishment_address?: string;
  establishment_phone?: string;
  establishment_area?: string;
  business_name?: string;
  business_sector?: string;
  business_activity?: string;
  operating_hours?: string;
  employee_count?: string;
  created_at: string;
  updated_at: string;
}

export interface DynamicFieldData {
  id: string | number;
  name?: string;
  label?: string;
  value: any;
  field_type?: string;
  step?: number;
  options?: string | null;
  options_description?: string | null;
}

export interface AnalyticsData {
  kpis: {
    tiempo_promedio: number;
    eficiencia: number;
    total_procesados: number;
    satisfaccion: number;
  };
  tendencias: Array<{
    name: string;
    value: number;
    extra?: number;
  }>;
  distribucion_estados: Array<{
    estado: string;
    cantidad: number;
    porcentaje: number;
    color: string;
  }>;
  dependencias: Array<{
    id: string;
    nombre: string;
    tramites_procesados: number;
    tiempo_promedio: number;
    eficiencia: number;
    estado: string;
  }>;
  licensing_status: {
    consultation: number;
    initiated: number;
    under_review: number;
    issued: number;
  };
  review_status: {
    approved: number;
    under_review: number;
    corrected: number;
    discarded: number;
  };
}

export async function generateProcedurePDF(
  procedure: ProcedureData,
  dynamicFields: DynamicFieldData[][],
  t: any
): Promise<void> {
  const pdf = new jsPDF('p', 'mm', 'a4');
  const pageWidth = pdf.internal.pageSize.getWidth();
  const pageHeight = pdf.internal.pageSize.getHeight();
  const margin = 20;
  const contentWidth = pageWidth - margin * 2;
  let currentY = margin;

  // Helper function to get translated procedure type
  const getTranslatedProcedureType = (
    procedureType: string | null | undefined
  ): string => {
    if (!procedureType) return '--';

    const typeTranslations: Record<string, string> = {
      business_license: t('edit.pdf.procedureTypes.businessLicense'),
      permits_building_license: t('edit.pdf.procedureTypes.buildingLicense'),
    };

    return typeTranslations[procedureType] || procedureType;
  };
  const getReadableValue = (field: DynamicFieldData): string => {
    if (!field.value || field.value === '') return '--';

    // For radio and select fields, try to map the value to its description
    if (
      (field.field_type === 'radio' || field.field_type === 'select') &&
      field.options_description
    ) {
      try {
        // Parse the options_description which should contain the readable values
        const optionsDesc = field.options_description
          .split(',')
          .map(opt => opt.trim());
        const options = field.options
          ? field.options.split(',').map(opt => opt.trim())
          : [];

        // Find the index of the current value in options
        const valueIndex = options.findIndex(opt => opt === field.value);

        // If found, return the corresponding description, otherwise return the raw value
        if (valueIndex !== -1 && optionsDesc[valueIndex]) {
          return optionsDesc[valueIndex];
        }
      } catch (error) {
        console.warn('Error parsing options for field:', field.name, error);
      }
    }

    return String(field.value);
  };

  // Helper function to add new page if needed
  const checkNewPage = (height: number) => {
    if (currentY + height > pageHeight - margin) {
      pdf.addPage();
      currentY = margin;
    }
  };

  // Helper function to add text with word wrap
  const addText = (
    text: string,
    fontSize: number = 10,
    isBold: boolean = false
  ) => {
    pdf.setFontSize(fontSize);
    pdf.setFont('helvetica', isBold ? 'bold' : 'normal');

    const lines = pdf.splitTextToSize(text, contentWidth);
    const lineHeight = fontSize * 0.35;

    checkNewPage(lines.length * lineHeight);

    lines.forEach((line: string) => {
      pdf.text(line, margin, currentY);
      currentY += lineHeight;
    });

    return lines.length * lineHeight;
  };

  // Helper function to add section header
  const addSectionHeader = (title: string) => {
    checkNewPage(15);

    // Add background color for section headers
    pdf.setFillColor(79, 70, 229); // Purple background
    pdf.rect(margin, currentY - 3, contentWidth, 10, 'F');

    pdf.setTextColor(255, 255, 255); // White text
    pdf.setFontSize(12);
    pdf.setFont('helvetica', 'bold');

    pdf.text(title, margin + 3, currentY + 3);

    currentY += 12;
    pdf.setTextColor(0, 0, 0); // Reset to black text
  };

  // Helper function to add field
  const addField = (
    label: string,
    value: string | number | null | undefined
  ) => {
    if (!value || value === '') value = '--';

    checkNewPage(8);

    // Label
    pdf.setFontSize(9);
    pdf.setFont('helvetica', 'bold');
    pdf.setTextColor(100, 100, 100);
    pdf.text(label, margin, currentY);
    currentY += 4;

    // Value
    pdf.setFont('helvetica', 'normal');
    pdf.setTextColor(0, 0, 0);
    const valueLines = pdf.splitTextToSize(String(value), contentWidth);
    valueLines.forEach((line: string) => {
      pdf.text(line, margin, currentY);
      currentY += 3.5;
    });

    currentY += 2; // Space between fields
  };

  // Helper function to get procedure type display with icon
  const getProcedureTypeDisplay = (type: string) => {
    const typeKey = type as keyof typeof typeTranslations;
    return typeTranslations[typeKey] || type || t('edit.pdf.notSpecified');
  };

  const typeTranslations = {
    business_license: t('edit.pdf.procedureTypes.businessLicense'),
    permits_building_license: t('edit.pdf.procedureTypes.buildingLicense'),
  };

  // Document title
  pdf.setFontSize(18);
  pdf.setFont('helvetica', 'bold');
  pdf.setTextColor(79, 70, 229);
  pdf.text(t('edit.pdf.title'), margin, currentY);
  currentY += 8;

  // Procedure info
  pdf.setFontSize(14);
  pdf.setTextColor(0, 0, 0);
  pdf.text(`${t('edit.pdf.folio')}: ${procedure.folio}`, margin, currentY);
  currentY += 12;

  // Header info section
  addSectionHeader(t('edit.pdf.generalInfo'));

  addField(t('edit.pdf.fields.folio'), procedure.folio);
  addField(t('edit.pdf.fields.status'), procedure.status);
  addField(
    t('edit.pdf.fields.type'),
    getTranslatedProcedureType(procedure.procedure_type)
  );
  addField(
    t('edit.pdf.fields.created'),
    new Date(procedure.created_at).toLocaleDateString('es-MX')
  );
  addField(
    t('edit.pdf.fields.updated'),
    new Date(procedure.updated_at).toLocaleDateString('es-MX')
  );

  currentY += 5;

  // Section 1: Applicant Information
  const section1Fields = dynamicFields[0] || [];
  if (section1Fields.length > 0) {
    addSectionHeader(t('edit.sections.section1.title'));

    addField(
      t('edit.pdf.fields.applicantName'),
      procedure.official_applicant_name
    );

    section1Fields.forEach(field => {
      if (field.value && field.value !== '') {
        const label = field.label || field.name || `Campo ${field.id}`;
        const displayValue = getReadableValue(field);

        addField(label, displayValue);
      }
    });

    currentY += 5;
  }

  // Section 2: Establishment Information
  const section2Fields = dynamicFields[1] || [];
  if (section2Fields.length > 0) {
    addSectionHeader(t('edit.sections.section2.title'));

    addField(
      t('edit.pdf.fields.establishmentName'),
      procedure.establishment_name
    );
    addField(
      t('edit.pdf.fields.establishmentAddress'),
      procedure.establishment_address
    );
    addField(
      t('edit.pdf.fields.establishmentPhone'),
      procedure.establishment_phone
    );
    addField(
      t('edit.pdf.fields.establishmentArea'),
      procedure.establishment_area
    );

    section2Fields.forEach(field => {
      if (field.value && field.value !== '') {
        const label = field.label || field.name || `Campo ${field.id}`;
        const displayValue = getReadableValue(field);
        addField(label, displayValue);
      }
    });

    currentY += 5;
  }

  // Section 3: Business Information
  const section3Fields = dynamicFields[2] || [];
  if (section3Fields.length > 0) {
    addSectionHeader(t('edit.sections.section3.title'));

    // Only add procedure fields if they have actual values
    if (procedure.business_name && procedure.business_name !== '') {
      addField(t('edit.pdf.fields.businessName'), procedure.business_name);
    }
    if (procedure.business_sector && procedure.business_sector !== '') {
      addField(t('edit.pdf.fields.businessSector'), procedure.business_sector);
    }
    if (procedure.business_activity && procedure.business_activity !== '') {
      addField(
        t('edit.pdf.fields.businessActivity'),
        procedure.business_activity
      );
    }
    if (procedure.operating_hours && procedure.operating_hours !== '') {
      addField(t('edit.pdf.fields.operatingHours'), procedure.operating_hours);
    }
    if (procedure.employee_count && procedure.employee_count !== '') {
      addField(t('edit.pdf.fields.employeeCount'), procedure.employee_count);
    }

    // Filter out dynamic fields that might duplicate procedure data
    const filteredSection3Fields = section3Fields.filter(field => {
      if (!field.value || field.value === '') return false;

      const fieldName = (field.name || '').toLowerCase();

      // Skip fields that duplicate procedure data we already showed
      const skipFields = [
        'nombre_negocio',
        'nombre_del_negocio',
        'business_name',
        'giro_comercial',
        'business_sector',
        'actividad_del_negocio',
        'actividad',
        'business_activity',
        'horario_de_operacion',
        'horario_operacion',
        'operating_hours',
        'numero_empleados',
        'numero_de_empleados',
        'employee_count',
      ];

      return !skipFields.some(skip => fieldName.includes(skip));
    });

    // Add remaining dynamic fields
    filteredSection3Fields.forEach(field => {
      const label = field.label || field.name || `Campo ${field.id}`;
      const displayValue = getReadableValue(field);
      addField(label, displayValue);
    });

    currentY += 5;
  }

  // Section 4: Required Documents
  const section4Fields = dynamicFields[3] || [];
  if (section4Fields.length > 0) {
    addSectionHeader(t('edit.sections.section4.title'));

    section4Fields.forEach(field => {
      if (field.value && field.value !== '') {
        const label = field.label || field.name || `Campo ${field.id}`;
        let displayValue = field.value;

        // For file fields, extract and show only the filename
        if (field.field_type === 'file' || field.field_type === 'multifile') {
          if (typeof field.value === 'object' && field.value.filename) {
            // Extract just the filename from the path
            displayValue =
              field.value.filename.split('/').pop() || field.value.filename;
          } else if (
            typeof field.value === 'object' &&
            field.value.original_name
          ) {
            displayValue = field.value.original_name;
          } else if (typeof field.value === 'string') {
            // If it's a string, try to extract filename from various patterns
            if (field.value.includes('filename')) {
              // Extract filename from the object-like string
              const match = field.value.match(/'filename':\s*'([^']+)'/);
              if (match) {
                displayValue = match[1].split('/').pop() || match[1];
              }
            } else if (field.value.includes('original_name')) {
              // Extract original_name from the object-like string
              const match = field.value.match(/'original_name':\s*'([^']+)'/);
              if (match) {
                displayValue = match[1];
              }
            } else if (
              field.value.includes('.pdf') ||
              field.value.includes('.')
            ) {
              // If it looks like a filename, extract just the name part
              displayValue = field.value.split('/').pop() || field.value;
            }
          }
        }

        addField(label, displayValue);
      }
    });

    currentY += 5;
  }

  // Address information
  const addressParts = [
    procedure.street,
    procedure.exterior_number,
    procedure.interior_number && `Int. ${procedure.interior_number}`,
    procedure.neighborhood,
    procedure.municipality,
  ].filter(Boolean);

  if (addressParts.length > 0) {
    addSectionHeader(t('edit.pdf.addressInfo'));
    addField(t('edit.pdf.fields.address'), addressParts.join(', '));
    currentY += 5;
  }

  // Footer
  checkNewPage(20);
  currentY = pageHeight - 30;
  pdf.setFontSize(8);
  pdf.setTextColor(100, 100, 100);
  pdf.text(
    `${t('edit.pdf.generatedOn')}: ${new Date().toLocaleDateString('es-MX')} ${new Date().toLocaleTimeString('es-MX')}`,
    margin,
    currentY
  );

  pdf.text(
    `${t('edit.pdf.page')} ${pdf.getNumberOfPages()}`,
    pageWidth - margin - 20,
    currentY
  );

  // Save the PDF
  const fileName = `tramite_${procedure.folio}_${new Date().toISOString().split('T')[0]}.pdf`;
  pdf.save(fileName);
}

export async function generateAnalyticsPDF(
  analytics: AnalyticsData,
  t: any,
  selectedPeriod: string
): Promise<void> {
  const pdf = new jsPDF('p', 'mm', 'a4');
  const pageWidth = pdf.internal.pageSize.getWidth();
  const pageHeight = pdf.internal.pageSize.getHeight();
  const margin = 20;
  const contentWidth = pageWidth - margin * 2;
  let currentY = margin;

  // Helper function to check if we need a new page
  const checkNewPage = (spaceNeeded: number = 20) => {
    if (currentY + spaceNeeded > pageHeight - 30) {
      pdf.addPage();
      currentY = margin;
      return true;
    }
    return false;
  };

  // Helper function to add section title
  const addSectionTitle = (title: string) => {
    checkNewPage(30);
    pdf.setFontSize(16);
    pdf.setFont('helvetica', 'bold');
    pdf.setTextColor(30, 41, 59); // slate-800
    pdf.text(title, margin, currentY);
    currentY += 10;

    // Add underline
    pdf.setDrawColor(59, 130, 246); // blue-500
    pdf.setLineWidth(0.5);
    pdf.line(margin, currentY, margin + contentWidth, currentY);
    currentY += 15;
  };

  // Header
  pdf.setFontSize(24);
  pdf.setFont('helvetica', 'bold');
  pdf.setTextColor(30, 41, 59);
  pdf.text(t('analytics.title'), margin, currentY);
  currentY += 10;

  pdf.setFontSize(12);
  pdf.setFont('helvetica', 'normal');
  pdf.setTextColor(100, 116, 139);
  pdf.text(t('analytics.subtitle'), margin, currentY);
  currentY += 5;

  // Period and generation date
  pdf.setFontSize(10);
  pdf.setTextColor(156, 163, 175);
  const periodText = t(`analytics.filters.periods.${selectedPeriod}`);
  pdf.text(`${t('analytics.filters.period')}: ${periodText}`, margin, currentY);
  pdf.text(
    `${t('analytics.lastUpdate')}: ${new Date().toLocaleDateString()}`,
    pageWidth - margin - 50,
    currentY
  );
  currentY += 20;

  // KPIs Section
  addSectionTitle(t('analytics.kpis.title'));

  const kpiData = [
    {
      label: t('analytics.kpis.averageTime'),
      value: `${analytics.kpis.tiempo_promedio} ${t('analytics.kpis.units.days')}`,
      color: [59, 130, 246] as [number, number, number], // blue-500
    },
    {
      label: t('analytics.kpis.efficiency'),
      value: `${analytics.kpis.eficiencia}${t('analytics.kpis.units.percentage')}`,
      color: [34, 197, 94] as [number, number, number], // green-500
    },
    {
      label: t('analytics.kpis.totalProcessed'),
      value: analytics.kpis.total_procesados.toLocaleString(),
      color: [168, 85, 247] as [number, number, number], // purple-500
    },
    {
      label: t('analytics.kpis.satisfaction'),
      value: `${analytics.kpis.satisfaccion}${t('analytics.kpis.units.rating')}`,
      color: [234, 179, 8] as [number, number, number], // yellow-500
    },
  ];

  // Draw KPI boxes
  const boxWidth = (contentWidth - 15) / 2; // 2 columns with gap
  const boxHeight = 25;

  kpiData.forEach((kpi, index) => {
    const col = index % 2;
    const row = Math.floor(index / 2);
    const x = margin + col * (boxWidth + 5);
    const y = currentY + row * (boxHeight + 10);

    // KPI box background
    pdf.setFillColor(248, 250, 252); // slate-50
    pdf.setDrawColor(226, 232, 240); // slate-200
    pdf.rect(x, y, boxWidth, boxHeight, 'FD');

    // KPI label
    pdf.setFontSize(10);
    pdf.setFont('helvetica', 'normal');
    pdf.setTextColor(71, 85, 105); // slate-600
    pdf.text(kpi.label, x + 5, y + 8);

    // KPI value
    pdf.setFontSize(14);
    pdf.setFont('helvetica', 'bold');
    pdf.setTextColor(...kpi.color);
    pdf.text(kpi.value, x + 5, y + 18);
  });

  currentY += Math.ceil(kpiData.length / 2) * 35 + 15;

  // Status Distribution Section
  addSectionTitle(t('analytics.charts.statusDistribution'));

  analytics.distribucion_estados.forEach((item, index) => {
    checkNewPage(15);

    // Status name
    pdf.setFontSize(11);
    pdf.setFont('helvetica', 'normal');
    pdf.setTextColor(30, 41, 59);
    pdf.text(item.estado, margin, currentY);

    // Progress bar background
    const barWidth = 80;
    const barHeight = 4;
    const barX = margin + 60;
    const barY = currentY - 3;

    pdf.setFillColor(229, 231, 235); // gray-200
    pdf.rect(barX, barY, barWidth, barHeight, 'F');

    // Progress bar fill (convert color class to RGB)
    const fillWidth = (barWidth * item.porcentaje) / 100;
    let fillColor: [number, number, number] = [59, 130, 246]; // default blue
    if (item.color.includes('green')) fillColor = [34, 197, 94];
    else if (item.color.includes('yellow')) fillColor = [234, 179, 8];
    else if (item.color.includes('red')) fillColor = [239, 68, 68];
    else if (item.color.includes('gray')) fillColor = [107, 114, 128];

    pdf.setFillColor(...fillColor);
    pdf.rect(barX, barY, fillWidth, barHeight, 'F');

    // Percentage and count
    pdf.setFontSize(10);
    pdf.setTextColor(107, 114, 128);
    pdf.text(`${item.porcentaje}%`, barX + barWidth + 5, currentY);
    pdf.text(`(${item.cantidad})`, barX + barWidth + 20, currentY);

    currentY += 12;
  });

  currentY += 10;

  // Dependencies Performance Section
  addSectionTitle(t('analytics.performance.title'));

  // Table headers
  pdf.setFontSize(10);
  pdf.setFont('helvetica', 'bold');
  pdf.setTextColor(75, 85, 99);

  const colWidths = [50, 35, 30, 25, 30];
  const headers = [
    t('analytics.performance.columns.dependency'),
    t('analytics.performance.columns.processedProcedures'),
    t('analytics.performance.columns.averageTime'),
    t('analytics.performance.columns.efficiency'),
    t('analytics.performance.columns.status'),
  ];

  let tableX = margin;
  headers.forEach((header, index) => {
    pdf.text(header, tableX, currentY);
    tableX += colWidths[index];
  });

  currentY += 5;

  // Table separator line
  pdf.setDrawColor(229, 231, 235);
  pdf.setLineWidth(0.3);
  pdf.line(margin, currentY, margin + contentWidth, currentY);
  currentY += 8;

  // Table rows
  analytics.dependencias.forEach((dep, index) => {
    checkNewPage(12);

    pdf.setFont('helvetica', 'normal');
    pdf.setTextColor(30, 41, 59);

    tableX = margin;
    const rowData = [
      dep.nombre,
      dep.tramites_procesados.toLocaleString(),
      `${dep.tiempo_promedio} ${t('analytics.kpis.units.days')}`,
      `${dep.eficiencia}%`,
      getStatusText(dep.estado),
    ];

    rowData.forEach((data, colIndex) => {
      if (colIndex === 0) {
        pdf.setFontSize(9);
      } else {
        pdf.setFontSize(8);
      }

      const maxWidth = colWidths[colIndex] - 2;
      const lines = pdf.splitTextToSize(data.toString(), maxWidth);
      pdf.text(lines, tableX, currentY);
      tableX += colWidths[colIndex];
    });

    currentY += 10;
  });

  // Helper function for status text
  function getStatusText(estado: string): string {
    switch (estado) {
      case 'excellent':
        return t('analytics.performance.statusLevels.excellent');
      case 'good':
        return t('analytics.performance.statusLevels.good');
      case 'warning':
        return t('analytics.performance.statusLevels.warning');
      case 'poor':
        return t('analytics.performance.statusLevels.poor');
      default:
        return t('analytics.performance.statusLevels.na');
    }
  }

  currentY += 15;

  // Licensing Status Summary
  addSectionTitle(t('analytics.charts.municipalSummary'));

  const licensingData = [
    {
      label: t('analytics.statuses.consultations'),
      value: analytics.licensing_status.consultation,
    },
    {
      label: t('analytics.statuses.initiated'),
      value: analytics.licensing_status.initiated,
    },
    {
      label: t('analytics.statuses.underReview'),
      value: analytics.licensing_status.under_review,
    },
    {
      label: t('analytics.statuses.issued'),
      value: analytics.licensing_status.issued,
    },
  ];

  licensingData.forEach((item, index) => {
    const col = index % 2;
    const row = Math.floor(index / 2);
    const x = margin + col * (boxWidth + 5);
    const y = currentY + row * 20;

    pdf.setFontSize(10);
    pdf.setFont('helvetica', 'normal');
    pdf.setTextColor(107, 114, 128);
    pdf.text(item.label, x, y);

    pdf.setFontSize(16);
    pdf.setFont('helvetica', 'bold');
    pdf.setTextColor(30, 41, 59);
    pdf.text(item.value.toString(), x, y + 10);
  });

  currentY += 50;

  // Review Status Summary
  checkNewPage(50);
  addSectionTitle(t('analytics.charts.departmentalReviews'));

  const reviewData = [
    {
      label: t('analytics.statuses.approved'),
      value: analytics.review_status.approved,
    },
    {
      label: t('analytics.statuses.underReview'),
      value: analytics.review_status.under_review,
    },
    {
      label: t('analytics.statuses.corrected'),
      value: analytics.review_status.corrected,
    },
    {
      label: t('analytics.statuses.discarded'),
      value: analytics.review_status.discarded,
    },
  ];

  reviewData.forEach((item, index) => {
    const col = index % 2;
    const row = Math.floor(index / 2);
    const x = margin + col * (boxWidth + 5);
    const y = currentY + row * 20;

    pdf.setFontSize(10);
    pdf.setFont('helvetica', 'normal');
    pdf.setTextColor(107, 114, 128);
    pdf.text(item.label, x, y);

    pdf.setFontSize(16);
    pdf.setFont('helvetica', 'bold');
    pdf.setTextColor(30, 41, 59);
    pdf.text(item.value.toString(), x, y + 10);
  });

  // Footer on last page
  currentY = pageHeight - 30;
  pdf.setFontSize(8);
  pdf.setTextColor(156, 163, 175);
  pdf.text(
    `${t('analytics.generatedOn')}: ${new Date().toLocaleDateString()} ${new Date().toLocaleTimeString()}`,
    margin,
    currentY
  );

  pdf.text(
    `${t('analytics.page')} ${pdf.getNumberOfPages()}`,
    pageWidth - margin - 20,
    currentY
  );

  // Save the PDF
  const fileName = `analytics_${selectedPeriod}_${new Date().toISOString().split('T')[0]}.pdf`;
  pdf.save(fileName);
}
