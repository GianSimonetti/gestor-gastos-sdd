# Phase 0 Research: Gestor de Gastos MVP

**Date**: 2026-10-15
**Status**: Complete — no unresolved technical clarifications

## 1. Backend architecture

**Decision**: Use a synchronous modular monolith with FastAPI, SQLAlchemy ORM 2.x and the standard
SQLite driver. Keep four concrete responsibilities: HTTP adapters, application use cases, pure
domain rules, and infrastructure adapters.

**Rationale**: SQLite serializes writes and the MVP has no requirement for distributed execution.
Synchronous request-scoped transactions are easier to reason about and test. The separation keeps
critical rules independent without introducing a framework-heavy domain architecture.

**Alternatives considered**:

- Async FastAPI with `aiosqlite`: rejected because it adds coordination complexity without
  improving SQLite write concurrency.
- Microservices, CQRS, event bus or worker queue: rejected because no spec requirement justifies
  independent deployment or eventual consistency.
- Routers calling ORM models directly: rejected because it would mix transport, authorization and
  critical financial rules.

## 2. Exact monetary representation

**Decision**: Exchange money through HTTP as canonical decimal strings with two fractional digits,
parse them from strings with Python `Decimal`, convert immediately to integer cents, and persist and
calculate exclusively with integer cents. Frontend helpers use strings and `BigInt` only for input
feedback; server results remain authoritative.

**Rationale**: Integer cents make equality, summation and SQLite persistence exact. Equal splitting
uses `divmod(total_cents, count)` and gives one residual cent to each of the first people in stable
selection order. Custom parts are accepted only when every part is non-negative and their integer
sum equals the total.

**Alternatives considered**:

- Binary floating point: rejected by the constitution and because it cannot represent every cent
  exactly.
- SQLite `NUMERIC` plus Python `Decimal`: rejected because SQLite uses dynamic type affinity;
  integer minor units give a stronger invariant.
- A JavaScript decimal library: rejected because the frontend does not own final calculations and
  `BigInt` is sufficient for cents.

## 3. Persistence and transaction boundaries

**Decision**: Use one SQLAlchemy `Session` per request and one explicit transaction per mutating use
case. Repositories never commit. Enable SQLite foreign keys, modern transaction control, WAL and a
bounded busy timeout on every connection. Derive summaries and debts from confirmed movements
instead of storing duplicated totals.

**Rationale**: Atomic use cases prevent partial expenses, shares or membership records. Derived
queries eliminate synchronization bugs after edit or deletion. SQLAlchemy documents explicit
session transaction scopes, while its SQLite documentation notes that Python 3.12 otherwise uses
legacy transaction behavior and that foreign-key enforcement must be enabled.

**Alternatives considered**:

- Persisting monthly totals and debts: rejected because every mutation would need fragile
  multi-record synchronization.
- In-memory SQLite for integration tests: rejected because its pooling/connection behavior differs
  from a file database.
- Alembic in the initial greenfield MVP: deferred to the first schema evolution; `create_all` is
  sufficient for the single initial schema but MUST NOT be used to alter a populated schema.

