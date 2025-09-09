import { CheckCircle, Clock, AlertCircle, X } from 'lucide-react';

export interface WorkflowStep {
  id: string;
  label: string;
  description: string;
  status: 'completed' | 'current' | 'pending' | 'skipped';
}

interface WorkflowIndicatorProps {
  procedure: any;
  t: any;
  workflowStatus?: any;
}

export function getProcedureStatusDetails(procedure: any) {
  const details = {
    status: procedure.status,
    director_approval: procedure.director_approval,
    sent_to_reviewers: procedure.sent_to_reviewers,
    step_one: procedure.step_one,
    step_two: procedure.step_two,
    step_three: procedure.step_three,
    step_four: procedure.step_four,
    window_license_generated: procedure.window_license_generated,
    folio: procedure.folio,
    procedure_type: procedure.procedure_type,
    created_at: procedure.created_at,
  };
  return details;
}

export function getWorkflowSteps(
  procedure: any,
  t: any,
  workflowStatus?: any
): WorkflowStep[] {
  getProcedureStatusDetails(procedure);

  const procedureType = procedure.procedure_type?.toLowerCase() || '';

  const isProcedureCompleted = () => {
    if (workflowStatus?.current_workflow_step === 'completed') {
      return true;
    }
    return procedure.status >= 7;
  };

  const isProcedureRejected = () => {
    if (workflowStatus?.current_workflow_step === 'rejected') {
      return true;
    }
    // Only status 3 is truly rejected
    return procedure.status === 3;
  };

  const isProcedurePrevention = () => {
    if (workflowStatus?.current_workflow_step === 'prevention') {
      return true;
    }
    // Only status 3 with prevention flag should be considered prevention
    // For now, we'll keep this as status 3, but this might need refinement
    return procedure.status === 3;
  };

  const getStepStatus = (stepConditions: {
    completed?: boolean;
    inProgress?: boolean;
    blocked?: boolean;
  }) => {
    if (isProcedureCompleted()) {
      return 'completed';
    }
    if (stepConditions.blocked) {
      return 'pending';
    }
    if (stepConditions.completed) {
      return 'completed';
    }
    if (stepConditions.inProgress) {
      return 'current';
    }
    return 'pending';
  };

  const isProcedureInProgress = () => {
    if (workflowStatus?.can_proceed_to_next_step !== undefined) {
      return workflowStatus.can_proceed_to_next_step;
    }
    return (
      procedure.sent_to_reviewers === 1 ||
      procedure.step_one === 1 ||
      procedure.step_two === 1 ||
      procedure.step_three === 1 ||
      procedure.step_four === 1
    );
  };

  const isStartStepCompleted = () => {
    const result = procedure.status >= 0;
    return result;
  };

  const isProcedureApproved = () => {
    if (workflowStatus?.current_workflow_step === 'aprobacion_completed') {
      return true;
    }
    return procedure.status === 2; // Status 2 = approved in backend
  };

  const isProcedureInReview = () => {
    return procedure.status === 1; // Status 1 = pending_review in backend
  };

  if (
    procedureType.includes('construccion') ||
    procedureType.includes('construction')
  ) {
    return [
      {
        id: 'submission',
        label: t('detail.progress.steps.construction.submission'),
        description: t('detail.progress.descriptions.construction.submission'),
        status: getStepStatus({
          completed: isStartStepCompleted(),
          blocked: isProcedureRejected(),
        }),
      },
      {
        id: 'technical_review',
        label: t('detail.progress.steps.construction.technicalReview'),
        description: t(
          'detail.progress.descriptions.construction.technicalReview'
        ),
        status: getStepStatus({
          completed: procedure.step_one === 1,
          inProgress: isProcedureInProgress() && !procedure.step_one,
          blocked: isProcedureRejected() || !isProcedureInProgress(),
        }),
      },
      {
        id: 'department_approval',
        label: t('detail.progress.steps.construction.departmentApproval'),
        description: t(
          'detail.progress.descriptions.construction.departmentApproval'
        ),
        status: getStepStatus({
          completed: procedure.step_two === 1 && procedure.step_three === 1,
          inProgress:
            procedure.step_one === 1 &&
            (procedure.step_two !== 1 || procedure.step_three !== 1),
          blocked: isProcedureRejected() || procedure.step_one !== 1,
        }),
      },
      {
        id: 'director_approval',
        label: t('detail.progress.steps.construction.directorApproval'),
        description: t(
          'detail.progress.descriptions.construction.directorApproval'
        ),
        status: getStepStatus({
          completed: procedure.director_approval === 1 || isProcedureApproved(),
          inProgress:
            procedure.step_two === 1 &&
            procedure.step_three === 1 &&
            procedure.director_approval !== 1,
          blocked:
            isProcedureRejected() ||
            procedure.step_two !== 1 ||
            procedure.step_three !== 1,
        }),
      },
      {
        id: 'license_generation',
        label: t('detail.progress.steps.construction.licenseGeneration'),
        description: t(
          'detail.progress.descriptions.construction.licenseGeneration'
        ),
        status: getStepStatus({
          completed:
            isProcedureCompleted() || procedure.window_license_generated === 1,
          inProgress:
            (procedure.director_approval === 1 || isProcedureApproved()) &&
            !isProcedureCompleted(),
          blocked: isProcedureRejected() || procedure.director_approval !== 1,
        }),
      },
    ];
  } else if (
    procedureType.includes('comercial') ||
    procedureType.includes('giro') ||
    procedureType.includes('negocio') ||
    procedureType.includes('business_license')
  ) {
    return [
      {
        id: 'inicio',
        label: t('workflow.states.inicio'),
        description: t('workflow.descriptions.inicio'),
        status: getStepStatus({
          completed: isStartStepCompleted(),
          blocked: isProcedureRejected(),
        }),
      },
      {
        id: 'revision',
        label: t('workflow.states.revision'),
        description: t('workflow.descriptions.revision'),
        status: getStepStatus({
          completed: procedure.status >= 2, // Completed when status is 2 (approved) or higher
          inProgress:
            procedure.status === 1 && procedure.sent_to_reviewers === 1, // In progress when status is 1 (pending_review)
          blocked: false, // Don't block this step unless explicitly rejected
        }),
      },
      {
        id: 'aprobacion',
        label: t('workflow.states.aprobacion'),
        description: t('workflow.descriptions.aprobacion'),
        status: getStepStatus({
          completed: procedure.status >= 7, // Only completed when license is issued (status 7+)
          inProgress: procedure.status === 2, // In progress/current when approved (status 2)
          blocked: procedure.status === 3, // Only blocked if explicitly rejected
        }),
      },
      {
        id: 'finalizacion',
        label: t('workflow.states.finalizacion'),
        description: t('workflow.descriptions.finalizacion'),
        status: getStepStatus({
          completed:
            procedure.status >= 7 || procedure.window_license_generated === 1, // Completed when license is issued
          inProgress: false, // Never in progress, only completed when license is issued
          blocked: procedure.status === 3, // Only blocked if explicitly rejected
        }),
      },
    ];
  } else if (
    procedureType.includes('refrendo') ||
    procedureType.includes('renewal')
  ) {
    return [
      {
        id: 'submission',
        label: t('detail.progress.steps.renewal.submission'),
        description: t('detail.progress.descriptions.renewal.submission'),
        status: getStepStatus({
          completed: isStartStepCompleted(),
          blocked: isProcedureRejected(),
        }),
      },
      {
        id: 'verification',
        label: t('detail.progress.steps.renewal.verification'),
        description: t('detail.progress.descriptions.renewal.verification'),
        status: getStepStatus({
          completed: procedure.step_one === 1,
          inProgress: isProcedureInProgress() && !procedure.step_one,
          blocked: isProcedureRejected() || !isProcedureInProgress(),
        }),
      },
      {
        id: 'approval',
        label: t('detail.progress.steps.renewal.approval'),
        description: t('detail.progress.descriptions.renewal.approval'),
        status: getStepStatus({
          completed: procedure.director_approval === 1 || isProcedureApproved(),
          inProgress:
            procedure.step_one === 1 && procedure.director_approval !== 1,
          blocked: isProcedureRejected() || procedure.step_one !== 1,
        }),
      },
      {
        id: 'issuance',
        label: t('detail.progress.steps.renewal.issuance'),
        description: t('detail.progress.descriptions.renewal.issuance'),
        status: getStepStatus({
          completed:
            isProcedureCompleted() || procedure.window_license_generated === 1,
          inProgress:
            (procedure.director_approval === 1 || isProcedureApproved()) &&
            !isProcedureCompleted(),
          blocked: isProcedureRejected() || procedure.director_approval !== 1,
        }),
      },
    ];
  } else {
    return [
      {
        id: 'inicio',
        label: t('workflow.states.inicio'),
        description: t('workflow.descriptions.inicio'),
        status: getStepStatus({
          completed: isStartStepCompleted(),
          blocked: isProcedureRejected(),
        }),
      },
      {
        id: 'revision',
        label: t('workflow.states.revision'),
        description: t('workflow.descriptions.revision'),
        status: getStepStatus({
          completed: procedure.step_one === 1, // Only completed when step_one is 1
          inProgress:
            procedure.sent_to_reviewers === 1 && procedure.step_one !== 1, // In progress when sent to reviewers but not yet completed
          blocked: isProcedureRejected() || isProcedurePrevention(),
        }),
      },
      {
        id: 'aprobacion',
        label: t('workflow.states.aprobacion'),
        description: t('workflow.descriptions.aprobacion'),
        status: getStepStatus({
          completed: procedure.director_approval === 1 || isProcedureApproved(),
          inProgress:
            procedure.step_one === 1 && procedure.director_approval !== 1, // Only in progress after step_one is completed
          blocked:
            isProcedureRejected() ||
            isProcedurePrevention() ||
            procedure.step_one !== 1, // Blocked until step_one is completed
        }),
      },
      {
        id: 'finalizacion',
        label: t('workflow.states.finalizacion'),
        description: t('workflow.descriptions.finalizacion'),
        status: getStepStatus({
          completed:
            isProcedureCompleted() || procedure.window_license_generated === 1,
          inProgress:
            (procedure.director_approval === 1 || isProcedureApproved()) &&
            !isProcedureCompleted(),
          blocked: isProcedureRejected() || procedure.director_approval !== 1,
        }),
      },
    ];
  }
}

