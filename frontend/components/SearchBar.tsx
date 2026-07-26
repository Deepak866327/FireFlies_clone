"use client";

interface SearchBarProps {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
}

export default function SearchBar({
  value,
  onChange,
  placeholder = "Search meetings...",
}: SearchBarProps) {
  return (
    <input
      type="text"
      value={value}
      onChange={(event) => onChange(event.target.value)}
      placeholder={placeholder}
      aria-label="Search meetings"
      className="w-full max-w-sm rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-gray-400 focus:outline-none"
    />
  );
}