**Sources**: [SQLAlchemy SQLite](https://docs.sqlalchemy.org/en/20/dialects/sqlite.html),
[SQLAlchemy transactions](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html)

## 4. Person and membership model

**Decision**: Use `board_people` as the common identity referenced by payers and shares. A row is
either linked to a user account through a membership or represents a guest participant. Retiring a
guest changes its state to inactive; historical expense references remain intact.

**Rationale**: A single person foreign key avoids polymorphic payer/share references and guarantees
that members and guests follow the same distribution rules. Account names come from the user;
email is returned only where homonyms require disambiguation.

**Alternatives considered**:

- Separate member and guest foreign keys on each share: rejected because it doubles constraints
  and complicates every query.
- Copying names into each expense: rejected because it duplicates mutable display data and weakens
  identity.

## 5. Authentication, logout and password security

**Decision**: Sign 30-minute HS256 JWT access tokens with PyJWT using an environment-provided
secret and fixed algorithm, then place them in `HttpOnly`, `SameSite=Lax` cookies (`Secure` outside
local development). Persist a session row keyed by JWT `jti`; every protected request verifies both
signature/claims and non-revoked session. Logout revokes that session and clears the cookie.
Passwords use Argon2 through `pwdlib[argon2]`.

**Rationale**: Session lookup provides immediate logout, which a purely stateless token cannot.
Short-lived access without refresh tokens minimizes the MVP attack surface. FastAPI's official JWT
guide uses PyJWT, recommends Argon2 through pwdlib and stresses password hashing rather than
plaintext storage.

**Alternatives considered**:

- JWT in `localStorage`: rejected because JavaScript-readable storage increases token exposure.
- Stateless JWT only: rejected because logout could not invalidate a captured token immediately.
- Refresh tokens: rejected because they add rotation and revocation flows absent from the spec.
- Asymmetric signing: rejected because a single service does not need distributed verification.

**Source**: [FastAPI OAuth2/JWT tutorial](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)

## 6. Password recovery email

**Decision**: Generate a 32-byte opaque token, send the raw value once in an HTTPS reset link, and
store only its SHA-256 digest with `expires_at` and `used_at`. Reset atomically consumes it after 30
minutes, updates the password hash and revokes the user's sessions. Deliver through a small
`EmailSender` port and an environment-configured TLS SMTP adapter built with Python's standard
library. Tests use an in-memory fake.

**Rationale**: SMTP is the only external facility strictly required by the email requirement and
does not tie the product to a vendor SDK. A hashed one-time token prevents database disclosure from
yielding a usable reset link. The recovery request always returns the same generic response to
avoid account enumeration.

**Alternatives considered**:

- Store raw reset tokens: rejected as unnecessary exposure.
- Add a vendor-specific mail SDK: rejected because standard SMTP satisfies the contract.
- Durable worker/queue: rejected for the MVP; a bounded in-process background send and explicit
  retry request are sufficient, with delivery failure logged without email or token contents.

**Source**: [Python 3.12 `smtplib`](https://docs.python.org/3.12/library/smtplib.html)

## 7. Invitation codes

**Decision**: Keep one invitation state per board with issue/expiry timestamps and a random nonce.
Derive the displayed code deterministically with HMAC using an environment secret, so the same code
can be reproduced throughout its 7-day validity without storing a reusable bearer value. Expiry
rotates the nonce on the next member request. Joining is idempotent under a unique membership
constraint.

**Rationale**: This satisfies the clarification that repeated requests return the same current
code, while avoiding plaintext storage. HMAC validation also rejects tampering before membership is
created.

**Alternatives considered**:

- Store the invitation code in plaintext: simpler but exposes a still-valid access capability if
  the database is read.
- Store only a random digest: secure, but cannot return the same current code to members.
- One code per invited person: rejected because the spec defines one reusable board code.

## 8. Audio transcription and deterministic extraction

**Decision**: Capture audio with `MediaRecorder`, with file capture as fallback, and process a
maximum 60-second/15-MB file synchronously. Transcribe locally with pinned `faster-whisper` model
`small`, CPU `int8`, Spanish language, loaded once per process. A pure deterministic extractor maps
the transcript to the fixed category catalog, Argentine monetary expressions, dates, expense type
and board people. Missing or ambiguous values remain explicit; neither audio nor proposal is
persisted after the response.

**Rationale**: Local inference avoids an operational AI service and preserves privacy. The `small`
model fits the 4-GB target according to the project's published CPU benchmark. Deterministic
extraction keeps the same transcript and board context repeatable, while mandatory review mitigates
speech-recognition errors.

**Alternatives considered**:

- Browser Web Speech API: rejected because support and behavior are inconsistent across the fixed
  mobile matrix.
- Remote speech/LLM API: rejected because it adds credentials, cost and a service dependency before
  the local approach has failed the required 12/20 evaluation.
- Local generative model for extraction: rejected because rule-based extraction is smaller,
  deterministic and adequate for the fixed fields.
- Distributed job queue: rejected because no audio latency target requires asynchronous jobs.

**Sources**: [`faster-whisper`](https://github.com/SYSTRAN/faster-whisper),
[MDN MediaRecorder](https://developer.mozilla.org/en-US/docs/Web/API/MediaRecorder)

## 9. Frontend structure and dependencies

**Decision**: Use React with JavaScript and Vite, React Router for public/protected routes, native
`fetch`, local `useState`/`useReducer`, and Context only for the authenticated account and selected
board. Use semantic HTML and mobile-first CSS. Render category totals as accessible horizontal bars
plus a textual list; do not add a chart library.

**Rationale**: The app has enough routes to justify a maintained router, but its data volume does
not justify Redux, a server-cache framework, a UI kit or a form library. A shared expense draft
reducer supports manual entry and audio review without duplicating their data model.

**Alternatives considered**:

- Hand-written routing: rejected because it duplicates URL parameter, history and fallback logic.
- Redux/Zustand/TanStack Query: rejected because explicit reload after mutations is simpler and
  avoids a second financial source of truth.
- Recharts/Chart.js: rejected because one category chart can be accessible with HTML/CSS.

**Source**: [React build tools](https://react.dev/learn/build-a-react-app-from-scratch)

## 10. Concurrency and HTTP contracts

**Decision**: Add integer `version` fields to mutable resources. Update/delete requests carry the
observed version; stale writes return `409 conflict` and the client reloads instead of silently
overwriting. Publish an OpenAPI 3.1 contract with JSON for normal operations and multipart only for
audio. Dates use ISO `YYYY-MM-DD`, periods `YYYY-MM`, amounts decimal strings, and errors a uniform
`code/message/field_errors` shape.

**Rationale**: Optimistic concurrency handles rare collisions without locks or distributed
coordination. Explicit representations preserve money and date meaning across JavaScript/Python.

**Alternatives considered**:

- Last-write-wins: rejected because simultaneous edits could silently erase confirmed changes.
- Pessimistic row locks: unsupported as a useful cross-request pattern in SQLite and unnecessary
  for expected contention.
- GraphQL: rejected because resource-oriented operations and generated FastAPI documentation are
  sufficient.

## 11. Test and validation strategy

**Decision**: Apply red-green-refactor to pure domain rules first, then application services,
file-backed SQLite integration tests and HTTP contract tests. Maintain a frozen manifest of 20
Argentine Spanish audio fixtures with hashes and expected values. Keep audio evaluation and the
100-login performance scenario opt-in so the fast suite stays deterministic.

**Rationale**: The layers match the constitution's test-first requirement and expose failures at
the smallest responsible boundary. File-backed SQLite exercises the same constraints and
transaction behavior as runtime. Injected clock, transcriber and email sender make security and
failure scenarios deterministic.

**Alternatives considered**:

- Mock every repository: rejected because authorization and transaction invariants need real
  database coverage.
- Add Hypothesis, Locust or a browser automation framework immediately: deferred because
  parametrized pytest, `httpx` and the required manual mobile matrix cover current acceptance
  without extra dependencies.

## 12. Operational signals

**Decision**: Use Python structured application logs with request correlation ID, route, outcome,
duration and non-sensitive error code. Never log JWTs, reset/invitation codes, passwords, full
emails, audio content or transcripts. Log audio/SMTP failures and SQLite lock conflicts; expose a
simple health endpoint that checks process and database reachability.

**Rationale**: These signals are sufficient to diagnose MVP failures without introducing a
telemetry platform or retaining sensitive content.

**Alternatives considered**:

- Metrics/tracing platform: deferred until usage justifies another service.
- Logging request/response bodies: rejected because they can contain financial and authentication
  data.
