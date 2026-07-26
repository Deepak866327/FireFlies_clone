import MeetingCard from "@/components/MeetingCard";
import { Meeting } from "@/lib/types";

interface MeetingListProps {
  meetings: Meeting[];
}

export default function MeetingList({ meetings }: MeetingListProps) {
  return (
    <div className="flex flex-col gap-3">
      {meetings.map((meeting) => (
        <MeetingCard key={meeting.id} meeting={meeting} />
      ))}
    </div>
  );
}
