export interface TranscriptSegment {
  id: number;
  meeting_id: number;
  order_index: number;
  speaker: string | null;
  start_time: number | null;
  text: string;
}

export interface ActionItem {
  id: number;
  meeting_id: number;
  segment_id: number | null;
  text: string;
  owner: string | null;
  is_done: boolean;
  created_at: string;
}

export interface Topic {
  id: number;
  meeting_id: number;
  label: string;
}

export interface Meeting {
  id: number;
  title: string;
  participants: string | null;
  created_at: string;
  summary: string | null;
  audio_url: string | null;
}

export interface MeetingDetail extends Meeting {
  segments: TranscriptSegment[];
  action_items: ActionItem[];
  topics: Topic[];
}

export type Provider = "openai" | "gemini";

export type ChatRole = "user" | "assistant";

export interface ChatMessage {
  role: ChatRole;
  content: string;
}

export interface ChatResponse {
  answer: string;
  provider: Provider;
}
