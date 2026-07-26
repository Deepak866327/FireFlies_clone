"use client";

interface DateFilterProps {
  value?: string;
  onChange?: (value: string) => void;
}

const OPTIONS = [
  { value: "all", label: "All Meetings" },
  { value: "today", label: "Today" },
  { value: "7d", label: "Last 7 Days" },
  { value: "30d", label: "Last 30 Days" },
  { value: "year", label: "This Year" },
];

export default function DateFilter({ value = "all", onChange }: DateFilterProps) {
  return (
    <select
      value={value}
      onChange={(event) => onChange?.(event.target.value)}
      aria-label="Filter by date"
      className="rounded-md border border-gray-300 bg-white px-3 py-2 text-sm text-gray-700 focus:border-gray-400 focus:outline-none"
    >
      {OPTIONS.map((option) => (
        <option key={option.value} value={option.value}>
          {option.label}
        </option>
      ))}
    </select>
  );
}
