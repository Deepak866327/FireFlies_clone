import { ActionItem, ChatMessage, ChatResponse, Meeting, MeetingDetail, Provider } from "./types";

export const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, options);

  if (!res.ok) {
    const body = await res.json().catch(() => null);
    throw new Error(body?.detail || `Request failed with status ${res.status}`);
  }

  if (res.status === 204) {
    return undefined as T;
  }

  return res.json();
}

export function getMeetings(params?: {
  search?: string;
  dateFilter?: string;
  sort?: string;
}): Promise<Meeting[]> {
  const query = new URLSearchParams();
  if (params?.search) query.set("search", params.search);
  if (params?.dateFilter) query.set("date_filter", params.dateFilter);
  if (params?.sort) query.set("sort", params.sort);

  const queryString = query.toString();
  return request<Meeting[]>(`/meetings${queryString ? `?${queryString}` : ""}`);
}

export function getMeeting(id: number): Promise<MeetingDetail> {
  return request<MeetingDetail>(`/meetings/${id}`);
}

export function createMeeting(data: {
  title: string;
  participants?: string;
  transcript_text?: string;
  file?: File;
}): Promise<MeetingDetail> {
  const formData = new FormData();
  formData.append("title", data.title);
  if (data.participants) formData.append("participants", data.participants);
  if (data.transcript_text) formData.append("transcript_text", data.transcript_text);
  if (data.file) formData.append("file", data.file);

  return request<MeetingDetail>("/meetings", {
    method: "POST",
    body: formData,
  });
}

export function updateMeeting(
  id: number,
  data: { title?: string; participants?: string }
): Promise<MeetingDetail> {
  return request<MeetingDetail>(`/meetings/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
}

export function deleteMeeting(id: number): Promise<void> {
  return request<void>(`/meetings/${id}`, { method: "DELETE" });
}

export function toggleActionItem(id: number, is_done: boolean): Promise<ActionItem> {
  return request<ActionItem>(`/action-items/${id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ is_done }),
  });
}

export function getExportUrl(meetingId: number, format: "pdf" | "md" | "txt"): string {
  return `${API_URL}/meetings/${meetingId}/export?format=${format}`;
}

export function askAboutMeeting(
  meetingId: number,
  data: { provider: Provider; question: string; history?: ChatMessage[] }
): Promise<ChatResponse> {
  return request<ChatResponse>(`/meetings/${meetingId}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
}
