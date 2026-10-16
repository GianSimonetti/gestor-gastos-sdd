# Quickstart and Validation Guide: Gestor de Gastos MVP

This guide validates the design end to end after implementation. It does not replace the detailed
requirements in [spec.md](./spec.md), the model in [data-model.md](./data-model.md), or the HTTP
contract in [contracts/openapi.yaml](./contracts/openapi.yaml).

## Prerequisites

- Python 3.12 and `uv`
- Node.js with npm
- A writable local directory for SQLite and temporary audio files
- The pinned `faster-whisper` `small` model available in the configured model cache
- For production-like recovery validation, access to a TLS-capable SMTP server; automated tests use
  an in-memory sender and make no network calls
- Safari on iOS 14 at 390 × 844 CSS pixels and Chrome on Android 12 at 360 × 800 CSS pixels for the
  required responsive matrix

## Configuration

Create local environment configuration outside version control. At minimum, provide:

```text
DATABASE_URL=sqlite:///.../gestor_gastos.db
JWT_SECRET=<random secret, never committed>
JWT_ISSUER=gestor-gastos
JWT_AUDIENCE=gestor-gastos-web
INVITATION_SECRET=<independent random secret, never committed>
APP_TIMEZONE=America/Argentina/Buenos_Aires
FRONTEND_ORIGIN=http://localhost:5173
RESET_URL_BASE=http://localhost:5173/reset-password
EMAIL_BACKEND=memory
WHISPER_MODEL=small
WHISPER_DEVICE=cpu
WHISPER_COMPUTE_TYPE=int8
WHISPER_LOCAL_ONLY=true
```

For real email delivery, replace the memory backend with SMTP and provide host, port, sender,
username/password and TLS settings through environment variables. Never place these values in source
files. Download/cache the pinned speech model during setup; runtime validation uses local-only mode
to avoid an implicit network dependency.

## Install and run

Backend:

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload
```

Frontend in another terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend should be available at `http://localhost:5173`. The API contract and interactive
documentation should reflect [contracts/openapi.yaml](./contracts/openapi.yaml).

## Test-first validation order

Critical rules must be introduced as failing tests before their implementation. Run the fast suite
frequently:

```bash
cd backend
uv run pytest -m "not audio_eval and not performance"
```

Required test groups:

1. `tests/unit`: decimal parsing, Money, personal/equal/custom distributions, residual cents,
   debts, consumed/remaining calculations, USD totals and Argentina default dates.
2. `tests/integration`: file-backed SQLite constraints, transaction rollback, persistence across a
   recreated engine, membership/person identity, cross-board isolation and stale-version conflicts.
3. `tests/api`: request/response shapes, cookie JWT lifecycle, password recovery, invitation code,
   CRUD flows, pagination, audio proposal separation and uniform errors.
4. `tests/fixtures/audio-eval`: frozen manifest plus exactly 20 consented, non-sensitive Argentine
   Spanish audio files and SHA-256 hashes. Freeze the files and manifest before implementing or
   adjusting extraction rules.

Run the slower audio gate explicitly:

```bash
cd backend
uv run pytest -m audio_eval
```

It passes only when at least 12 of the 20 frozen cases match every expected value present in their
manifest entry. A partial field match does not count.

Run the authentication performance gate in the fixed 2-vCPU/4-GB environment against a running
backend with no external calls:

```bash
cd backend
uv run pytest -m performance
```

The scenario performs 10 excluded warmups followed by 100 valid logins with concurrency 5; at least
95 measured requests must complete in 4 seconds or less.

Build the frontend after any frontend change:

```bash
cd frontend
npm run build
```

## End-to-end validation scenarios

### 1. Account and recovery

1. Register Carla with display name, unique email and a password of at least 8 characters.
2. Log in and refresh the browser; the HttpOnly session remains usable without exposing a token to
   JavaScript.
3. Log out and confirm protected data requires a new login.
4. Request recovery. The response must be identical for registered and unknown emails.
5. From the in-memory mail outbox, use the reset link within 30 minutes. The old password must fail,
   the new password must succeed, and a second use of the same link must fail.
6. Repeat with the clock advanced to 30 minutes and confirm expiry without plaintext token storage.

### 2. Board isolation and invitations

