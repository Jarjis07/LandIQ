
import { Stack } from "expo-router";

export default function DashboardLayout() {
  return (
    <Stack
      screenOptions={{
        headerShown: true,
        headerStyle: {
          backgroundColor: "#FFFFFF",
        },
        headerTintColor: "#172B4D",
        headerTitleStyle: {
          fontWeight: "600",
        },
        contentStyle: {
          backgroundColor: "#F4F6F8",
        },
      }}
    >
      <Stack.Screen
        name="dashboard"
        options={{
          title: "LandIQ Dashboard",
        }}
      />

      <Stack.Screen
        name="map"
        options={{
          title: "Property Map",
        }}
      />

      <Stack.Screen
        name="audit"
        options={{
          title: "Audit Trail",
        }}
      />

      <Stack.Screen
        name="documents"
        options={{
          title: "Documents",
        }}
      />

      <Stack.Screen
        name="search"
        options={{
          title: "Search Records",
        }}
      />

      <Stack.Screen
        name="verification"
        options={{
          title: "Verification",
        }}
      />
    </Stack>
  );
}