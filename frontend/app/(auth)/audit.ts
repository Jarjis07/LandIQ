
export type AuditAction =
  | "Document Upload"
  | "OCR Processing"
  | "Extraction"
  | "Validation"
  | "Field Correction"
  | "Verification"
  | "Record Update"
  | "Record Access";

export interface AuditEvent {
  id: string;
  action: AuditAction;
  user: string;
  role: string;
  timestamp: string;
  entity_type: string;
  entity_id: string;
  field?: string | null;
  old_value?: string | null;
  new_value?: string | null;
  reason?: string | null;
  description: string;
}

export interface DashboardMetrics {
  total_records: number;
  documents_processed: number;
  requiring_verification: number;
  validation_conflicts: number;
  verified_records: number;
  average_confidence: number;
}