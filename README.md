# Meeting Notes — AI-Powered Meeting Intelligence Platform

A full-stack meeting notes platform inspired by [Fireflies.ai](https://fireflies.ai). Paste or upload a meeting transcript and get an automatically generated summary, topic list, and action items — then search the transcript, chat with an AI about the meeting, and export everything to PDF, Markdown, or plain text.

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-000000?logo=next.js&logoColor=white)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-06B6D4?logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-412991?logo=openai&logoColor=white)](https://platform.openai.com/)
[![Gemini](https://img.shields.io/badge/Google_Gemini-8E75B2?logo=googlegemini&logoColor=white)](https://ai.google.dev/)
[![Vercel](https://img.shields.io/badge/Deployed_on-Vercel-000000?logo=vercel&logoColor=white)](https://vercel.com/)
[![Railway](https://img.shields.io/badge/Deployed_on-Railway-0B0D0E?logo=railway&logoColor=white)](https://railway.app/)

---

## Overview

**Meeting Notes** turns a raw meeting transcript into a structured, searchable record. Instead of requiring live audio capture or a meeting bot, the platform is **transcript-first**: paste text or upload a `.txt`/`.json` transcript, and the backend automatically derives a summary, topics, and action items, then stores everything in a relational database for browsing, searching, editing, and exporting later.

On top of the automatic notes, an optional **Ask AI** panel lets you have a real conversation with either **OpenAI GPT** or **Google Gemini** about a specific meeting — answers are grounded strictly in that meeting's own content.

This is a personal/portfolio project built to demonstrate a complete, production-shaped full-stack application: a typed React frontend, a clean FastAPI backend with a proper service layer, a normalized relational schema, real third-party AI integration, and a working cloud deployment.

---

## Features

### Meetings
- **Meeting dashboard** with search, date filtering, and sorting
- **Search** by meeting title, participant name, or transcript content
- **Date filters** — Today, Last 7 Days, Last 30 Days, This Year, All Meetings
- **Sorting** — Newest First, Oldest First, A → Z, Z → A
- **Full CRUD** — create, view, edit (title & participants), and delete meetings
- **Transcript upload** — paste text directly or upload a `.txt`/`.json` transcript file

### Automatic meeting notes
- **Meeting summary** — generated automatically from the transcript on creation
- **Topic extraction** — key topics surfaced as tags
- **Action items** — extracted automatically, with an interactive checklist to mark them complete
- **Transcript view** — speaker-attributed, timestamped, with in-transcript search and highlighting

> These automatic notes use deterministic, rule-based text analysis (word frequency, phrase matching) — not a language model — so the app works fully offline with no API keys. See [Known Limitations](#-known-limitations).

### Ask AI
- **Chat with a meeting** using either **OpenAI GPT** or **Google Gemini** — switch providers per question
- Answers are grounded only in that meeting's title, summary, topics, action items, and transcript
- Short-term conversation memory (last 5 exchanges) within the page session — nothing is stored permanently

### Export
- **PDF export** (via ReportLab)
- **Markdown export** (`.md`)
- **Plain text export** (`.txt`)

Each format includes the meeting title, date, participants, summary, topics, action items, and full timestamped transcript.

### Other
- **Toast notifications** for create/update/delete/error feedback
- **Audio player UI** — present in the interface; there is currently no audio upload/transcription pipeline behind it (see [Known Limitations](#-known-limitations))
- **Live Meeting Bot**, **Speech-to-Text**, **Integrations**, **Team Collaboration**, **Profile**, and **Settings** — UI placeholders marked "Coming Soon", included to show the intended product surface. No backend logic sits behind them today.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend framework | Next.js 16 (App Router) |
| Frontend language | TypeScript |
| Styling | Tailwind CSS |
| Backend framework | FastAPI |
| Backend language | Python |
| ORM | SQLAlchemy (sync) |
| Validation / schemas | Pydantic v2 |
| Database | SQLite |
| PDF generation | ReportLab |
| AI providers | OpenAI (Chat Completions API) & Google Gemini API, called directly over HTTPS via `httpx` — no LangChain, no vector store |
| Frontend hosting | Vercel |
| Backend hosting | Railway |

---

## Architecture

The project deliberately avoids heavyweight patterns (no repository layer, no dependency-injection framework, no CQRS) in favor of a flat, readable structure on both sides.

**Backend** — one direction of dependency, no circular logic:

```
Router  →  Service  →  SQLAlchemy Model  →  SQLite
```

Routers handle HTTP concerns only (parsing, status codes, 404s). All business logic — transcript parsing, note generation, AI prompting, PDF/Markdown/text rendering — lives in `services/`. The AI integration uses a small **provider/factory pattern** (`services/llm/`) so OpenAI and Gemini share one interface and routers never branch on which provider was chosen.

**Frontend** — pages own data-fetching, components stay presentational:

```
Page  →  Component  →  lib/api.ts  →  Backend API
```

`lib/api.ts` is the single place that calls `fetch()` — no component talks to the network directly.

---

## Folder Structure

```
scalarAI/
├── backend/
│   ├── main.py                     # FastAPI app, CORS, router registration, startup hook
│   ├── database.py                  # SQLAlchemy engine/session (SQLite by default, DATABASE_URL-configurable)
│   ├── seed.py                       # seeds 5 demo meetings on first run
│   ├── requirements.txt
│   ├── Procfile                      # Railway start command
│   ├── models/                       # SQLAlchemy models (Meeting, TranscriptSegment, ActionItem, Topic)
│   ├── schemas/                      # Pydantic request/response models, incl. chat schemas
│   ├── routers/
│   │   ├── meetings.py                # meeting CRUD + transcript search
│   │   ├── action_items.py            # action item updates
│   │   ├── export.py                  # PDF / Markdown / TXT export
│   │   └── chat.py                    # Ask AI endpoint
│   └── services/
│       ├── meeting_service.py         # transcript parsing + summary/topic/action-item generation
│       ├── export_service.py          # export document builders
│       ├── chat_service.py            # meeting-context prompt building + history trimming
│       └── llm/                       # provider-based AI architecture
│           ├── base.py                 # provider interface + typed errors
│           ├── factory.py              # provider name → provider instance
│           ├── openai_provider.py
│           └── gemini_provider.py
│
└── frontend/
    ├── app/
    │   ├── layout.tsx                  # root layout, navbar, toast provider
    │   ├── page.tsx                     # dashboard
    │   ├── upload/page.tsx               # create meeting
    │   ├── meetings/[id]/page.tsx        # meeting detail (transcript, summary, export, Ask AI)
    │   ├── integrations/page.tsx         # placeholder
    │   ├── team/page.tsx                 # placeholder
    │   ├── profile/page.tsx              # placeholder (mock user, no auth)
    │   └── settings/page.tsx             # placeholder
    ├── components/
    │   ├── TranscriptView.tsx, SummaryPanel.tsx, AudioPlayer.tsx
    │   ├── ExportMenu.tsx, AskAI.tsx
    │   ├── MeetingCard.tsx, MeetingList.tsx, SearchBar.tsx, DateFilter.tsx, SortDropdown.tsx
    │   └── ui/                          # Button, Card, Input, Modal, Textarea, Toast
    └── lib/
        ├── types.ts                     # TypeScript types mirroring backend schemas
        └── api.ts                       # typed fetch client
```

---

## Installation

### Prerequisites

- **Node.js 20+**
- **Python 3.11+**
- (Optional) An [OpenAI API key](https://platform.openai.com/api-keys) and/or [Google Gemini API key](https://ai.google.dev/) if you want the Ask AI feature to work — the rest of the app runs fully without them.

### Clone the repository

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd scalarAI
```

---

## Backend Setup

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

Create `backend/.env` (see [Environment Variables](#-environment-variables) below — every value is optional for local development):

```bash
cp .env.example .env
```

Run the API:

```bash
uvicorn main:app --reload
```

The API is now available at `http://localhost:8000`, with interactive docs at `http://localhost:8000/docs`. Tables are created and the database is seeded with 5 demo meetings automatically on first startup — no manual migration step required.

---

## Frontend Setup

```bash
cd frontend
npm install
cp .env.local.example .env.local
npm run dev
```

The app is now available at `http://localhost:3000`. Start the backend first so the dashboard has data to load.

---

## Environment Variables

### Backend (`backend/.env`)

| Variable | Required | Default | Description |
|---|---|---|---|
| `OPENAI_API_KEY` | No | — | Enables the OpenAI option in Ask AI. Without it, selecting OpenAI returns a friendly "not configured" error. |
| `GEMINI_API_KEY` | No | — | Enables the Google Gemini option in Ask AI. Same behavior as above if unset. |
| `ALLOWED_ORIGINS` | No | `http://localhost:3000` | Comma-separated list of origins allowed to call the API (CORS). Set this to your deployed frontend URL in production. |
| `DATABASE_URL` | No | `sqlite:///./app.db` | SQLAlchemy connection string. Swappable to Postgres or a persistent-volume SQLite path without other code changes. |

### Frontend (`frontend/.env.local`)

| Variable | Required | Default | Description |
|---|---|---|---|
| `NEXT_PUBLIC_API_URL` | Yes | `http://127.0.0.1:8000` (fallback in code) | Base URL of the backend API. |

---

## Running Locally

1. Start the backend: `cd backend && uvicorn main:app --reload`
2. Start the frontend: `cd frontend && npm run dev`
3. Open `http://localhost:3000`

---

## Building for Production

**Frontend:**

```bash
cd frontend
npm run build
npm run start
```

**Backend:** there is no separate build step — FastAPI runs the same way in production as in development, just without `--reload` and bound to the host/port your platform provides:

```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port $PORT
```

---

## Deployment

The app deploys as two independent services: **frontend on Vercel**, **backend on Railway**.

**Backend (Railway):**
1. Create a new Railway project from this GitHub repository, with **Root Directory** set to `backend`.
2. Railway auto-detects Python via `requirements.txt` and uses the included `Procfile` as the start command.
3. Set the environment variables from the [Backend table](#backend-backendenv) above (`OPENAI_API_KEY`, `GEMINI_API_KEY`, `ALLOWED_ORIGINS`, `DATABASE_URL`).
4. Generate a public domain for the service.

**Frontend (Vercel):**
1. Import this repository into Vercel with **Root Directory** set to `frontend`.
2. Set `NEXT_PUBLIC_API_URL` to your Railway backend's public URL.
3. Deploy.

**Finally**, update `ALLOWED_ORIGINS` on Railway to include your real Vercel domain so the browser isn't blocked by CORS.

A full, detailed step-by-step walkthrough (including SQLite persistence options and troubleshooting) is in [`deploy.md`](./deploy.md).

---

## API Overview

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/meetings` | List meetings — supports `search`, `date_filter`, `sort` query params |
| `GET` | `/meetings/{id}` | Full meeting detail |
| `GET` | `/meetings/{id}/transcript` | Transcript segments only, with optional `search` |
| `POST` | `/meetings` | Create a meeting from pasted text or an uploaded `.txt`/`.json` file |
| `PUT` | `/meetings/{id}` | Update a meeting's title/participants |
| `DELETE` | `/meetings/{id}` | Delete a meeting (cascades to its segments, action items, and topics) |
| `PATCH` | `/action-items/{id}` | Update an action item (e.g. toggle completion) |
| `GET` | `/meetings/{id}/export?format=pdf\|md\|txt` | Download the meeting as a file |
| `POST` | `/meetings/{id}/chat` | Ask AI a question about the meeting (`{ provider, question }`) |

Interactive API documentation is auto-generated by FastAPI at `/docs`.

---

## Known Limitations

Being upfront about what this project does **not** do:

- **Automatic summaries/topics/action items are rule-based, not AI-generated.** They use keyword frequency and phrase matching, not a language model. (The separate **Ask AI** chat feature does use real LLMs.)
- **No audio or video transcription.** The app is transcript-first by design; the audio player UI exists but nothing currently populates it with real audio.
- **SQLite is file-based.** On platforms with an ephemeral filesystem (like a default Railway deploy without a persistent volume), data resets on redeploy unless `DATABASE_URL` points at persistent storage.
- **No authentication.** The app assumes a single demo user; Profile, Settings, Integrations, and Team pages are UI placeholders with no backend behind them.
- **Search is basic SQL pattern matching**, not a full-text search engine.
- **No automated test suite** yet.
- **Chat history is not persisted** — it lives only in the browser tab for the current session, by design.

---

## Future Improvements

- Real audio/video upload with transcription (e.g. Whisper)
- Optional LLM-based summary/topic/action-item generation as an alternative to the rule-based engine
- Full-text search (SQLite FTS5 or a dedicated search index)
- Authentication and multi-user workspaces
- Real integrations (calendar, CRM, conferencing platforms)
- Automated backend and frontend test suites
- Pagination for large meeting libraries

---



