import React, { useCallback, useEffect, useState } from "react";
import {
  ActivityIndicator,
  FlatList,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
} from "react-native";

const API_URL = "http://127.0.0.1:8000/api/land-records/";

type LandRecord = {
  id: number;
  survey_number: string;
  owner_name: string;
  village: string;
  taluka: string;
  district: string;
  land_area: number;
  status: string;
};

type LandRecordForm = {
  survey_number: string;
  owner_name: string;
  village: string;
  taluka: string;
  district: string;
  land_area: string;
  status: string;
};

const emptyForm: LandRecordForm = {
  survey_number: "",
  owner_name: "",
  village: "",
  taluka: "",
  district: "",
  land_area: "",
  status: "Pending",
};

const fields: {
  key: keyof LandRecordForm;
  label: string;
  placeholder: string;
}[] = [
  {
    key: "survey_number",
    label: "Survey Number",
    placeholder: "Enter survey number",
  },
  {
    key: "owner_name",
    label: "Owner Name",
    placeholder: "Enter owner name",
  },
  { key: "village", label: "Village", placeholder: "Enter village" },
  { key: "taluka", label: "Taluka", placeholder: "Enter taluka" },
  { key: "district", label: "District", placeholder: "Enter district" },
  { key: "land_area", label: "Land Area", placeholder: "Enter land area" },
  {
    key: "status",
    label: "Status",
    placeholder: "Pending / Approved / Rejected",
  },
];

