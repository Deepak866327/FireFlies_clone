import PlaceholderCard from "@/components/PlaceholderCard";

const TEAM_FEATURES = [
  { title: "Invite Team Members", description: "Bring your teammates into your workspace." },
  { title: "Shared Workspaces", description: "Organize meetings by team or project." },
  { title: "Meeting Sharing", description: "Share a meeting's notes with specific people." },
  { title: "Permissions", description: "Control who can view or edit meeting notes." },
  { title: "Comments", description: "Discuss meeting notes with your team." },
  { title: "Real-time Collaboration", description: "Edit notes together, live." },
];

export default function TeamPage() {
  return (
    <div className="mt-6">
      <h1 className="text-xl font-semibold text-gray-900">Team Collaboration</h1>
      <p className="mt-1 text-sm text-gray-500">
        Work on meeting notes together with your team.
      </p>

      <div className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {TEAM_FEATURES.map((feature) => (
          <PlaceholderCard
            key={feature.title}
            title={feature.title}
            description={feature.description}
          />
        ))}
      </div>
    </div>
  );
}
