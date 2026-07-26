# Deployment Guide — Railway (backend) + Vercel (frontend)

This guide deploys the FastAPI backend to **Railway** and the Next.js frontend to **Vercel**. They're deployed as two separate services that talk to each other over HTTPS — Railway gives you a backend URL, Vercel gives you a frontend URL, and you wire the two together with environment variables.

Three small, backward-compatible code changes were made to support this (all default to the exact same local-dev behavior if their env vars are unset, so nothing about running the project locally changes):
- `backend/database.py` now reads `DATABASE_URL` from the environment (falls back to the local SQLite file).
- `backend/main.py` now reads `ALLOWED_ORIGINS` from the environment (falls back to `http://localhost:3000`).
- `backend/Procfile` was added so Railway knows how to start the server.

**Order matters below** — deploy the backend first, because the frontend needs its URL, and the final CORS step needs the frontend's URL. You'll go: **Backend → Frontend → back to Backend to close the loop.**

---

## Prerequisites

- A [GitHub](https://github.com) account (both Railway and Vercel deploy from a Git repo)
- A [Railway](https://railway.app) account
- A [Vercel](https://vercel.com) account
- Git installed locally
- Your `OPENAI_API_KEY` / `GEMINI_API_KEY` on hand if you want "Ask AI" to work in production (optional — the app runs fine without them, those requests will just return a friendly "not configured" error)

---

## Step 1 — Push the project to GitHub

This project isn't in a Git repo yet, so start here.

```bash
cd C:\Users\abdde\Desktop\scalarAI
git init
git add .
git commit -m "Initial commit"
```

Create a new **empty** repository on GitHub (no README/license, so it doesn't conflict with your commit), then:

```bash
git remote add origin https://github.com/<your-username>/<your-repo>.git
git branch -M main
git push -u origin main
```

Both `frontend/.gitignore` and `backend/.gitignore` already exclude the right things (`node_modules/`, `.next/`, `.env.local`, `backend/.env`, `backend/app.db`, `backend/venv/`). Still, **before your first commit, double-check your real API keys aren't about to be staged**:

```bash
git status
```

`backend/.env` should **not** appear in that output. If it does, something's wrong with the `.gitignore` — stop and fix that before committing, don't push it and clean up after.

---

## Step 2 — Deploy the backend to Railway

1. Go to [railway.app](https://railway.app) → **New Project** → **Deploy from GitHub repo** → select your repo.
2. Railway will try to build from the repo root. Open the new service's **Settings** tab and set:
   - **Root Directory**: `backend`
   - Railway auto-detects Python via `requirements.txt` and uses the `Procfile` for the start command (`uvicorn main:app --host 0.0.0.0 --port $PORT`) — no Dockerfile needed.
3. **Add a persistent volume** (so your SQLite data survives redeploys — without this, every redeploy wipes the database back to the 5 seed meetings):
   - In the service, go to **Settings → Volumes → New Volume**.
   - Mount path: `/data`
4. Go to **Variables** and add:

   | Variable | Value |
   |---|---|
   | `DATABASE_URL` | `sqlite:////data/app.db` (note: **four** slashes — three for `sqlite://` plus the leading `/` of the absolute path) |
   | `OPENAI_API_KEY` | your key (optional) |
   | `GEMINI_API_KEY` | your key (optional) |
   | `ALLOWED_ORIGINS` | `http://localhost:3000` for now — you'll update this in Step 4 once you have your Vercel URL |

5. Deploy. Once it's live, open **Settings → Networking → Generate Domain** to get a public URL, something like `https://your-backend.up.railway.app`.
6. **Verify it's actually working** before moving on — visit `https://your-backend.up.railway.app/docs` in a browser. You should see the Swagger UI, and `GET /meetings` should return the 5 seeded meetings.

---

## Step 3 — Deploy the frontend to Vercel

1. Go to [vercel.com](https://vercel.com) → **Add New → Project** → import the same GitHub repo.
2. In the import screen, set **Root Directory** to `frontend` (Vercel needs this since the repo has `backend/` and `frontend/` as siblings, not a single app at the root).
3. Framework preset should auto-detect as **Next.js** — leave build/output settings on their defaults.
4. Under **Environment Variables**, add:

   | Variable | Value |
   |---|---|
   | `NEXT_PUBLIC_API_URL` | your Railway backend URL from Step 2, e.g. `https://your-backend.up.railway.app` (no trailing slash) |

5. Click **Deploy**. Once done, you'll get a URL like `https://your-app.vercel.app`.
6. Open it — the dashboard will load the shell, but data fetches will fail with a CORS error right now. That's expected — you haven't told the backend to trust this origin yet. That's the next step.

---

## Step 4 — Close the loop: allow the Vercel origin on Railway

1. Back in Railway, open your backend service → **Variables**.
2. Update `ALLOWED_ORIGINS` to your real Vercel URL:
   ```
   ALLOWED_ORIGINS=https://your-app.vercel.app
   ```
   If you also want to test from `localhost:3000` against the deployed backend, use a comma-separated list (the code already supports this):
   ```
   ALLOWED_ORIGINS=http://localhost:3000,https://your-app.vercel.app
   ```
3. Save — Railway will automatically redeploy the service with the new variable (or trigger a redeploy manually from the **Deployments** tab if it doesn't).

---

## Step 5 — Verify end-to-end

Open your Vercel URL and check, in order:

- ✓ Dashboard loads and shows the 5 seeded meetings
- ✓ Search, date filter, and sort all work
- ✓ Opening a meeting loads its transcript/summary/topics/action items
- ✓ Checking an action item persists (refresh the page, it should stay checked)
- ✓ Create a new meeting via Upload, confirm it appears on the dashboard
- ✓ Edit and Delete a meeting work
- ✓ Export → PDF/Markdown/Text all download correctly
- ✓ Ask AI returns an answer (if you set API keys) or a clear "not configured" message (if you didn't)

If any data-fetching step fails, open the browser DevTools Network tab first — a CORS error there means Step 4 isn't done yet or has a typo; a connection failure means the `NEXT_PUBLIC_API_URL` in Vercel is wrong or the Railway service is down.

---

## Redeploying after changes

Both platforms auto-deploy on push once connected:

```bash
git add .
git commit -m "Your change"
git push
```

Railway redeploys the backend, Vercel redeploys the frontend, both from the same push. No manual steps needed unless you're changing environment variables.

---

## Troubleshooting

**CORS error in the browser console, requests going to the right URL**
`ALLOWED_ORIGINS` on Railway doesn't include your exact Vercel origin (must match scheme + host exactly, no trailing slash). Re-check Step 4.

**Frontend shows network errors, nothing reaches the backend at all**
`NEXT_PUBLIC_API_URL` in Vercel is missing, wrong, or you forgot to redeploy after adding it — Vercel env vars only apply to builds that happen after they're set. Trigger a redeploy from the Vercel dashboard after adding/changing it.

**Dashboard resets to only the 5 seed meetings after every deploy**
The Railway volume isn't mounted, or `DATABASE_URL` isn't pointed at it. Without both, `app.db` lives on the container's ephemeral filesystem and is wiped on every redeploy.

**502/504 from `/meetings/{id}/chat`**
This is almost always the LLM provider, not your deployment — see the app's own error message (it now surfaces OpenAI's/Gemini's real reason: missing key, no quota/billing, invalid model, etc.), not a Railway/Vercel problem.

**Railway build fails on a specific package**
Some packages (this project hit this with `reportlab`/`pydantic-core` during local development) don't have prebuilt wheels for very new Python versions and try to compile from source, which can fail in Railway's build environment. If this happens, add a `backend/.python-version` file pinning a slightly older, more widely-supported Python (e.g. `3.12`) and redeploy.

**Cold starts / free-tier sleep**
Both Railway's and Vercel's free tiers have usage limits and may cold-start or pause after inactivity — check current pricing/limits on each platform if this matters for your use case; this guide doesn't assume a specific paid tier.

---

## What's intentionally not covered here

- Migrating off SQLite to Postgres (the `DATABASE_URL` env var change from Step 2 already makes this a connection-string swap whenever you want it — see `README.md`'s Trade-offs section)
- Custom domains (both platforms support them under their respective domain settings; not required for a working deployment)
- CI/CD beyond each platform's built-in "redeploy on push" (already enough for this project's scope)
