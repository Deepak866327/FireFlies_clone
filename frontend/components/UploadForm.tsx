"use client";

import { FormEvent, useState } from "react";

export interface UploadFormData {
  title: string;
  participants?: string;
  transcript_text?: string;
  file?: File;
}

interface UploadFormProps {
  onSubmit: (data: UploadFormData) => void;
  submitting?: boolean;
}

export default function UploadForm({ onSubmit, submitting = false }: UploadFormProps) {
  const [title, setTitle] = useState("");
  const [participants, setParticipants] = useState("");
  const [transcriptText, setTranscriptText] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [mode, setMode] = useState<"paste" | "upload">("paste");
  const [validationError, setValidationError] = useState<string | null>(null);

  function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setValidationError(null);

    if (!title.trim()) {
      setValidationError("Please enter a meeting title.");
      return;
    }
    if (mode === "paste" && !transcriptText.trim()) {
      setValidationError("Please paste a transcript.");
      return;
    }
    if (mode === "upload" && !file) {
      setValidationError("Please choose a transcript file.");
      return;
    }

    onSubmit({
      title: title.trim(),
      participants: participants.trim() || undefined,
      transcript_text: mode === "paste" ? transcriptText : undefined,
      file: mode === "upload" ? file ?? undefined : undefined,
    });
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4">
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
            Upload File
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
            accept=".txt,.json"
            onChange={(event) => setFile(event.target.files?.[0] ?? null)}
            className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm"
          />
        )}
      </div>

      {validationError && <p className="text-sm text-red-600">{validationError}</p>}

      <button
        type="submit"
        disabled={submitting}
        className="mt-2 rounded-md bg-gray-900 px-4 py-2 text-sm font-medium text-white disabled:opacity-50"
      >
        {submitting ? "Creating..." : "Create Meeting"}
      </button>
    </form>
  );
}
