"use client";

import { useState } from "react";

import { useToast } from "@/components/ui/Toast";
import { toggleActionItem } from "@/lib/api";
import { ActionItem, Topic } from "@/lib/types";

interface SummaryPanelProps {
  summary: string | null;
  topics: Topic[];
  actionItems: ActionItem[];
}

export default function SummaryPanel({ summary, topics, actionItems }: SummaryPanelProps) {
  const [items, setItems] = useState(actionItems);
  const { showToast } = useToast();

  async function handleToggle(item: ActionItem) {
    const nextDone = !item.is_done;
    setItems((prev) => prev.map((i) => (i.id === item.id ? { ...i, is_done: nextDone } : i)));

    try {
      await toggleActionItem(item.id, nextDone);
      showToast(nextDone ? "Action item completed." : "Action item updated.", "success");
    } catch (err) {
      setItems((prev) => prev.map((i) => (i.id === item.id ? { ...i, is_done: !nextDone } : i)));
      showToast(
        err instanceof Error ? err.message : "Failed to update action item.",
        "error"
      );
    }
  }

  return (
    <div className="flex flex-col gap-4">
      <section className="rounded-lg border border-gray-200 bg-white p-4">
        <h2 className="mb-2 text-sm font-semibold text-gray-900">Summary</h2>
        <p className="text-sm text-gray-600">{summary || "No summary available."}</p>
      </section>

      <section className="rounded-lg border border-gray-200 bg-white p-4">
        <h2 className="mb-2 text-sm font-semibold text-gray-900">Topics</h2>
        {topics.length === 0 ? (
          <p className="text-sm text-gray-500">No topics extracted.</p>
        ) : (
          <div className="flex flex-wrap gap-2">
            {topics.map((topic) => (
              <span
                key={topic.id}
                className="rounded-full bg-gray-100 px-2.5 py-1 text-xs font-medium text-gray-700"
              >
                {topic.label}
              </span>
            ))}
          </div>
        )}
      </section>

      <section className="rounded-lg border border-gray-200 bg-white p-4">
        <h2 className="mb-2 text-sm font-semibold text-gray-900">Action Items</h2>
        {items.length === 0 ? (
          <p className="text-sm text-gray-500">No action items.</p>
        ) : (
          <ul className="flex flex-col gap-2">
            {items.map((item) => (
              <li key={item.id}>
                <label className="flex items-start gap-2 text-sm">
                  <input
                    type="checkbox"
                    checked={item.is_done}
                    onChange={() => handleToggle(item)}
                    className="mt-0.5 h-4 w-4 shrink-0 rounded border-gray-300"
                  />
                  <span className={item.is_done ? "text-gray-400 line-through" : "text-gray-800"}>
                    {item.text}
                    {item.owner && (
                      <span className="ml-1 text-xs text-gray-400">— {item.owner}</span>
                    )}
                  </span>
                </label>
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  );
}
