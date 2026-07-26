"use client";

import Link from "next/link";
import { notFound, useRouter } from "next/navigation";
import { use, useEffect, useRef, useState } from "react";

import AskAI from "@/components/AskAI";
import AudioPlayer, { AudioPlayerHandle } from "@/components/AudioPlayer";
import ExportMenu from "@/components/ExportMenu";
import Loading from "@/components/Loading";
import SummaryPanel from "@/components/SummaryPanel";
import TranscriptView from "@/components/TranscriptView";
import Button from "@/components/ui/Button";
import Input from "@/components/ui/Input";
import Modal from "@/components/ui/Modal";
import { useToast } from "@/components/ui/Toast";
import { deleteMeeting, getMeeting, updateMeeting } from "@/lib/api";
import { MeetingDetail } from "@/lib/types";

interface MeetingPageProps {
  params: Promise<{ id: string }>;
}

export default function MeetingPage({ params }: MeetingPageProps) {
  const { id } = use(params);
  const router = useRouter();
  const { showToast } = useToast();
  const audioPlayerRef = useRef<AudioPlayerHandle>(null);

  const [meeting, setMeeting] = useState<MeetingDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [failed, setFailed] = useState(false);

  const [editOpen, setEditOpen] = useState(false);
  const [editTitle, setEditTitle] = useState("");
  const [editParticipants, setEditParticipants] = useState("");
  const [editError, setEditError] = useState<string | null>(null);
  const [savingEdit, setSavingEdit] = useState(false);

  const [deleteOpen, setDeleteOpen] = useState(false);
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    setLoading(true);
    setFailed(false);

    getMeeting(Number(id))
      .then(setMeeting)
      .catch(() => setFailed(true))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) {
    return <Loading message="Loading meeting..." />;
  }

  if (failed || !meeting) {
    notFound();
  }

  const currentMeeting = meeting;

  function openEdit() {
    setEditTitle(currentMeeting.title);
    setEditParticipants(currentMeeting.participants ?? "");
    setEditError(null);
    setEditOpen(true);
  }

  async function handleSaveEdit() {
    if (!editTitle.trim()) {
      setEditError("Title cannot be empty.");
      return;
    }

    setSavingEdit(true);
    try {
      const updated = await updateMeeting(currentMeeting.id, {
        title: editTitle.trim(),
        participants: editParticipants.trim(),
      });
      setMeeting((prev) =>
        prev ? { ...prev, title: updated.title, participants: updated.participants } : prev
      );
      setEditOpen(false);
      showToast("Meeting updated.", "success");
    } catch (err) {
      showToast(err instanceof Error ? err.message : "Failed to update meeting.", "error");
    } finally {
      setSavingEdit(false);
    }
  }

  async function handleDelete() {
    setDeleting(true);
    try {
      await deleteMeeting(currentMeeting.id);
      showToast("Meeting deleted.", "success");
      router.push("/");
    } catch (err) {
      showToast(err instanceof Error ? err.message : "Failed to delete meeting.", "error");
      setDeleting(false);
      setDeleteOpen(false);
    }
  }

  return (
    <div className="mt-6">
      <Link
        href="/"
        className="mb-3 inline-flex items-center gap-1 text-sm text-gray-500 hover:text-gray-900"
      >
        ← Back to Dashboard
      </Link>

      <header className="mb-6 flex items-start justify-between gap-4">
        <div>
          <h1 className="text-xl font-semibold text-gray-900">{meeting.title}</h1>
          <p className="mt-1 text-sm text-gray-500">
            {new Date(meeting.created_at).toLocaleString()}
            {meeting.participants ? ` · ${meeting.participants}` : ""}
          </p>
        </div>

        <div className="flex shrink-0 gap-2">
          <ExportMenu meetingId={meeting.id} />
          <Button onClick={openEdit}>Edit</Button>
          <Button onClick={() => setDeleteOpen(true)}>Delete</Button>
        </div>
      </header>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-[2fr_1fr_1.2fr]">
        <TranscriptView
          segments={meeting.segments}
          onSeek={(timestamp) => audioPlayerRef.current?.seekTo(timestamp)}
        />
        <AudioPlayer ref={audioPlayerRef} src={meeting.audio_url} />
        <div className="flex flex-col gap-6">
          <SummaryPanel
            summary={meeting.summary}
            topics={meeting.topics}
            actionItems={meeting.action_items}
          />
          <AskAI meetingId={meeting.id} />
        </div>
      </div>

      <Modal open={editOpen} onClose={() => setEditOpen(false)}>
        <h2 className="text-base font-semibold text-gray-900">Edit Meeting</h2>

        <div className="mt-4 flex flex-col gap-3">
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">Title</label>
            <Input value={editTitle} onChange={(event) => setEditTitle(event.target.value)} />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">Participants</label>
            <Input
              value={editParticipants}
              onChange={(event) => setEditParticipants(event.target.value)}
            />
          </div>
          {editError && <p className="text-sm text-red-600">{editError}</p>}
        </div>

        <div className="mt-5 flex justify-end gap-2">
          <button
            type="button"
            onClick={() => setEditOpen(false)}
            className="rounded-md border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
          >
            Cancel
          </button>
          <Button onClick={handleSaveEdit} disabled={savingEdit}>
            {savingEdit ? "Saving..." : "Save"}
          </Button>
        </div>
      </Modal>

      <Modal open={deleteOpen} onClose={() => setDeleteOpen(false)}>
        <h2 className="text-base font-semibold text-gray-900">Delete Meeting?</h2>
        <p className="mt-2 text-sm text-gray-600">This action cannot be undone.</p>

        <div className="mt-5 flex justify-end gap-2">
          <button
            type="button"
            onClick={() => setDeleteOpen(false)}
            className="rounded-md border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
          >
            Cancel
          </button>
          <button
            type="button"
            onClick={handleDelete}
            disabled={deleting}
            className="rounded-md bg-red-600 px-4 py-2 text-sm font-medium text-white hover:bg-red-700 disabled:opacity-50"
          >
            {deleting ? "Deleting..." : "Delete"}
          </button>
        </div>
      </Modal>
    </div>
  );
}
