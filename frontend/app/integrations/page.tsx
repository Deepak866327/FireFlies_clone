import PlaceholderCard from "@/components/PlaceholderCard";

const INTEGRATIONS = [
  { title: "Zoom", description: "Automatically record and transcribe Zoom meetings." },
  { title: "Google Meet", description: "Automatically record and transcribe Google Meet calls." },
  { title: "Microsoft Teams", description: "Automatically record and transcribe Teams meetings." },
  { title: "Google Calendar", description: "Sync upcoming meetings from your Google Calendar." },
  { title: "Outlook Calendar", description: "Sync upcoming meetings from your Outlook Calendar." },
  { title: "Salesforce CRM", description: "Push meeting notes into Salesforce records." },
  { title: "HubSpot CRM", description: "Push meeting notes into HubSpot records." },
];

export default function IntegrationsPage() {
  return (
    <div className="mt-6">
      <h1 className="text-xl font-semibold text-gray-900">Integrations</h1>
      <p className="mt-1 text-sm text-gray-500">
        Connect Meeting Notes with the tools your team already uses.
      </p>

      <div className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {INTEGRATIONS.map((integration) => (
          <PlaceholderCard
            key={integration.title}
            title={integration.title}
            description={integration.description}
          />
        ))}
      </div>
    </div>
  );
}
