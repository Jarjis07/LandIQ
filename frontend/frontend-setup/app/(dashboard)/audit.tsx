
import React, { useEffect, useState } from "react";
import {
  ActivityIndicator,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  View,
} from "react-native";

import {
  DEMO_AUDIT_EVENTS,
  getAuditEvents,
} from "../../services/auditService";

import type { AuditEvent } from "../../../types/audit";

export default function AuditScreen() {
  const [events, setEvents] = useState<AuditEvent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  async function loadEvents() {
    setLoading(true);
    setError(false);

    try {
      const data = await getAuditEvents();
      setEvents(data);
    } catch {
      setEvents(DEMO_AUDIT_EVENTS);
      setError(true);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadEvents();
  }, []);

  return (
    <ScrollView style={styles.screen}>
      <View style={styles.container}>
        <Text style={styles.title}>Audit Trail</Text>

        <Text style={styles.subtitle}>
          Track actions, users, timestamps and record changes.
        </Text>

        <View style={styles.notice}>
          <Text style={styles.noticeText}>
            Audit history is read-only in this screen.
            Demo events are used when the API is unavailable.
          </Text>
        </View>

        <Pressable onPress={loadEvents} style={styles.button}>
          <Text style={styles.buttonText}>
            Refresh History
          </Text>
        </Pressable>

        {loading ? (
          <View style={styles.stateBox}>
            <ActivityIndicator size="large" color="#176B56" />
            <Text style={styles.subtitle}>
              Loading audit history...
            </Text>
          </View>
        ) : (
          <>
            {error && (
              <Text style={styles.warning}>
                API unavailable. Showing demo audit events.
              </Text>
            )}

            {events.length === 0 ? (
              <View style={styles.stateBox}>
                <Text style={styles.subtitle}>
                  No audit events found.
                </Text>
              </View>
            ) : (
              events.map((event) => (
                <View key={event.id} style={styles.card}>
                  <View style={styles.header}>
                    <Text style={styles.action}>
                      {event.action}
                    </Text>

                    <Text style={styles.id}>{event.id}</Text>
                  </View>

                  <Text style={styles.description}>
                    {event.description}
                  </Text>

                  <Text style={styles.meta}>
                    {event.user} · {event.role}
                  </Text>

                  <Text style={styles.meta}>
                    {new Date(event.timestamp).toLocaleString()}
                  </Text>

                  <View style={styles.divider} />

                  <Detail
                    label="Entity"
                    value={`${event.entity_type} / ${event.entity_id}`}
                  />

                  {event.field && (
                    <Detail label="Field" value={event.field} />
                  )}

                  {event.old_value != null && (
                    <Detail
                      label="Old value"
                      value={event.old_value}
                    />
                  )}

                  {event.new_value != null && (
                    <Detail
                      label="New value"
                      value={event.new_value}
                    />
                  )}

                  {event.reason && (
                    <Detail label="Reason" value={event.reason} />
                  )}
                </View>
              ))
            )}
          </>
        )}
      </View>
    </ScrollView>
  );
}

function Detail({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
  return (
    <View style={styles.detail}>
      <Text style={styles.detailLabel}>{label}</Text>
      <Text style={styles.detailValue}>{value}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  screen: {
    flex: 1,
    backgroundColor: "#F4F6F8",
  },
  container: {
    width: "100%",
    maxWidth: 1000,
    alignSelf: "center",
    padding: 16,
    gap: 14,
  },
  title: {
    fontSize: 26,
    fontWeight: "700",
    color: "#172B4D",
  },
  subtitle: {
    fontSize: 14,
    color: "#64748B",
    lineHeight: 21,
  },
  notice: {
    backgroundColor: "#E8F1FA",
    padding: 12,
    borderRadius: 8,
  },
  noticeText: {
    fontSize: 13,
    color: "#24527A",
    lineHeight: 20,
  },
  button: {
    backgroundColor: "#176B56",
    padding: 12,
    borderRadius: 6,
    alignSelf: "flex-start",
  },
  buttonText: {
    color: "#FFFFFF",
    fontWeight: "600",
  },
  warning: {
    color: "#92400E",
    backgroundColor: "#FEF3C7",
    padding: 10,
    borderRadius: 6,
    fontSize: 13,
  },
  stateBox: {
    minHeight: 200,
    alignItems: "center",
    justifyContent: "center",
    gap: 12,
  },
  card: {
    backgroundColor: "#FFFFFF",
    borderWidth: 1,
    borderColor: "#E2E8F0",
    borderRadius: 10,
    padding: 16,
    gap: 10,
  },
  header: {
    flexDirection: "row",
    justifyContent: "space-between",
    flexWrap: "wrap",
    gap: 8,
  },
  action: {
    fontSize: 16,
    fontWeight: "700",
    color: "#176B56",
  },
  id: {
    color: "#64748B",
    fontSize: 12,
  },
  description: {
    color: "#172B4D",
    fontSize: 14,
  },
  meta: {
    color: "#64748B",
    fontSize: 12,
  },
  divider: {
    height: 1,
    backgroundColor: "#E2E8F0",
    marginVertical: 4,
  },
  detail: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 8,
  },
  detailLabel: {
    width: 95,
    color: "#64748B",
    fontSize: 12,
  },
  detailValue: {
    flex: 1,
    color: "#172B4D",
    fontSize: 13,
  },
});