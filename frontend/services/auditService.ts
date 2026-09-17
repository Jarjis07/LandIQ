
import type {
  AuditEvent,
  DashboardMetrics,
} from "../types/audit";

const API_BASE_URL = "http://localhost:8000";

export const DEMO_AUDIT_EVENTS: AuditEvent[] = [
  {
    id: "AUD-001",
    action: "Field Correction",
    user: "Demo Verifier",
    role: "Verifier",
    timestamp: "2026-09-12T10:30:00Z",
    entity_type: "property",
    entity_id: "DEMO-PROP-001",
    field: "Area",
    old_value: "1200 sq.ft",
    new_value: "1500 sq.ft",
    reason: "Corrected after reviewing original document",
    description: "Property area corrected",
  },
  {
    id: "AUD-002",
    action: "Document Upload",
    user: "Demo Operator",
    role: "Operator",
    timestamp: "2026-09-12T09:45:00Z",
    entity_type: "document",
    entity_id: "DEMO-DOC-001",
    description: "Sample land record uploaded",
  },
  {
    id: "AUD-003",
    action: "Verification",
    user: "Demo Verifier",
    role: "Verifier",
    timestamp: "2026-09-12T09:15:00Z",
    entity_type: "property",
    entity_id: "DEMO-PROP-002",
    description: "Sample property verified",
  },
];

export const DEMO_METRICS: DashboardMetrics = {
  total_records: 248,
  documents_processed: 312,
  requiring_verification: 18,
  validation_conflicts: 7,
  verified_records: 203,
  average_confidence: 91.4,
};

export async function getAuditEvents(): Promise<AuditEvent[]> {
  const response = await fetch(`${API_BASE_URL}/api/audit`);

  if (!response.ok) {
    throw new Error("Unable to load audit history");
  }

  return response.json();
}

export async function createAuditEvent(
  event: Omit<AuditEvent, "id" | "timestamp">
): Promise<AuditEvent> {
  const response = await fetch(`${API_BASE_URL}/api/audit`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(event),
  });

  if (!response.ok) {
    throw new Error("Unable to create audit event");
  }

  return response.json();
}

export async function getDashboardMetrics(): Promise<DashboardMetrics> {
  const response = await fetch(
    `${API_BASE_URL}/api/dashboard/metrics`
  );

  if (!response.ok) {
    throw new Error("Unable to load dashboard metrics");
  }

  return response.json();
}