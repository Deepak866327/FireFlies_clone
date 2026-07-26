import Link from "next/link";

import { Meeting, TranscriptSegment } from "@/lib/types";

interface MeetingCardProps {
  meeting: Meeting & { segments?: TranscriptSegment[] };
}

function formatDate(dateString: string): string {
  return new Date(dateString).toLocaleDateString(undefined, {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
}

function formatDuration(segments?: TranscriptSegment[]): string | null {
  if (!segments || segments.length === 0) return null;
  const lastStart = segments[segments.length - 1].start_time ?? 0;
  const totalSeconds = Math.round(lastStart);
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  return `${minutes}m ${seconds.toString().padStart(2, "0")}s`;
}

export default function MeetingCard({ meeting }: MeetingCardProps) {
  const duration = formatDuration(meeting.segments);

  return (
    <Link
      href={`/meetings/${meeting.id}`}
      className="block rounded-lg border border-gray-200 bg-white p-4 shadow-sm transition hover:border-gray-300 hover:shadow-md"
    >
      <div className="flex items-start justify-between gap-4">
        <h3 className="text-base font-semibold text-gray-900">{meeting.title}</h3>
        {duration && (
          <span className="shrink-0 text-xs font-medium text-gray-500">{duration}</span>
        )}
      </div>

      <div className="mt-1 flex flex-wrap items-center gap-x-2 text-xs text-gray-500">
        <span>{formatDate(meeting.created_at)}</span>
        {meeting.participants && (
          <>
            <span>&middot;</span>
            <span className="truncate">{meeting.participants}</span>
          </>
        )}
      </div>

      {meeting.summary && (
        <p className="mt-2 line-clamp-2 text-sm text-gray-600">{meeting.summary}</p>
      )}
    </Link>
  );
}
