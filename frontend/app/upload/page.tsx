"use client";

import { useRouter } from "next/navigation";
import { FormEvent, useState } from "react";

import PlaceholderCard from "@/components/PlaceholderCard";
import { useToast } from "@/components/ui/Toast";
import { createMeeting } from "@/lib/api";

export default function UploadPage() {
  const router = useRouter();
  const { showToast } = useToast();

  const [title, setTitle] = useState("");
  const [participants, setParticipants] = useState("");
  const [transcriptText, setTranscriptText] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [mode, setMode] = useState<"paste" | "upload">("paste");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setError(null);

    if (!title.trim()) {
      setError("Please enter a meeting title.");
      return;
    }
    if (mode === "paste" && !transcriptText.trim()) {
      setError("Please paste a transcript.");
      return;
    }
    if (mode === "upload" && !file) {
      setError("Please choose a .txt transcript file.");
      return;
    }

    setSubmitting(true);
    try {
      const meeting = await createMeeting({
        title,
        participants: participants || undefined,
        transcript_text: mode === "paste" ? transcriptText : undefined,
        file: mode === "upload" ? file ?? undefined : undefined,
      });
      showToast("Meeting created.", "success");
      router.push(`/meetings/${meeting.id}`);
    } catch (err) {
      const message = err instanceof Error ? err.message : "Something went wrong.";
      setError(message);
      showToast(message, "error");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="mx-auto mt-6 max-w-2xl">
      <h1 className="text-xl font-semibold text-gray-900">New Meeting</h1>
      <p className="mt-1 text-sm text-gray-500">
        Paste a transcript or upload a .txt file to generate a summary, topics, and action items.
      </p>

      <div className="mt-4">
        <PlaceholderCard
          title="Automatic Speech-to-Text"
          description="In future versions meetings can be uploaded as audio/video and transcripts will be generated automatically."
        />
      </div>

      <form onSubmit={handleSubmit} className="mt-6 flex flex-col gap-4">
        <div>
          <label className="mb-1 block text-sm font-medium text-gray-700">Meeting Title</label>
          <input
            type="text"
            value={title}
            onChange={(event) => setTitle(event.target.value)}
            placeholder="e.g. Q3 Product Roadmap Planning"
            className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-gray-400 focus:outline-none"
          />
        </div>

        <div>
          <label className="mb-1 block text-sm font-medium text-gray-700">Participants</label>
          <input
            type="text"
            value={participants}
            onChange={(event) => setParticipants(event.target.value)}
            placeholder="e.g. Sarah Chen, Mike Rodriguez"
            className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-gray-400 focus:outline-none"
          />
        </div>

        <div>
          <div className="mb-2 flex gap-2">
            <button
              type="button"
              onClick={() => setMode("paste")}
              className={`rounded-md px-3 py-1.5 text-sm font-medium ${
                mode === "paste" ? "bg-gray-900 text-white" : "bg-gray-100 text-gray-600"
              }`}
            >
              Paste Transcript
            </button>
            <button
              type="button"
              onClick={() => setMode("upload")}
              className={`rounded-md px-3 py-1.5 text-sm font-medium ${
                mode === "upload" ? "bg-gray-900 text-white" : "bg-gray-100 text-gray-600"
              }`}
            >
              Upload .txt File
            </button>
          </div>

          {mode === "paste" ? (
            <textarea
              value={transcriptText}
              onChange={(event) => setTranscriptText(event.target.value)}
              placeholder={"Speaker: text\nSpeaker: text..."}
              rows={10}
              className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-gray-400 focus:outline-none"
            />
          ) : (
            <input
              type="file"
              accept=".txt"
              onChange={(event) => setFile(event.target.files?.[0] ?? null)}
              className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm"
            />
          )}
        </div>

        {error && <p className="text-sm text-red-600">{error}</p>}

        <button
          type="submit"
          disabled={submitting}
          className="mt-2 rounded-md bg-gray-900 px-4 py-2 text-sm font-medium text-white disabled:opacity-50"
        >
          {submitting ? "Creating..." : "Create Meeting"}
        </button>
      </form>
    </div>
  );
}
