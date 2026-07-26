"use client";

interface SortDropdownProps {
  value?: string;
  onChange?: (value: string) => void;
}

export default function SortDropdown({ value = "newest", onChange }: SortDropdownProps) {
  return (
    <select
      value={value}
      onChange={(event) => onChange?.(event.target.value)}
      aria-label="Sort meetings"
      className="rounded-md border border-gray-300 bg-white px-3 py-2 text-sm text-gray-700 focus:border-gray-400 focus:outline-none"
    >
      <option value="newest">Newest First</option>
      <option value="oldest">Oldest First</option>
      <option value="az">A → Z</option>
      <option value="za">Z → A</option>
    </select>
  );
}
