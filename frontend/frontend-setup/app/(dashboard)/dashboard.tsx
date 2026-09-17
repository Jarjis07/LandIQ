
import React, { useEffect, useState } from "react";
import { useRouter } from "expo-router";
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
  DEMO_METRICS,
  getAuditEvents,
  getDashboardMetrics,
} from "../../services/auditService";

import type {
  AuditEvent,
  DashboardMetrics,
} from "../../../types/audit";

export default function DashboardScreen() { 
    const router = useRouter();
  const [metrics, setMetrics] =
    useState<DashboardMetrics | null>(null);

  const [events, setEvents] = useState<AuditEvent[]>([]);
  const [loading, setLoading] = useState(true);
  const [demo, setDemo] = useState(false);

  useEffect(() => {
    async function loadDashboard() {
      try {
        const [metricData, auditData] = await Promise.all([
          getDashboardMetrics(),
          getAuditEvents(),
        ]);

        setMetrics(metricData);
        setEvents(auditData);
      } catch {
        setMetrics(DEMO_METRICS);
        setEvents(DEMO_AUDIT_EVENTS);
        setDemo(true);
      } finally {
        setLoading(false);
      }
    }

    loadDashboard();
  }, []);

  if (loading) {
    return (
      <View style={styles.loading}>
        <ActivityIndicator size="large" color="#176B56" />
        <Text style={styles.subtitle}>
          Loading dashboard...
        </Text>
      </View>
    );
  }

  if (!metrics) {
    return (
      <View style={styles.loading}>
        <Text>Unable to load dashboard.</Text>
      </View>
    );
  }

  const cards = [
    ["Digitized Records", metrics.total_records],
    ["Documents Processed", metrics.documents_processed],
    ["Needs Verification", metrics.requiring_verification],
    ["Validation Conflicts", metrics.validation_conflicts],
    ["Verified Records", metrics.verified_records],
    ["Average Confidence", `${metrics.average_confidence}%`],
  ];

  return (
    <ScrollView style={styles.screen}>
      <View style={styles.container}>
        <Text style={styles.title}>LandIQ Dashboard</Text>

        <Text style={styles.subtitle}>
          Land record digitization and validation overview.
        </Text>

        {demo && (
          <View style={styles.notice}>
            <Text style={styles.noticeText}>
              DEMO MODE — Metrics and activity are sample data.
              Replace with live API data when available.
            </Text>
          </View>
        )}

        <View style={styles.grid}>
          {cards.map(([label, value]) => (
            <View key={String(label)} style={styles.metricCard}>
              <Text style={styles.metricValue}>
                {String(value)}
              </Text>

              <Text style={styles.metricLabel}>
                {String(label)}
              </Text>
            </View>
          ))}
        </View>

               <Pressable
          style={styles.auditButton}
          onPress={() => router.push("/(dashboard)/audit")}
        >
          <Text style={styles.auditButtonText}>Open Audit Trail</Text>
        </Pressable>

        <Text style={styles.sectionTitle}>
          Recent Activity
        </Text>
        {events.length === 0 ? (
          <View style={styles.activityCard}>
            <Text style={styles.subtitle}>
              No recent activity.
            </Text>
          </View>
        ) : (
          events.slice(0, 5).map((event) => (
            <View key={event.id} style={styles.activityCard}>
              <Text style={styles.activityTitle}>
                {event.action}
              </Text>

              <Text style={styles.activityDescription}>
                {event.description}
              </Text>

              <Text style={styles.subtitle}>
                {event.user} · {event.role}
              </Text>

              <Text style={styles.subtitle}>
                {new Date(event.timestamp).toLocaleString()}
              </Text>
            </View>
          ))
        )}
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  screen: {
    flex: 1,
    backgroundColor: "#F4F6F8",
  },
  container: {
    width: "100%",
    maxWidth: 1100,
    alignSelf: "center",
    padding: 16,
    gap: 16,
  },
  loading: {
    flex: 1,
    minHeight: 300,
    alignItems: "center",
    justifyContent: "center",
    gap: 12,
    backgroundColor: "#F4F6F8",
  },
  title: {
    fontSize: 26,
    fontWeight: "700",
    color: "#172B4D",
  },
  subtitle: {
    color: "#64748B",
    fontSize: 12,
    lineHeight: 18,
  },
  notice: {
    backgroundColor: "#FFF4D6",
    padding: 12,
    borderRadius: 8,
  },
  noticeText: {
    color: "#805A00",
    fontSize: 13,
    lineHeight: 20,
  },
  grid: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 12,
  },
  metricCard: {
    flexGrow: 1,
    flexBasis: 145,
    minHeight: 110,
    backgroundColor: "#FFFFFF",
    borderWidth: 1,
    borderColor: "#E2E8F0",
    borderRadius: 10,
    padding: 16,
    justifyContent: "center",
    gap: 8,
  },
  metricValue: {
    fontSize: 26,
    fontWeight: "700",
    color: "#176B56",
  },
  metricLabel: {
    fontSize: 12,
    color: "#64748B",
  },
  sectionTitle: {
    fontSize: 19,
    fontWeight: "700",
    color: "#172B4D",
  },
  activityCard: {
    backgroundColor: "#FFFFFF",
    borderWidth: 1,
    borderColor: "#E2E8F0",
    borderRadius: 10,
    padding: 14,
    gap: 6,
  },
  activityTitle: {
    fontSize: 15,
    fontWeight: "700",
    color: "#172B4D",
  },
  activityDescription: {
    fontSize: 13,
    color: "#334155",
  },
    auditButton: {
    backgroundColor: "#176B56",
    padding: 12,
    borderRadius: 8,
    alignItems: "center",
  },
  auditButtonText: {
    color: "#FFFFFF",
    fontSize: 14,
    fontWeight: "600",
  },
});