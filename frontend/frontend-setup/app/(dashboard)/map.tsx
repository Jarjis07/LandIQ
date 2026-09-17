
import React, { useState } from "react";
import {
  ActivityIndicator,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  View,
} from "react-native";

const DEMO_PROPERTY = {
  id: "DEMO-PROP-001",
  name: "Sample Land Parcel",
  owner: "Demo Property Owner",
  village: "Demo Village",
  district: "Demo District",
  state: "Demo State",
  surveyNumber: "DEMO-123",
  area: "1500 sq.ft",
  latitude: 20.5937,
  longitude: 78.9629,
};

export default function MapScreen() {
  const [loading, setLoading] = useState(false);
  const [hasLocation, setHasLocation] = useState(true);
  const [error, setError] = useState(false);

  const property = DEMO_PROPERTY;

  const reloadMap = () => {
    setLoading(true);
    setError(false);
    setHasLocation(true);

    setTimeout(() => {
      setLoading(false);
    }, 700);
  };

  return (
    <ScrollView style={styles.screen}>
      <View style={styles.container}>
        <Text style={styles.title}>Property Map</Text>

        <Text style={styles.subtitle}>
          Approximate property location
        </Text>

        <View style={styles.notice}>
          <Text style={styles.noticeText}>
            DEMO DATA — Not an official cadastral map.
            Boundaries and coordinates are illustrative.
          </Text>
        </View>

        <View style={styles.card}>
          <Text style={styles.sectionTitle}>
            Location Preview
          </Text>

          {loading ? (
            <View style={styles.stateBox}>
              <ActivityIndicator
                size="large"
                color="#176B56"
              />
              <Text style={styles.muted}>
                Loading location...
              </Text>
            </View>
          ) : error ? (
            <View style={styles.stateBox}>
              <Text style={styles.error}>
                Unable to load location.
              </Text>

              <Pressable
                onPress={reloadMap}
                style={styles.button}
              >
                <Text style={styles.buttonText}>
                  Retry
                </Text>
              </Pressable>
            </View>
          ) : !hasLocation ? (
            <View style={styles.stateBox}>
              <Text style={styles.muted}>
                No location information is available.
              </Text>
            </View>
          ) : (
            <View style={styles.map}>
              <View style={styles.roadHorizontal} />
              <View style={styles.roadVertical} />

              <View style={styles.parcel}>
                <View style={styles.parcelInner}>
                  <Text style={styles.parcelLabel}>
                    DEMO PARCEL
                  </Text>
                </View>
              </View>

              <View style={styles.marker}>
                <View style={styles.markerDot} />
                <Text style={styles.markerText}>
                  Sample Property
                </Text>
              </View>

              <Text style={styles.mapFooter}>
                Illustrative location only
              </Text>
            </View>
          )}
        </View>

        <View style={styles.card}>
          <Text style={styles.sectionTitle}>
            Property Information
          </Text>

          <InfoRow label="Property ID" value={property.id} />
          <InfoRow
            label="Survey Number"
            value={property.surveyNumber}
          />
          <InfoRow label="Owner" value={property.owner} />
          <InfoRow label="Area" value={property.area} />
          <InfoRow label="Village" value={property.village} />
          <InfoRow label="District" value={property.district} />
          <InfoRow label="State" value={property.state} />

          <View style={styles.divider} />

          <Text style={styles.sectionTitle}>
            Approximate Coordinates
          </Text>

          <InfoRow
            label="Latitude"
            value={property.latitude.toFixed(4)}
          />

          <InfoRow
            label="Longitude"
            value={property.longitude.toFixed(4)}
          />
        </View>

        <View style={styles.actions}>
          <Pressable
            onPress={() => {
              setHasLocation(false);
              setError(false);
            }}
            style={styles.secondaryButton}
          >
            <Text style={styles.secondaryButtonText}>
              Test No Location
            </Text>
          </Pressable>

          <Pressable
            onPress={() => {
              setError(true);
              setHasLocation(false);
            }}
            style={styles.secondaryButton}
          >
            <Text style={styles.secondaryButtonText}>
              Test Error
            </Text>
          </Pressable>

          <Pressable
            onPress={reloadMap}
            style={styles.secondaryButton}
          >
            <Text style={styles.secondaryButtonText}>
              Reload Map
            </Text>
          </Pressable>
        </View>
      </View>
    </ScrollView>
  );
}

