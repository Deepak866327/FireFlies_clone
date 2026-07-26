import PlaceholderCard from "@/components/PlaceholderCard";

const SETTINGS_SECTIONS = [
  { title: "Appearance", description: "Theme and display preferences." },
  { title: "Notifications", description: "Email and in-app notification preferences." },
  { title: "Language", description: "Choose your preferred language." },
  { title: "Integrations", description: "Manage connected apps." },
  { title: "Privacy", description: "Data and privacy controls." },
];

export default function SettingsPage() {
  return (
    <div className="mt-6">
      <h1 className="text-xl font-semibold text-gray-900">Settings</h1>
      <p className="mt-1 text-sm text-gray-500">
        Manage your account and workspace preferences.
      </p>

      <div className="mt-6 flex flex-col gap-4">
        {SETTINGS_SECTIONS.map((section) => (
          <PlaceholderCard
            key={section.title}
            title={section.title}
            description={section.description}
          />
        ))}
      </div>
    </div>
  );
}