export function WorkflowIndicator({
  procedure,
  t,
  workflowStatus,
}: WorkflowIndicatorProps) {
  const steps = getWorkflowSteps(procedure, t, workflowStatus);

  const currentStepIndex = steps.findIndex(step => step.status === 'current');
  const activeStepIndex =
    currentStepIndex >= 0
      ? currentStepIndex
      : steps.findIndex(step => step.status !== 'completed');

  const isRejected = procedure.status === 3; // Status 3 = rejected
  const isPrevention = procedure.status === 3; // Prevention also uses status 3
  const isCompleted = procedure.status >= 7;

  const getProgressBarColor = () => {
    if (isRejected) return 'bg-red-500';
    if (isPrevention) return 'bg-yellow-500';
    if (procedure.status === 2) return 'bg-green-500'; // Approved
    if (isCompleted) return 'bg-green-500';
    return 'bg-blue-500';
  };

  const getStatusMessage = () => {
    if (isRejected)
      return {
        text: t('workflow.statusMessages.rejected'),
        color: 'text-red-600',
      };
    if (isPrevention)
      return {
        text: t('workflow.statusMessages.prevention'),
        color: 'text-yellow-600',
      };
    if (procedure.status === 2)
      return {
        text: t('workflow.statusMessages.approvedPending'),
        color: 'text-green-600',
      };
    if (isCompleted)
      return {
        text: t('workflow.statusMessages.completed'),
        color: 'text-green-600',
      };
    return null;
  };

  const statusMessage = getStatusMessage();

  return (
    <div className="w-full">
      {statusMessage && (
        <div className="mb-4 p-3 rounded-lg bg-gray-50 border">
          <div
            className={`text-sm font-medium ${statusMessage.color} text-center`}
          >
            {statusMessage.text}
          </div>
        </div>
      )}

      <div className="relative flex items-center justify-between mb-8">
        <div
          className="absolute top-1/2 left-0 right-0 h-1 bg-gray-200 transform -translate-y-1/2 z-0"
          style={{ left: '1rem', right: '1rem' }}
        />
        <div
          className={`absolute top-1/2 h-1 transform -translate-y-1/2 transition-all duration-300 z-0 ${getProgressBarColor()}`}
          style={{
            left: '1rem',
            width:
              steps.length > 1
                ? isCompleted
                  ? `calc(100% - 2rem)`
                  : (() => {
                      const completedSteps = steps.filter(
                        s => s.status === 'completed'
                      ).length;
                      const currentSteps = steps.filter(
                        s => s.status === 'current'
                      ).length;

                      // For approved procedures (status 2), fill until "Aprobación" step
                      if (procedure.status === 2) {
                        const aprovacionIndex = steps.findIndex(
                          s => s.id === 'aprobacion'
                        );
                        if (aprovacionIndex >= 0) {
                          return `calc(${(aprovacionIndex / (steps.length - 1)) * 100}% - 2rem)`;
                        }
                      }

                      // Default calculation
                      return `calc(${((completedSteps + (currentSteps > 0 ? 0.5 : 0)) / (steps.length - 1)) * 100}% - 2rem)`;
                    })()
                : '0%',
          }}
        />
        {steps.map((step, i) => (
          <div
            key={step.id}
            className="flex flex-col items-center relative z-10 flex-1"
          >
            <div
              className={`w-10 h-10 rounded-full flex items-center justify-center text-sm font-medium mb-2 transition-all duration-300 ${
                step.status === 'completed'
                  ? 'bg-green-500 text-white shadow-md'
                  : step.status === 'current'
                    ? isRejected
                      ? 'bg-red-500 text-white shadow-md ring-4 ring-red-200'
                      : isPrevention
                        ? 'bg-yellow-500 text-white shadow-md ring-4 ring-yellow-200'
                        : 'bg-blue-500 text-white shadow-md ring-4 ring-blue-200'
                    : 'bg-gray-200 text-gray-600'
              }`}
              title={step.description}
            >
              {step.status === 'completed' ? (
                <CheckCircle size={16} />
              ) : step.status === 'current' ? (
                isRejected ? (
                  <X size={16} />
                ) : isPrevention ? (
                  <AlertCircle size={16} />
                ) : (
                  <Clock size={16} />
                )
              ) : (
                i + 1
              )}
            </div>
          </div>
        ))}
      </div>
      <div className="flex justify-between items-start">
        {steps.map((step, i) => (
          <div key={step.id} className="flex-1 text-center px-1">
            <div
              className={`text-xs font-medium mb-1 ${
                step.status === 'completed'
                  ? 'text-green-600'
                  : step.status === 'current'
                    ? isRejected
                      ? 'text-red-600'
                      : isPrevention
                        ? 'text-yellow-600'
                        : 'text-blue-600'
                    : 'text-gray-500'
              }`}
            >
              {step.label}
            </div>
            <div className="text-xs text-gray-400 leading-tight">
              {step.description}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