1. Carla creates Hogar and receives one invitation code valid for 7 days.
2. Request it again before expiry and confirm the same code is returned.
3. A second account joins with the code; repeated join does not duplicate membership.
4. Advance beyond 7 days, request a code and confirm rotation.
5. With a third authenticated non-member, attempt every board read and mutation class. Each must
   return the uniform unavailable response and leave data unchanged.

### 3. People and historical identity

1. Add guest Ana, rename her to Ana Pérez and use her in a confirmed expense.
2. Retire her and confirm she disappears from new-expense choices while remaining in historical
   expense detail.
3. Create homonymous people and confirm account emails/candidate choices disambiguate selection and
   audio proposals rather than guessing.

### 4. Exact expense distribution

1. Create a personal expense and confirm the full amount belongs to the payer with no self-debt.
2. Split ARS 30.000,00 equally between two people and confirm ARS 15.000,00 each.
3. Split ARS 100,00 between three people in a fixed order repeatedly. The same first person receives
   the residual cent every time and shares sum to ARS 100,00.
4. Create a custom ARS 150.000,00 split of ARS 40.000,00/ARS 110.000,00 and confirm the second
   person's debt to the payer.
5. Submit a negative share, more than two decimal places and a non-matching sum. Each must fail
   without an expense or partial shares.

### 5. Monthly budget and corrections

1. Without a base, record expenses and confirm consumed is shown while remaining is unavailable.
2. Set January 2026 base to ARS 500.000,00; edit it to ARS 600.000,00 with ARS 40.000,00 expenses
   and ARS 150.000,00 in USD purchases. Remaining must be ARS 410.000,00.
3. Change an expense's amount and month; both original and destination summaries update.
4. Delete an expense only after UI confirmation and verify totals return to the state derived from
   remaining movements.
5. Send two edits with the same version. The first succeeds; the second receives a conflict and
   makes no change.

### 6. Savings

1. Create, edit and remove the single initial USD savings record.
2. Record USD 100,00 bought with ARS 150.000,00. Confirm USD increases total savings while ARS
   increases only the corresponding month's consumption.
3. Edit the purchase to USD 120,00/ARS 180.000,00 and confirm the delta is reflected once.
4. Move a purchase to another month and then delete it; both summaries and the USD total must be
   derived from current records only.

### 7. Audio proposal

1. Start recording after an explicit user gesture. Confirm visible requesting, recording,
   processing, proposal and error states.
2. On an environment without usable `MediaRecorder`, select or capture an audio file through the
   fallback control.
3. Process a complete example and review every extracted field before confirmation.
4. Process silence, ambiguous names and missing category. Each returns an editable incomplete
   proposal and creates no expense.
5. Accept WAV, MP3, M4A/MP4, WebM and Ogg. Reject any other container, files over 15 MB or 60
   seconds, and temporary transcription failure without financial mutations; manual entry remains
   available.
6. Edit the proposal and confirm it through the normal expense creation flow. Exactly one expense
   is created from the final reviewed values.

### 8. Responsive and accessible operation

For every screen used above, run the fixed Safari/iOS and Chrome/Android matrix in portrait at 100%
zoom. Requirements pass only when there is no page-level horizontal scrolling, clipped content or
inaccessible control. Also confirm:

- visible labels and field-associated errors;
- controls remain usable with the virtual keyboard open;
- category bars have an equivalent textual category/amount list and do not rely on color alone;
- recording tracks stop after completion or cancellation.

### 9. Unassisted usability outcome

Run the same protocol with exactly five representative users. Without assistance, each participant
must attempt to register a shared expense, consult the monthly remaining amount and review an audio
proposal. Record anonymous completion results per participant and per flow; SC-010 passes only when
at least four of the five participants complete all three flows.

## Persistence and secret review

1. Create the full confirmed dataset: account, board, guest, expense, monthly budget, initial
   savings and USD purchase.
2. Stop and restart the backend with the same SQLite file; confirm every value remains unchanged.
3. Inspect stored authentication data and captured logs. Passwords, JWTs, raw reset/invitation
   codes, SMTP credentials, audio and transcripts must not appear in plaintext.
4. Ensure `.env`, database files, audio fixtures containing private recordings and model caches are
   excluded from version control as appropriate. The fixed evaluation corpus must contain only
   consented, non-sensitive test audio.
