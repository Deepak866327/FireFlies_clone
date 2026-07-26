"use client";

import { ReactNode, useEffect, useRef, useState } from "react";

import { TranscriptSegment } from "@/lib/types";

interface TranscriptViewProps {
  segments: TranscriptSegment[];
  onSeek: (timestamp: number) => void;
}

function formatTimestamp(seconds: number | null): string {
  if (seconds === null) return "--:--";
  const minutes = Math.floor(seconds / 60);
  const remaining = Math.floor(seconds % 60);
  return `${minutes}:${remaining.toString().padStart(2, "0")}`;
}

function highlightText(text: string, term: string): ReactNode {
  if (!term.trim()) return text;

  const index = text.toLowerCase().indexOf(term.toLowerCase());
  if (index === -1) return text;

  return (
    <>
      {text.slice(0, index)}
      <mark className="bg-yellow-200">{text.slice(index, index + term.length)}</mark>
      {text.slice(index + term.length)}
    </>
  );
}

export default function TranscriptView({ segments, onSeek }: TranscriptViewProps) {
  const [search, setSearch] = useState("");
  const [activeId, setActiveId] = useState<number | null>(null);
  const lineRefs = useRef<Record<number, HTMLButtonElement | null>>({});

  useEffect(() => {
    if (!search.trim()) return;

    const firstMatch = segments.find((segment) =>
      segment.text.toLowerCase().includes(search.toLowerCase())
    );

    if (firstMatch) {
      lineRefs.current[firstMatch.id]?.scrollIntoView({ behavior: "smooth", block: "center" });
    }
  }, [search, segments]);

  function handleLineClick(segment: TranscriptSegment) {
    setActiveId(segment.id);
    onSeek(segment.start_time ?? 0);
  }

  return (
    <div className="rounded-lg border border-gray-200 bg-white p-4">
      <h2 className="mb-3 text-sm font-semibold text-gray-900">Transcript</h2>

      <input
        type="text"
        value={search}
        onChange={(event) => setSearch(event.target.value)}
        placeholder="Search transcript..."
        className="mb-3 w-full rounded-md border border-gray-300 px-3 py-1.5 text-sm focus:border-gray-400 focus:outline-none"
      />

      <div className="flex max-h-[70vh] flex-col gap-2 overflow-y-auto">
        {segments.map((segment) => {
          const isActive = segment.id === activeId;

          return (
            <button
              key={segment.id}
              ref={(el) => {
                lineRefs.current[segment.id] = el;
              }}
              type="button"
              onClick={() => handleLineClick(segment)}
              className={`flex gap-3 rounded-md p-2 text-left transition ${
                isActive ? "bg-blue-50" : "hover:bg-gray-50"
              }`}
            >
              <span className="w-12 shrink-0 pt-0.5 text-xs font-medium text-gray-400">
                {formatTimestamp(segment.start_time)}
              </span>
              <div>
                {segment.speaker && (
                  <p className="text-xs font-semibold text-gray-700">{segment.speaker}</p>
                )}
                <p className="text-sm text-gray-800">{highlightText(segment.text, search)}</p>
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
}
