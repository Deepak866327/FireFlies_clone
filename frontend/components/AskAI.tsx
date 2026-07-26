"use client";

import { FormEvent, useEffect, useRef, useState } from "react";

import { useToast } from "@/components/ui/Toast";
import { askAboutMeeting } from "@/lib/api";
import { ChatMessage, Provider } from "@/lib/types";

interface AskAIProps {
  meetingId: number;
}

interface DisplayMessage extends ChatMessage {
  provider?: Provider;
}

const PROVIDER_LABELS: Record<Provider, string> = {
  openai: "OpenAI GPT",
  gemini: "Google Gemini",
};

const MAX_HISTORY = 5;

export default function AskAI({ meetingId }: AskAIProps) {
  const { showToast } = useToast();
  const [provider, setProvider] = useState<Provider>("openai");
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState<DisplayMessage[]>([]);
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [messages]);

  async function handleAsk(event: FormEvent) {
    event.preventDefault();
    const trimmed = question.trim();
    if (!trimmed || loading) return;

    const history: ChatMessage[] = messages
      .slice(-MAX_HISTORY)
      .map(({ role, content }) => ({ role, content }));

    setMessages((prev) => [...prev, { role: "user", content: trimmed }]);
    setQuestion("");
    setLoading(true);

    try {
      const response = await askAboutMeeting(meetingId, { provider, question: trimmed, history });
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: response.answer, provider: response.provider },
      ]);
    } catch (err) {
      showToast(err instanceof Error ? err.message : "Failed to get an answer.", "error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="rounded-lg border border-gray-200 bg-white p-4">
      <h2 className="mb-3 text-sm font-semibold text-gray-900">Ask AI</h2>

      <label className="mb-1 block text-xs font-medium text-gray-700">Model</label>
      <select
        value={provider}
        onChange={(event) => setProvider(event.target.value as Provider)}
        className="mb-3 w-full rounded-md border border-gray-300 px-3 py-1.5 text-sm focus:border-gray-400 focus:outline-none"
      >
        <option value="openai">OpenAI GPT</option>
        <option value="gemini">Google Gemini</option>
      </select>

      {messages.length > 0 && (
        <div className="mb-3 flex max-h-64 flex-col gap-3 overflow-y-auto">
          {messages.map((message, index) => (
            <div key={index}>
              {message.role === "assistant" && message.provider && (
                <span className="mb-1 inline-block rounded-full bg-gray-100 px-2 py-0.5 text-[11px] font-medium text-gray-500">
                  {PROVIDER_LABELS[message.provider]}
                </span>
              )}
              <p
                className={
                  message.role === "user"
                    ? "rounded-md bg-gray-900 px-3 py-2 text-sm text-white"
                    : "rounded-md bg-gray-50 px-3 py-2 text-sm text-gray-800"
                }
              >
                {message.content}
              </p>
            </div>
          ))}
          <div ref={bottomRef} />
        </div>
      )}

      <form onSubmit={handleAsk} className="flex gap-2">
        <input
          type="text"
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          placeholder="Ask a question about this meeting..."
          disabled={loading}
          className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-gray-400 focus:outline-none disabled:opacity-50"
        />
        <button
          type="submit"
          disabled={loading || !question.trim()}
          className="flex shrink-0 items-center gap-2 rounded-md bg-gray-900 px-4 py-2 text-sm font-medium text-white disabled:opacity-50"
        >
          {loading && (
            <span className="h-3.5 w-3.5 animate-spin rounded-full border-2 border-white/40 border-t-white" />
          )}
          {loading ? "Asking..." : "Ask"}
        </button>
      </form>
    </section>
  );
}