function InfoRow({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
  return (
    <View style={styles.infoRow}>
      <Text style={styles.infoLabel}>{label}</Text>
      <Text style={styles.infoValue}>{value}</Text>
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
    gap: 16,
  },
  title: {
    fontSize: 26,
    fontWeight: "700",
    color: "#172B4D",
  },
  subtitle: {
    fontSize: 14,
    color: "#64748B",
  },
  notice: {
    backgroundColor: "#FFF4D6",
    borderRadius: 8,
    padding: 12,
  },
  noticeText: {
    color: "#805A00",
    fontSize: 13,
    lineHeight: 20,
  },
  card: {
    backgroundColor: "#FFFFFF",
    borderRadius: 10,
    padding: 16,
    gap: 14,
    borderWidth: 1,
    borderColor: "#E2E8F0",
  },
  sectionTitle: {
    fontSize: 17,
    fontWeight: "700",
    color: "#172B4D",
  },
  map: {
    height: 300,
    backgroundColor: "#E8EFE8",
    borderRadius: 8,
    overflow: "hidden",
    alignItems: "center",
    justifyContent: "center",
  },
  roadHorizontal: {
    position: "absolute",
    width: "120%",
    height: 34,
    backgroundColor: "#D1D5DB",
    transform: [{ rotate: "-12deg" }],
  },
  roadVertical: {
    position: "absolute",
    width: 28,
    height: "120%",
    backgroundColor: "#D1D5DB",
    transform: [{ rotate: "22deg" }],
  },
  parcel: {
    width: 170,
    height: 130,
    backgroundColor: "#D5E8C8",
    borderWidth: 2,
    borderColor: "#66875A",
    transform: [{ rotate: "-8deg" }],
    alignItems: "center",
    justifyContent: "center",
  },
  parcelInner: {
    borderWidth: 1,
    borderColor: "#66875A",
    borderStyle: "dashed",
    padding: 12,
  },
  parcelLabel: {
    color: "#365A30",
    fontWeight: "700",
    fontSize: 11,
  },
  marker: {
    position: "absolute",
    alignItems: "center",
    top: "28%",
  },
  markerDot: {
    width: 22,
    height: 22,
    borderRadius: 11,
    backgroundColor: "#176B56",
    borderWidth: 4,
    borderColor: "#FFFFFF",
  },
  markerText: {
    marginTop: 5,
    backgroundColor: "#FFFFFF",
    color: "#172B4D",
    paddingHorizontal: 8,
    paddingVertical: 5,
    borderRadius: 5,
    fontWeight: "600",
    fontSize: 12,
  },
  mapFooter: {
    position: "absolute",
    bottom: 10,
    right: 10,
    color: "#475569",
    fontSize: 11,
  },
  stateBox: {
    height: 250,
    alignItems: "center",
    justifyContent: "center",
    gap: 12,
  },
  muted: {
    color: "#64748B",
    fontSize: 14,
  },
  error: {
    color: "#B91C1C",
    fontSize: 15,
  },
  button: {
    backgroundColor: "#176B56",
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 6,
  },
  buttonText: {
    color: "#FFFFFF",
    fontWeight: "600",
  },
  infoRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    gap: 12,
    paddingVertical: 8,
    borderBottomWidth: 1,
    borderBottomColor: "#F1F5F9",
  },
  infoLabel: {
    flex: 1,
    color: "#64748B",
    fontSize: 13,
  },
  infoValue: {
    flex: 1,
    color: "#172B4D",
    fontSize: 13,
    fontWeight: "600",
    textAlign: "right",
  },
  divider: {
    height: 1,
    backgroundColor: "#E2E8F0",
    marginVertical: 4,
  },
  actions: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 8,
  },
  secondaryButton: {
    borderWidth: 1,
    borderColor: "#CBD5E1",
    backgroundColor: "#FFFFFF",
    padding: 10,
    borderRadius: 6,
  },
  secondaryButtonText: {
    color: "#334155",
    fontSize: 12,
    fontWeight: "600",
  },
});