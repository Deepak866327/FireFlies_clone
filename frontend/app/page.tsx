"use client";

import { useEffect, useState } from "react";

import DateFilter from "@/components/DateFilter";
import EmptyState from "@/components/EmptyState";
import Loading from "@/components/Loading";
import MeetingList from "@/components/MeetingList";
import PlaceholderCard from "@/components/PlaceholderCard";
import SearchBar from "@/components/SearchBar";
import SortDropdown from "@/components/SortDropdown";
import { getMeetings } from "@/lib/api";
import { Meeting } from "@/lib/types";

const BOT_ICON = (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" className="h-5 w-5 text-gray-500">
    <rect x="5" y="9" width="14" height="10" rx="2" />
    <path strokeLinecap="round" d="M12 9V5m-3 0h6" />
    <circle cx="9" cy="14" r="1" />
    <circle cx="15" cy="14" r="1" />
  </svg>
);

export default function HomePage() {
  const [meetings, setMeetings] = useState<Meeting[]>([]);
  const [search, setSearch] = useState("");
  const [dateFilter, setDateFilter] = useState("all");
  const [sort, setSort] = useState("newest");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    setError(null);

    getMeetings({ search, dateFilter, sort })
      .then(setMeetings)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [search, dateFilter, sort]);

  return (
    <>
      <section className="mt-6">
        <h2 className="text-sm font-semibold text-gray-900">Live Meeting Assistant</h2>
        <div className="mt-2">
          <PlaceholderCard
            title="Live Meeting Bot"
            description="Automatically joins Zoom, Google Meet and Microsoft Teams meetings to record and transcribe conversations."
            icon={BOT_ICON}
          />
        </div>
      </section>

      <div className="mt-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <SearchBar
          value={search}
          onChange={setSearch}
          placeholder="Search by title, participant, or transcript..."
        />
        <div className="flex gap-2">
          <DateFilter value={dateFilter} onChange={setDateFilter} />
          <SortDropdown value={sort} onChange={setSort} />
        </div>
      </div>

      <div className="mt-6">
        {loading ? (
          <Loading />
        ) : error ? (
          <p className="text-red-600">{error}</p>
        ) : meetings.length === 0 ? (
          <EmptyState />
        ) : (
          <MeetingList meetings={meetings} />
        )}
      </div>
    </>
  );
}