export default function DocumentsScreen() {
  const [records, setRecords] = useState<LandRecord[]>([]);
  const [form, setForm] = useState<LandRecordForm>(emptyForm);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);

  const loadRecords = useCallback(async () => {
    setLoading(true);

    try {
      const response = await fetch(API_URL);

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data = await response.json();
      setRecords(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error("Load records error:", error);
      window.alert(
        "Records load nahi hue. Check karo ki backend server chal raha hai."
      );
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadRecords();
  }, [loadRecords]);

  const updateField = (key: keyof LandRecordForm, value: string) => {
    setForm((previous) => ({ ...previous, [key]: value }));
  };

  const resetForm = () => {
    setForm(emptyForm);
    setEditingId(null);
  };

  const handleSave = async () => {
    if (
      !form.survey_number.trim() ||
      !form.owner_name.trim() ||
      !form.village.trim() ||
      !form.taluka.trim() ||
      !form.district.trim() ||
      !form.land_area.trim() ||
      !form.status.trim()
    ) {
      window.alert("Saare fields fill karo.");
      return;
    }

    const landArea = Number(form.land_area);

    if (!Number.isFinite(landArea) || landArea <= 0) {
      window.alert("Land Area mein positive number enter karo.");
      return;
    }

    const wasEditing = editingId !== null;

    const payload = {
      survey_number: form.survey_number.trim(),
      owner_name: form.owner_name.trim(),
      village: form.village.trim(),
      taluka: form.taluka.trim(),
      district: form.district.trim(),
      land_area: landArea,
      status: form.status.trim(),
    };

    setSaving(true);

    try {
      const url = wasEditing ? `${API_URL}${editingId}` : API_URL;
      const method = wasEditing ? "PUT" : "POST";

      const response = await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const message = await response.text();
        throw new Error(message || `Server error: ${response.status}`);
      }

      resetForm();
      await loadRecords();
      window.alert(wasEditing ? "Land record updated." : "Land record added.");
    } catch (error) {
      console.error("Save record error:", error);
      window.alert(
        error instanceof Error ? error.message : "Record save nahi hua."
      );
    } finally {
      setSaving(false);
    }
  };

  const handleEdit = (record: LandRecord) => {
    setEditingId(record.id);
    setForm({
      survey_number: record.survey_number ?? "",
      owner_name: record.owner_name ?? "",
      village: record.village ?? "",
      taluka: record.taluka ?? "",
      district: record.district ?? "",
      land_area: String(record.land_area ?? ""),
      status: record.status ?? "Pending",
    });
  };

  const handleDelete = async (record: LandRecord) => {
    const confirmed = window.confirm(
      `Survey Number: ${record.survey_number}\nYe record permanently delete hoga.`
    );

    if (!confirmed) {
      return;
    }

    try {
      const response = await fetch(`${API_URL}${record.id}`, {
        method: "DELETE",
      });

      if (!response.ok) {
        const message = await response.text();
        throw new Error(message || `Server error: ${response.status}`);
      }

      if (editingId === record.id) {
        resetForm();
      }

      await loadRecords();
      window.alert("Land record delete ho gaya.");
    } catch (error) {
      console.error("Delete record error:", error);
      window.alert(
        error instanceof Error ? error.message : "Record delete nahi hua."
      );
    }
  };

  const renderRecord = ({ item }: { item: LandRecord }) => (
    <View style={styles.recordCard}>
      <Text style={styles.recordTitle}>
        {item.survey_number} — {item.owner_name}
      </Text>

      <Text style={styles.recordText}>
        {item.village}, {item.taluka}, {item.district}
      </Text>

      <Text style={styles.recordText}>
        Land Area: {item.land_area} | Status: {item.status}
      </Text>

      <View style={styles.actionRow}>
        <TouchableOpacity
          style={[styles.actionButton, styles.editButton]}
          onPress={() => handleEdit(item)}
        >
          <Text style={styles.actionButtonText}>Edit</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.actionButton, styles.deleteButton]}
          onPress={() => handleDelete(item)}
        >
          <Text style={styles.actionButtonText}>Delete</Text>
        </TouchableOpacity>
      </View>
    </View>
  );

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.heading}>Land Records</Text>

      <View style={styles.formCard}>
        <Text style={styles.sectionTitle}>
          {editingId === null ? "Add Land Record" : `Edit Record #${editingId}`}
        </Text>

        {fields.map((field) => (
          <View key={field.key} style={styles.fieldContainer}>
            <Text style={styles.label}>{field.label}</Text>
            <TextInput
              style={styles.input}
              value={form[field.key]}
              onChangeText={(value) => updateField(field.key, value)}
              placeholder={field.placeholder}
              keyboardType={
                field.key === "land_area" ? "decimal-pad" : "default"
              }
              autoCapitalize="none"
            />
          </View>
        ))}

        <TouchableOpacity
          style={[styles.primaryButton, saving && styles.disabledButton]}
          onPress={handleSave}
          disabled={saving}
        >
          <Text style={styles.primaryButtonText}>
            {saving
              ? "Saving..."
              : editingId === null
              ? "Save Land Record"
              : "Update Land Record"}
          </Text>
        </TouchableOpacity>

        {editingId !== null && (
          <TouchableOpacity style={styles.cancelButton} onPress={resetForm}>
            <Text style={styles.cancelButtonText}>Cancel Edit</Text>
          </TouchableOpacity>
        )}
      </View>

      <View style={styles.listHeader}>
        <Text style={styles.sectionTitle}>Saved Records</Text>

        <TouchableOpacity
          style={styles.refreshButton}
          onPress={loadRecords}
        >
          <Text style={styles.refreshButtonText}>Refresh</Text>
        </TouchableOpacity>
      </View>

      {loading ? (
        <ActivityIndicator size="large" style={styles.loader} />
      ) : records.length === 0 ? (
        <Text style={styles.emptyText}>No land records found.</Text>
      ) : (
        <FlatList
          data={records}
          keyExtractor={(item) => String(item.id)}
          renderItem={renderRecord}
          scrollEnabled={false}
        />
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 16,
    paddingBottom: 32,
    backgroundColor: "#f5f7fb",
  },
  heading: {
    fontSize: 26,
    fontWeight: "700",
    marginBottom: 16,
    color: "#172033",
  },
  formCard: {
    backgroundColor: "#ffffff",
    padding: 16,
    borderRadius: 12,
    marginBottom: 24,
  },
  sectionTitle: {
    fontSize: 19,
    fontWeight: "700",
    color: "#172033",
  },
  fieldContainer: {
    marginTop: 12,
  },
  label: {
    fontSize: 14,
    fontWeight: "600",
    marginBottom: 6,
    color: "#344054",
  },
  input: {
    borderWidth: 1,
    borderColor: "#d0d5dd",
    borderRadius: 8,
    paddingHorizontal: 12,
    paddingVertical: 10,
    fontSize: 16,
    backgroundColor: "#ffffff",
  },
  primaryButton: {
    backgroundColor: "#2457c5",
    padding: 14,
    borderRadius: 8,
    alignItems: "center",
    marginTop: 18,
  },
  disabledButton: {
    opacity: 0.6,
  },
  primaryButtonText: {
    color: "#ffffff",
    fontWeight: "700",
    fontSize: 16,
  },
  cancelButton: {
    padding: 12,
    alignItems: "center",
    marginTop: 8,
  },
  cancelButtonText: {
    color: "#475467",
    fontWeight: "600",
  },
  listHeader: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    marginBottom: 12,
  },
  refreshButton: {
    backgroundColor: "#e7edfb",
    paddingHorizontal: 14,
    paddingVertical: 8,
    borderRadius: 8,
  },
  refreshButtonText: {
    color: "#2457c5",
    fontWeight: "700",
  },
  loader: {
    marginTop: 20,
  },
  emptyText: {
    color: "#667085",
    paddingVertical: 16,
  },
  recordCard: {
    backgroundColor: "#ffffff",
    borderRadius: 10,
    padding: 14,
    marginBottom: 10,
  },
  recordTitle: {
    fontSize: 16,
    fontWeight: "700",
    color: "#172033",
    marginBottom: 6,
  },
  recordText: {
    color: "#475467",
    marginBottom: 4,
  },
  actionRow: {
    flexDirection: "row",
    gap: 10,
    marginTop: 12,
  },
  actionButton: {
    paddingHorizontal: 18,
    paddingVertical: 9,
    borderRadius: 7,
  },
  editButton: {
    backgroundColor: "#e7edfb",
  },
  deleteButton: {
    backgroundColor: "#fee4e2",
  },
  actionButtonText: {
    fontWeight: "700",
    color: "#172033",
  },
});