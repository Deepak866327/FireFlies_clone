"use client";

import { useState } from "react";

import { getExportUrl } from "@/lib/api";

interface ExportMenuProps {
  meetingId: number;
}

const FORMATS: { format: "pdf" | "md" | "txt"; label: string }[] = [
  { format: "pdf", label: "PDF" },
  { format: "md", label: "Markdown" },
  { format: "txt", label: "Text" },
];

export default function ExportMenu({ meetingId }: ExportMenuProps) {
  const [open, setOpen] = useState(false);

  return (
    <div className="relative">
      <button
        type="button"
        onClick={() => setOpen((prev) => !prev)}
        className="rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
      >
        Export ▾
      </button>

      {open && (
        <div className="absolute right-0 z-10 mt-2 w-40 rounded-md border border-gray-200 bg-white p-1 text-sm shadow-md">
          {FORMATS.map(({ format, label }) => (
            <a
              key={format}
              href={getExportUrl(meetingId, format)}
              onClick={() => setOpen(false)}
              className="block rounded px-2 py-1.5 text-gray-700 hover:bg-gray-50"
            >
              {label}
            </a>
          ))}
        </div>
      )}
    </div>
  );
}
