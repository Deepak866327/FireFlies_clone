"use client";

import Link from "next/link";
import { useState } from "react";

const NAV_LINKS = [
  { href: "/", label: "Dashboard" },
  { href: "/integrations", label: "Integrations" },
  { href: "/team", label: "Team" },
];

export default function Navbar() {
  const [userMenuOpen, setUserMenuOpen] = useState(false);

  return (
    <header className="flex flex-wrap items-center justify-between gap-4 border-b border-gray-200 pb-4">
      <div className="flex flex-wrap items-center gap-6">
        <span className="text-lg font-semibold text-gray-900">Meeting Notes</span>
        <nav className="flex flex-wrap gap-4">
          {NAV_LINKS.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className="text-sm font-medium text-gray-600 hover:text-gray-900"
            >
              {link.label}
            </Link>
          ))}
        </nav>
      </div>

      <div className="flex items-center gap-2">
        <Link
          href="/upload"
          className="rounded-md bg-gray-900 px-4 py-2 text-sm font-medium text-white hover:bg-gray-800"
        >
          New Meeting
        </Link>

        <div className="relative">
          <button
            type="button"
            onClick={() => setUserMenuOpen((prev) => !prev)}
            aria-label="Account menu"
            className="flex h-9 w-9 items-center justify-center rounded-full bg-gray-900 text-sm font-semibold text-white"
          >
            D
          </button>

          {userMenuOpen && (
            <div className="absolute right-0 z-10 mt-2 w-56 rounded-md border border-gray-200 bg-white p-2 text-sm shadow-md">
              <div className="border-b border-gray-100 px-2 pb-2">
                <p className="font-medium text-gray-900">Demo User</p>
                <p className="text-xs text-gray-500">demo@example.com</p>
              </div>

              <Link
                href="/profile"
                onClick={() => setUserMenuOpen(false)}
                className="mt-1 block rounded px-2 py-1.5 text-gray-700 hover:bg-gray-50"
              >
                Profile
              </Link>
              <Link
                href="/settings"
                onClick={() => setUserMenuOpen(false)}
                className="block rounded px-2 py-1.5 text-gray-700 hover:bg-gray-50"
              >
                Settings
              </Link>
              <button
                type="button"
                disabled
                className="block w-full cursor-not-allowed rounded px-2 py-1.5 text-left text-gray-400"
              >
                Logout
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
