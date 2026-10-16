---

description: "Dependency-ordered implementation tasks for Gestor de Gastos MVP"
---

# Tasks: Gestor de Gastos MVP

**Input**: Design documents from `/specs/001-gestor-gastos-mvp/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/openapi.yaml`, `quickstart.md`

**Tests**: Backend tests are mandatory because the constitution requires test-first development for monetary calculations, distributions, monthly availability, permissions and domain validations. Within every applicable phase, create the listed failing tests before the corresponding implementation and preserve red-green evidence in the task/commit history.

**Organization**: Tasks are grouped by user story so each story can be implemented and validated as an independently demonstrable increment. US9 is consolidated after all board resource families because its acceptance boundary spans P1 and P2 resources; authorization primitives and negative tests are still introduced test-first in Foundation and each earlier story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel because it changes different files and has no dependency on another incomplete task in the same group.
- **[Story]**: Maps the task to the corresponding story in `spec.md`.
- Every task names the file or directory it changes.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initialize the two-project repository and its deterministic local toolchain.

- [ ] T001 Initialize the Python 3.12 backend with FastAPI, Pydantic, SQLAlchemy 2.x, PyJWT, `pwdlib[argon2]`, `faster-whisper`, pytest and httpx dependencies plus pytest markers `audio_eval` and `performance` in `backend/pyproject.toml`
- [ ] T002 [P] Initialize the React JavaScript frontend with React, React DOM, React Router and Vite scripts for `dev` and `build` in `frontend/package.json`, `frontend/vite.config.js`, and `frontend/index.html`
- [ ] T003 [P] Create backend package markers matching the planned modular structure under `backend/app/api/`, `backend/app/application/`, `backend/app/domain/`, `backend/app/db/`, `backend/app/infrastructure/`, and `backend/app/core/`
- [ ] T004 [P] Create frontend entry points and feature directories under `frontend/src/app/`, `frontend/src/pages/`, `frontend/src/features/`, `frontend/src/components/`, `frontend/src/lib/`, and `frontend/src/styles/`
- [ ] T005 [P] Document non-secret local configuration keys and safe defaults in `.env.example` without adding any credential values
- [ ] T006 [P] Exclude `.env`, SQLite databases, temporary audio, private audio fixtures, Python/Node build artifacts and local model caches in `.gitignore`

**Checkpoint**: `uv sync` and `npm install` can materialize the declared projects without adding unapproved services or frameworks.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Establish exact money, deterministic time, persistence, errors, HTTP plumbing and the shared responsive shell required by every story.

**⚠️ CRITICAL**: No user story implementation starts until this phase is complete.

- [ ] T007 [P] Implement validated environment settings for database, JWT, invitation, timezone, frontend origin, reset URL, email and local Whisper configuration in `backend/app/core/config.py`
- [ ] T008 [P] Implement injectable UTC and `America/Argentina/Buenos_Aires` clocks for deterministic instants and omitted calendar dates in `backend/app/core/clock.py`
- [ ] T009 Write failing file-backed SQLite integration tests for foreign-key enforcement, explicit rollback, WAL/busy-timeout configuration and persistence after engine recreation in `backend/tests/integration/test_database.py`
- [ ] T010 Implement SQLAlchemy metadata, SQLite connection pragmas and request-scoped session/transaction lifecycle without repository commits in `backend/app/db/base.py` and `backend/app/db/session.py`
- [ ] T011 Write failing unit tests for canonical two-decimal parsing, rejection of `float`, integer-cent conversion, formatting, addition and subtraction across positive, zero and negative results in `backend/tests/unit/test_money.py`
- [ ] T012 Implement the exact Money boundary using string/Decimal parsing and integer-cent calculations only in `backend/app/domain/money.py`
- [ ] T013 [P] Write failing API tests for the uniform `code/message/field_errors` error shape and non-disclosing unavailable-resource response in `backend/tests/api/test_errors.py`
- [ ] T014 Implement domain exceptions and FastAPI exception mappings for validation, authentication, unavailable resources and stale versions in `backend/app/domain/errors.py` and `backend/app/api/dependencies.py`
- [ ] T015 Define repository protocols and SQLAlchemy implementations that accept a session, scope board resource lookups by both resource ID and board ID, and never commit independently in `backend/app/infrastructure/repositories.py`
- [ ] T016 [P] Implement credentialed native-fetch handling, uniform API errors and 401 session reset behavior in `frontend/src/lib/api.js`
- [ ] T017 [P] Implement non-authoritative string/BigInt money input helpers and Argentina date/month formatting helpers in `frontend/src/lib/money.js` and `frontend/src/lib/dates.js`
- [ ] T018 Build the FastAPI app factory, database-backed `/health`, correlation-ID structured logging with sensitive-body exclusion, React app shell, base router and mobile-first global styles in `backend/app/main.py`, `frontend/src/main.jsx`, `frontend/src/app/App.jsx`, `frontend/src/app/router.jsx`, and `frontend/src/styles/global.css`

**Checkpoint**: Foundation is ready; exact monetary primitives are green, the database transaction tests pass, and story work may begin.

---

## Phase 3: User Story 1 — Acceder de forma segura (Priority: P1) 🎯 MVP

**Goal**: Register, authenticate, revoke sessions and recover access without exposing credentials.

**Independent Test**: Register a unique account, log in and reload with its HttpOnly cookie, log out and lose protected access, then use a one-time 30-minute reset link so the old password and every prior session fail while the new password succeeds.

### Tests for User Story 1 — write and observe failure first

- [ ] T019 [P] [US1] Write failing unit tests for Argon2 password hashing, fixed-algorithm JWT claim validation, 30-minute expiry and raw-secret exclusion in `backend/tests/unit/test_security.py`
- [ ] T020 [P] [US1] Write failing integration tests for unique normalized email, persisted/revoked AuthSession state and atomic one-time PasswordResetToken consumption in `backend/tests/integration/test_auth_persistence.py`
- [ ] T021 [P] [US1] Write failing API contract tests for register, login, logout, `/auth/me`, enumeration-safe recovery, valid/expired/reused reset and cookie attributes in `backend/tests/api/test_auth.py`

### Implementation for User Story 1

- [ ] T022 [US1] Map User (`id`: "Immutable primary key"; `display_name`: "Trimmed, 1–100 characters"; `email`: "Trimmed, normalized to lowercase for identity; globally unique"; `password_hash`: "Argon2 hash only; never returned"; `created_at`: "Set on registration"), AuthSession (`id / jti`: "Primary key and JWT jti"; `user_id`: "FK to User; indexed"; `issued_at`: "Matches JWT iat"; `expires_at`: "30 minutes after issue"; `revoked_at`: "Set by logout or password reset" when present) and PasswordResetToken (`id`: "Primary key"; `user_id`: "FK to User; indexed"; `token_digest`: "SHA-256 digest; unique; raw token never stored"; `created_at`: "Issue instant"; `expires_at`: "Exactly 30 minutes after issue"; `used_at`: "Set atomically on successful reset" when present) in `backend/app/db/models.py`
- [ ] T023 [P] [US1] Implement Argon2 hashing, 30-minute HS256 JWT creation/verification with fixed issuer/audience/algorithm and secure random reset-token digesting in `backend/app/core/security.py`
- [ ] T024 [P] [US1] Define auth request/response schemas with display-name 1–100, normalized valid email and password minimum 8 characters in `backend/app/api/schemas/auth.py`
- [ ] T025 [P] [US1] Define the `EmailSender` port plus in-memory and TLS SMTP adapters that never log email, password or raw token content in `backend/app/infrastructure/email.py`
- [ ] T026 [US1] Implement registration, login, session lookup/revocation, enumeration-safe recovery and atomic reset that revokes all sessions and unused tokens in `backend/app/application/auth_service.py`
- [ ] T027 [US1] Implement `/auth/register`, `/auth/login`, `/auth/logout`, `/auth/me`, `/auth/password-recovery` and `/auth/password-reset` with HttpOnly SameSite=Lax cookies and Secure outside local development in `backend/app/api/routers/auth.py`
- [ ] T028 [US1] Register the auth router and inject session, clock and email dependencies in `backend/app/main.py` and `backend/app/api/dependencies.py`
- [ ] T029 [P] [US1] Implement the frontend auth API adapter without exposing JWTs to JavaScript in `frontend/src/features/auth/api.js`
- [ ] T030 [P] [US1] Build labeled registration and login forms with field-associated errors in `frontend/src/features/auth/RegisterForm.jsx` and `frontend/src/features/auth/LoginForm.jsx`
- [ ] T031 [P] [US1] Build enumeration-safe recovery and reset forms in `frontend/src/features/auth/RecoveryForm.jsx` and `frontend/src/features/auth/ResetPasswordForm.jsx`
- [ ] T032 [US1] Implement authenticated-account context, protected routes, refresh-safe `/auth/me` loading and logout navigation in `frontend/src/features/auth/AuthContext.jsx`, `frontend/src/features/auth/ProtectedRoute.jsx`, and `frontend/src/app/router.jsx`

**Checkpoint**: US1 passes independently and supplies authenticated identity to later stories.

---

## Phase 4: User Story 2 — Compartir un tablero (Priority: P1)

**Goal**: Create boards, retrieve a reusable seven-day invitation code and join a board idempotently.

**Independent Test**: Create Hogar as one account, obtain the same valid code repeatedly, join with a second account once, then advance beyond seven days and verify rotation and rejection of the old code.

### Tests for User Story 2 — write and observe failure first

- [ ] T033 [P] [US2] Write failing unit tests for deterministic HMAC invitation derivation, tamper rejection, seven-calendar-day validity and nonce rotation in `backend/tests/unit/test_invitations.py`
- [ ] T034 [P] [US2] Write failing integration tests for atomic board/member/account-person creation, unique membership, idempotent joining and concurrent invitation rotation in `backend/tests/integration/test_boards.py`
- [ ] T035 [P] [US2] Write failing API tests for board list/create/detail, invitation retrieval, join and authenticated non-member denial in `backend/tests/api/test_boards.py`

### Implementation for User Story 2

- [ ] T036 [US2] Map Board (`id`: "Immutable primary key"; `name`: "Trimmed, 1–100 characters; need not be globally unique"; `created_at`: "Creation instant"), Membership (`id`: "Primary key"; `board_id`: "FK to Board"; `user_id`: "FK to User"; `joined_at`: "Creation/join instant"; unique `(board_id, user_id)`), BoardPerson (`id`: "Primary key"; `board_id`: "FK to Board; part of board-scope constraints"; `kind`: "account or guest"; `user_id`: "Required and unique per board for account; null for guest"; `guest_name`: "Required, trimmed 1–100 chars for guest; null for account"; `active`: "Defaults true; account persons remain active while membership exists"; `version`: "Optimistic concurrency token"; `created_at`: "Creation instant"; `retired_at`: "Set only when a guest is retired" when present), and BoardInvitationState (`board_id`: "PK/FK to Board; one-to-one"; `nonce`: "Rotated after expiry"; `issued_at`: "Start of validity"; `expires_at`: "Seven calendar days after issue"; `version`: "Protects concurrent rotation") in `backend/app/db/models.py`
- [ ] T037 [P] [US2] Define board, invitation and join schemas matching the OpenAPI decimal-free board contracts in `backend/app/api/schemas/boards.py`
- [ ] T038 [US2] Implement atomic board creation, board listing/detail, membership checks, stable invitation retrieval/rotation and idempotent joining in `backend/app/application/board_service.py`
- [ ] T039 [US2] Implement `/boards`, `/boards/join`, `/boards/{boardId}` and `/boards/{boardId}/invitation-code` in `backend/app/api/routers/boards.py`
- [ ] T040 [P] [US2] Implement board API calls and selected-board context in `frontend/src/features/boards/api.js` and `frontend/src/features/boards/BoardContext.jsx`
- [ ] T041 [P] [US2] Build board list/create/join views with invalid and expired-code feedback in `frontend/src/pages/BoardsPage.jsx`
- [ ] T042 [P] [US2] Build the board header and invitation-code sharing panel with expiry display in `frontend/src/features/boards/BoardHeader.jsx` and `frontend/src/features/boards/InvitationPanel.jsx`
- [ ] T043 [US2] Add authenticated board routes and selected-board loading to `frontend/src/app/router.jsx`

**Checkpoint**: Two accounts can independently establish and share one board without duplicate membership.

---

## Phase 5: User Story 3 — Administrar personas del tablero (Priority: P1)

**Goal**: Create, rename, list and retire guest participants while preserving historical identity.

**Independent Test**: Add Ana, rename her to Ana Pérez, use her in a fixture expense, retire her, and verify she is absent from new choices but still present in historical detail; repeat with homonyms to verify stable-ID/email disambiguation.

### Tests for User Story 3 — write and observe failure first

- [ ] T044 [P] [US3] Write failing integration tests for guest active→retired lifecycle, optimistic version conflicts, homonyms and preserved historical references in `backend/tests/integration/test_people.py`
- [ ] T045 [P] [US3] Write failing API tests for list/create/rename/retire, account-person mutation rejection and cross-board non-disclosure in `backend/tests/api/test_people.py`

### Implementation for User Story 3

- [ ] T046 [US3] Add database invariants for BoardPerson so account requires unique-per-board `user_id` and null `guest_name`, guest requires null `user_id` and "Required, trimmed 1–100 chars" `guest_name`, retired guests set `retired_at`, and no reactivation path exists in `backend/app/db/models.py`
- [ ] T047 [P] [US3] Define people schemas that expose stable IDs, active state, kind and account email only for disambiguation in `backend/app/api/schemas/people.py`
- [ ] T048 [US3] Implement authorized guest creation, rename and retirement plus active-choice and historical lookup semantics in `backend/app/application/board_service.py`
- [ ] T049 [US3] Implement `/boards/{boardId}/people` and `/boards/{boardId}/people/{personId}` operations with version conflicts in `backend/app/api/routers/people.py`
- [ ] T050 [US3] Build participant list/create/rename/retire UI and reusable person selector labels in `frontend/src/features/people/PeoplePanel.jsx` and `frontend/src/features/people/PersonSelect.jsx`

**Checkpoint**: Guest participant lifecycle is independently usable and historical references remain stable.

---

## Phase 6: User Story 4 — Registrar y distribuir gastos (Priority: P1)

**Goal**: Create personal, equal and custom ARS expenses with exact shares, deterministic residual cents and derived debts.

**Independent Test**: Create each expense type, repeatedly split ARS 100,00 among three people in one order, confirm exact sums/debts, and reject negative, over-precision, duplicate, empty, retired and cross-board inputs without partial persistence.

### Tests for User Story 4 — write and observe failure first

- [ ] T051 [P] [US4] Write failing unit tests for personal assignment to payer, equal `divmod` splitting, stable residual order, custom exact sums, debts and all invalid distribution variants in `backend/tests/unit/test_expenses.py`
- [ ] T052 [P] [US4] Write failing integration tests for atomic Expense/ExpenseShare creation, same-board/active-person constraints, Argentina default date and rollback on invalid shares in `backend/tests/integration/test_expenses.py`
- [ ] T053 [P] [US4] Write failing API tests for expense creation/detail shapes, canonical money strings, fixed categories and cross-board participant rejection in `backend/tests/api/test_expenses_create.py`

### Implementation for User Story 4

- [ ] T054 [US4] Implement pure personal/equal/custom distribution validation and debt derivation using integer cents and stable zero-based selection order in `backend/app/domain/expenses.py`
- [ ] T055 [US4] Map Expense (`id`: "Primary key"; `board_id`: "FK to Board; indexed with expense_date"; `name`: "Trimmed, 1–150 characters"; `amount_ars_cents`: "Greater than 0"; `category`: `food|transport|housing|services|health|education|leisure|other`; `expense_date`: "Supplied or defaulted in Argentina timezone"; `payer_person_id`: "Active BoardPerson in same board at creation/edit"; `expense_type`: `personal|equal|custom`; `description`: "Trimmed; maximum 1000 characters" when present; `version`: "Optimistic concurrency token"; `created_at`: "Creation instant"; `updated_at`: "Last successful update") and ExpenseShare (`id`: "Primary key"; `expense_id`: "FK to Expense; cascade on expense deletion"; `board_id`: "Matches Expense and BoardPerson board"; `person_id`: "FK to BoardPerson in same board"; `amount_ars_cents`: "Greater than or equal to 0"; `selection_order`: "Zero-based, unique inside expense"; unique `(expense_id, person_id)` and `(expense_id, selection_order)`) in `backend/app/db/models.py`
- [ ] T056 [P] [US4] Define expense input/output, exact share, debt, category and type schemas using canonical decimal strings in `backend/app/api/schemas/expenses.py`
- [ ] T057 [US4] Implement authorized atomic expense creation, domain validation, person lookup and derived share/debt presentation in `backend/app/application/expense_service.py`
- [ ] T058 [US4] Implement POST `/boards/{boardId}/expenses` and the initial GET detail operation in `backend/app/api/routers/expenses.py`
- [ ] T059 [P] [US4] Implement the shared manual/audio expense draft reducer without authoritative calculations in `frontend/src/features/expenses/expenseDraftReducer.js`
- [ ] T060 [P] [US4] Build the responsive expense form for all fields/types with ordered participants, exact custom shares and field-associated errors in `frontend/src/features/expenses/ExpenseForm.jsx`
- [ ] T061 [P] [US4] Build exact share and debt presentation in `frontend/src/features/expenses/ExpenseDistribution.jsx`
- [ ] T062 [US4] Expose new-expense entry from the board home in one interaction and wire successful creation/reload in `frontend/src/pages/BoardPage.jsx` and `frontend/src/pages/NewExpensePage.jsx`

**Checkpoint**: The central expense flow is independently functional and all deterministic money tests are green.

---

## Phase 7: User Story 5 — Consultar y corregir gastos (Priority: P1)

**Goal**: List, inspect, edit and confirm deletion of expenses while recalculating all derived views.

**Independent Test**: Create one expense, inspect list/detail, edit amount/date/distribution with its version, observe affected summaries, reject a stale edit, then confirm deletion and verify it disappears with no residual shares.

### Tests for User Story 5 — write and observe failure first

- [ ] T063 [P] [US5] Write failing integration tests for paginated/ordered queries, atomic share replacement, stale update/delete conflicts and cascade deletion in `backend/tests/integration/test_expense_mutations.py`
- [ ] T064 [P] [US5] Write failing API tests for list/detail/update/delete contracts, confirmation-version input, pagination bounds and unavailable foreign-board IDs in `backend/tests/api/test_expense_crud.py`

### Implementation for User Story 5

- [ ] T065 [US5] Add scoped paginated queries and version-checked atomic update/delete operations to `backend/app/application/expense_service.py`
- [ ] T066 [US5] Complete GET collection/detail, PUT and DELETE expense routes with uniform 409 handling in `backend/app/api/routers/expenses.py`
- [ ] T067 [P] [US5] Implement list/detail/update/delete API calls and conflict-triggered reload in `frontend/src/features/expenses/api.js`
- [ ] T068 [P] [US5] Build paginated expense list, empty/loading/error states and stable detail links in `frontend/src/features/expenses/ExpenseList.jsx`
- [ ] T069 [P] [US5] Build expense detail and edit views reusing exact distribution controls in `frontend/src/pages/ExpenseDetailPage.jsx` and `frontend/src/pages/EditExpensePage.jsx`
- [ ] T070 [P] [US5] Build an accessible destructive confirmation dialog that requires explicit confirmation in `frontend/src/components/ConfirmDialog.jsx`
- [ ] T071 [US5] Wire expense list/detail/edit/delete routes and refresh affected board data after mutation in `frontend/src/app/router.jsx`

**Checkpoint**: Expense history can be corrected without duplicate or stale financial state.

---

## Phase 8: User Story 7 — Controlar el disponible mensual (Priority: P1)

**Goal**: Define a monthly ARS base and derive category totals, consumed and nullable/negative remaining values.

**Independent Test**: Query a month without a base, add expenses and ARS spent on USD purchases, set/edit a base, move/delete movements across months and verify exact category, consumed and remaining results including null and negative cases.

### Tests for User Story 7 — write and observe failure first

- [ ] T072 [P] [US7] Write failing unit tests for category aggregation, consumed-from-total-not-shares, purchase ARS inclusion, absent-base null remaining and negative remaining in `backend/tests/unit/test_monthly.py`
- [ ] T073 [P] [US7] Write failing integration tests for unique board/year/month budgets, integer version conflicts and month-boundary queries in Argentina dates in `backend/tests/integration/test_monthly.py`
- [ ] T074 [P] [US7] Write failing API tests for budget upsert and monthly summary, canonical signed money and cross-board denial in `backend/tests/api/test_monthly.py`

### Implementation for User Story 7

- [ ] T075 [US7] Implement pure category-total, consumed and remaining derivations without persisted aggregates in `backend/app/domain/monthly.py`
- [ ] T076 [US7] Map MonthlyBudget (`id`: "Primary key"; `board_id`: "FK to Board"; `year`: "Four-digit supported calendar year"; `month`: "1–12"; `base_ars_cents`: "Greater than or equal to 0"; `version`: "Optimistic concurrency token"; `created_at`: "Creation instant"; `updated_at`: "Last update"; unique `(board_id, year, month)`) in `backend/app/db/models.py`
- [ ] T077 [P] [US7] Define monthly budget and summary schemas with `remaining_ars` nullable when no base exists in `backend/app/api/schemas/monthly.py`
- [ ] T078 [US7] Implement authorized versioned budget upsert and on-demand monthly summary queries in `backend/app/application/monthly_service.py`
- [ ] T079 [US7] Implement `/boards/{boardId}/months/{month}/budget` and `/boards/{boardId}/months/{month}/summary` in `backend/app/api/routers/monthly.py`
- [ ] T080 [US7] Build month selection, budget editing, textual/category-bar summary and explicit “no disponible”/negative states in `frontend/src/features/monthly/MonthlyDashboard.jsx` and `frontend/src/features/monthly/CategoryBars.jsx`

**Checkpoint**: Monthly control is independently usable and remains exact after current expense mutations.

---

## Phase 9: User Story 6 — Cargar un gasto mediante audio (Priority: P2)

**Goal**: Capture or upload audio, produce a transient editable proposal and create an expense only after normal explicit confirmation.

**Independent Test**: Process complete, incomplete, silent, ambiguous, unsupported, oversized and failed-transcription inputs; verify no financial mutation until the edited proposal is submitted through the standard expense endpoint.

### Tests for User Story 6 — write and observe failure first

- [ ] T081 [P] [US6] Write failing unit tests for deterministic Argentine amount/date/category/type/person extraction, homonym ambiguities and explicit missing fields in `backend/tests/unit/test_speech_extractor.py`
- [ ] T082 [P] [US6] Write failing service tests with a fake transcriber for 60-second/15-MB limits, cleanup after success/failure and no proposal persistence in `backend/tests/unit/test_audio_service.py`
- [ ] T083 [P] [US6] Write failing API tests for multipart audio proposals, formats/errors, membership denial and confirmation only through POST expenses in `backend/tests/api/test_audio.py`

### Implementation for User Story 6

- [ ] T084 [P] [US6] Implement the local `faster-whisper` small/CPU/int8 Spanish transcriber loaded once per process with local-only model access in `backend/app/infrastructure/transcription.py`
- [ ] T085 [P] [US6] Implement the pure repeatable transcript extractor for the fixed catalog, monetary expressions, dates, expense type and board-person candidates in `backend/app/infrastructure/speech_extractor.py`
- [ ] T086 [P] [US6] Define transient AudioProposal fields (`transcript`: "Used for review; not logged or persisted"; extracted optional `name`; canonical optional `amount_ars`; fixed-catalog optional `category`; `expense_date`: "Extracted/defaulted only when unambiguous"; extracted optional `description`/`expense_type`; `payer_person_id`: "Only when exactly matched in board context"; stable-order optional `participant_person_ids`; optional `custom_shares`; required `missing_fields`, `ambiguities`, and `warnings`) without any persistence model in `backend/app/api/schemas/audio.py`
- [ ] T087 [US6] Implement authorized temporary-file validation, transcription, extraction and `finally` cleanup without logging audio/transcripts in `backend/app/application/audio_service.py`
- [ ] T088 [US6] Implement multipart POST `/boards/{boardId}/audio-proposals` with 15-MB/60-second and supported-format responses in `backend/app/api/routers/audio.py`
- [ ] T089 [P] [US6] Build MediaRecorder capture with visible requesting/recording/processing/error states, track cleanup and file-input fallback in `frontend/src/features/audio/AudioCapture.jsx`
- [ ] T090 [P] [US6] Build proposal review using the shared expense draft reducer, marking missing/ambiguous fields and permitting every field to be edited in `frontend/src/features/audio/AudioProposalReview.jsx`
- [ ] T091 [US6] Wire audio proposal confirmation to the normal expense creation API and cancellation to discard local state in `frontend/src/pages/AudioExpensePage.jsx` and `frontend/src/app/router.jsx`

**Checkpoint**: Audio assists entry without becoming an alternate financial write path.

---

## Phase 10: User Story 8 — Administrar ahorros en USD (Priority: P2)

**Goal**: Manage one initial USD balance and dated USD purchases whose ARS cost affects only the corresponding monthly consumption.

**Independent Test**: Create/edit/delete initial savings and purchases, move a purchase between months, reject stale versions and verify current USD total plus exact ARS impact without currency conversion.

### Tests for User Story 8 — write and observe failure first

- [ ] T092 [P] [US8] Write failing unit tests for USD total derivation and strict separation of USD quantities from ARS monthly consumption in `backend/tests/unit/test_savings.py`
- [ ] T093 [P] [US8] Write failing integration tests for single InitialSavings lifecycle, UsdPurchase persistence, Argentina default date, month movement, deletion and version conflicts in `backend/tests/integration/test_savings.py`
- [ ] T094 [P] [US8] Write failing API tests for savings summary, initial upsert/delete, paginated monthly purchases, purchase CRUD and cross-board denial in `backend/tests/api/test_savings.py`

### Implementation for User Story 8

- [ ] T095 [US8] Implement pure current-total and monthly-purchase calculations with separate integer-cent currencies and no conversion in `backend/app/domain/savings.py`
- [ ] T096 [US8] Map InitialSavings (`board_id`: "PK/FK to Board; enforces one current record"; `amount_usd_cents`: "Greater than or equal to 0"; `version`: "Optimistic concurrency token"; `created_at`: "Creation instant"; `updated_at`: "Last update") and UsdPurchase (`id`: "Primary key"; `board_id`: "FK to Board; indexed with purchase_date"; `amount_usd_cents`: "Greater than 0"; `ars_spent_cents`: "Greater than 0"; `purchase_date`: "Supplied or defaulted in Argentina timezone"; `version`: "Optimistic concurrency token"; `created_at`: "Creation instant"; `updated_at`: "Last update") in `backend/app/db/models.py`
- [ ] T097 [P] [US8] Define savings, purchase and paginated monthly response schemas with canonical USD/ARS strings in `backend/app/api/schemas/savings.py`
- [ ] T098 [US8] Implement authorized initial-savings lifecycle, purchase CRUD/filtering and derived totals using scoped repositories in `backend/app/application/savings_service.py`
- [ ] T099 [US8] Implement `/boards/{boardId}/savings`, `/savings/initial`, `/usd-purchases` and `/usd-purchases/{purchaseId}` operations in `backend/app/api/routers/savings.py`
- [ ] T100 [P] [US8] Implement savings API calls with version conflict reload in `frontend/src/features/savings/api.js`
- [ ] T101 [P] [US8] Build initial savings and total cards with create/edit/delete states in `frontend/src/features/savings/InitialSavingsCard.jsx`
- [ ] T102 [P] [US8] Build purchase list/month filter and exact USD/ARS purchase form in `frontend/src/features/savings/UsdPurchasePanel.jsx`
- [ ] T103 [US8] Wire savings routes and refresh monthly data after ARS-impacting purchase mutations in `frontend/src/pages/SavingsPage.jsx` and `frontend/src/app/router.jsx`

**Checkpoint**: Savings are independently manageable and never mix ARS and USD arithmetic.

---

## Phase 11: User Story 9 — Mantener aislamiento entre tableros (Priority: P1, consolidated after resource families)

**Goal**: Prove that every board-scoped read and mutation is authorized in the backend and never leaks or mutates foreign-board data.

**Independent Test**: With a valid non-member session, attempt every board, invitation, people, expense, monthly, savings and audio operation using valid foreign IDs; every attempt returns the uniform unavailable response, no payload data, and no state change.

### Tests for User Story 9 — write and observe failure first

- [ ] T104 [P] [US9] Write a parametrized cross-board API matrix covering every board-scoped operation and both foreign-valid/missing IDs in `backend/tests/api/test_board_isolation.py`
- [ ] T105 [P] [US9] Write integration tests proving every scoped repository filters by both resource ID and board ID and rolls back denied mutations in `backend/tests/integration/test_board_isolation.py`

### Implementation for User Story 9

- [ ] T106 [US9] Centralize `(board_id, actor_user_id)` membership proof and same-public-result resource lookup helpers, then replace any failing router/service checks found by T104–T105 in `backend/app/api/dependencies.py` and `backend/app/infrastructure/repositories.py`
- [ ] T107 [US9] Add regression cases for nested cross-board payer/share references, retired people and stale foreign versions to `backend/tests/api/test_board_isolation.py`

**Checkpoint**: The complete board boundary satisfies AC-47–AC-54 and FR-047 across every implemented resource family.

---

## Phase 12: User Story 10 — Conservar una experiencia confiable (Priority: P2)

**Goal**: Meet persistence, responsive/accessibility, credential protection, audio-quality and login-performance outcomes.

**Independent Test**: Recreate the process with one full confirmed dataset, run the fixed mobile/accessibility matrix, inspect storage/logs for secrets, pass at least 12/20 frozen audio cases and achieve at least 95/100 valid logins within four seconds after ten warmups at concurrency five on 2 vCPU/4 GB.

### Tests and evidence for User Story 10

- [ ] T108 [P] [US10] Write an end-to-end persistence test that recreates the engine and verifies account, membership, guest, expense/shares, monthly budget, initial savings and USD purchase values in `backend/tests/integration/test_restart_persistence.py`
- [ ] T109 [P] [US10] Create the consented 20-case Argentine Spanish audio manifest with SHA-256 hashes and expected present fields in `backend/tests/fixtures/audio-eval/manifest.json`
- [ ] T110 [US10] Implement the opt-in all-fields-match audio evaluation gate with a 12/20 threshold in `backend/tests/test_audio_evaluation.py`
- [ ] T111 [P] [US10] Implement the opt-in 10-warmup/100-login/concurrency-5 performance gate and percentile/result reporting for the fixed 2-vCPU/4-GB environment in `backend/tests/performance/test_login.py`
- [ ] T112 [P] [US10] Write security regression tests that scan persisted auth fields and captured logs for passwords, JWTs, raw reset/invitation codes, full emails, audio and transcripts in `backend/tests/integration/test_secret_exposure.py`

### Implementation for User Story 10

- [ ] T113 [P] [US10] Add reusable accessible form-error summary, first-invalid-field focus and 44×44-pixel control primitives in `frontend/src/components/FormErrorSummary.jsx` and `frontend/src/styles/accessibility.css`
- [ ] T114 [P] [US10] Harden responsive layouts at 360, 390, 768 and 1280 CSS pixels without horizontal page scrolling or clipped actions in `frontend/src/styles/responsive.css`
- [ ] T115 [US10] Apply semantic labels, keyboard/focus behavior, textual chart equivalents and visible loading/empty/error states across all routes listed in `frontend/src/app/router.jsx`
- [ ] T116 [US10] Record the five-user unassisted usability protocol and result template for shared expense, monthly remaining and audio review flows in `specs/001-gestor-gastos-mvp/usability-validation.md`

**Checkpoint**: The complete product has reproducible evidence for NFR-001–NFR-006 and SC-004–SC-010.

---

## Phase 13: Polish & Cross-Cutting Concerns

**Purpose**: Validate contract conformance, scope, quality gates and end-to-end readiness without adding product functionality.

- [ ] T117 [P] Add an OpenAPI conformance test for documented paths, methods, status codes, money/date formats and error schemas in `backend/tests/api/test_openapi_contract.py`
- [ ] T118 [P] Review dependencies and configuration for unrequested services, hardcoded secrets and prohibited financial integrations, documenting findings in `specs/001-gestor-gastos-mvp/security-review.md`
- [ ] T119 Run `uv run pytest -m "not audio_eval and not performance"`, then the explicit audio/performance gates, and record exact commands/results in `specs/001-gestor-gastos-mvp/validation-results.md`
- [ ] T120 Run `npm run build` and record the production build result in `specs/001-gestor-gastos-mvp/validation-results.md`
- [ ] T121 Execute every end-to-end scenario in `quickstart.md`, including Safari iOS 14 at 390×844 and Chrome Android 12 at 360×800, and record evidence in `specs/001-gestor-gastos-mvp/validation-results.md`
- [ ] T122 Reconcile implemented routes and schemas with `specs/001-gestor-gastos-mvp/contracts/openapi.yaml` and document any approved spec correction before release in `specs/001-gestor-gastos-mvp/validation-results.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Starts immediately.
- **Foundational (Phase 2)**: Depends on Setup and blocks every user story.
- **US1 (Phase 3)**: Starts after Foundation; supplies authenticated identity.
- **US2 (Phase 4)**: Depends on US1; supplies boards, memberships and account people.
- **US3 (Phase 5)**: Depends on US2; supplies guest people.
- **US4 (Phase 6)**: Depends on US2 and uses US3 when guests participate; it remains testable with account people alone.
- **US5 (Phase 7)**: Depends on US4.
- **US7 (Phase 8)**: Depends on US4 for expense consumption; purchase contribution becomes active when US8 lands.
- **US6 (Phase 9)**: Depends on US3 and US4 because it resolves people and confirms through normal expense creation.
- **US8 (Phase 10)**: Depends on US2 and the shared Money/date foundation; integrates with US7 summaries.
- **US9 (Phase 11)**: Authorization is enforced from Foundation onward, but final matrix completion depends on US2–US8 because FR-047 spans every board resource.
- **US10 (Phase 12)**: Depends on all functional stories selected for the release.
- **Polish (Phase 13)**: Depends on all desired stories and their checkpoints.

### User Story Dependency Graph

```text
Setup → Foundation → US1 → US2
                           ├─→ US3 ─→ US4 ─→ US5
                           │          ├─→ US7
                           │          └─→ US6
                           └─────────────→ US8 ─→ US7 integration

US2 + US3 + US4 + US5 + US6 + US7 + US8 → US9
US1…US9 → US10 → Polish
```

### Within Each Story

1. Create the listed tests and observe the relevant failures.
2. Add or extend persistence models before repository/application behavior.
3. Implement pure domain behavior before application services.
4. Implement services before HTTP routers.
5. Implement backend authority before frontend integration.
6. Pass the story tests and independent criterion before closing its checkpoint.

## Parallel Opportunities

- Setup tasks T002–T006 may proceed in parallel after T001 establishes the repository conventions.
- In Foundation, configuration/clock, API error tests and frontend helpers can proceed in parallel; T009→T010 and T011→T012 remain ordered red-green pairs.
- Within a story, tasks carrying `[P]` can proceed together only after all earlier non-parallel dependencies they consume are green.
- US6 and US8 can proceed in parallel after US4/US2 respectively; US9 waits for both resource families.
- Frontend work for a story may proceed against `contracts/openapi.yaml` while its backend services are completed, but integration waits for the route.

### Parallel Example: US1

```text
T019 security unit tests | T020 auth persistence tests | T021 auth API tests
T023 security implementation | T024 schemas | T025 email adapter
T030 register/login UI | T031 recovery/reset UI
```

### Parallel Example: US2

```text
T033 invitation tests | T034 board persistence tests | T035 board API tests
T040 board API/context | T041 boards page | T042 invitation panel
```

### Parallel Example: US3

```text
T044 people integration tests | T045 people API tests
T047 people schemas | T050 people UI after contract is stable
```

### Parallel Example: US4

```text
T051 distribution unit tests | T052 expense integration tests | T053 create API tests
T056 schemas | T059 draft reducer | T060 expense form | T061 distribution view
```

### Parallel Example: US5

```text
T063 mutation integration tests | T064 CRUD API tests
T067 frontend API | T068 list | T069 detail/edit | T070 confirmation dialog
```

### Parallel Example: US7

```text
T072 monthly unit tests | T073 budget integration tests | T074 monthly API tests
T077 schemas | T080 dashboard after the contract is stable
```

### Parallel Example: US6

```text
T081 extractor tests | T082 audio service tests | T083 audio API tests
T084 transcription adapter | T085 extractor | T086 schemas | T089 capture UI | T090 review UI
```

### Parallel Example: US8

```text
T092 savings unit tests | T093 savings integration tests | T094 savings API tests
T097 schemas | T100 frontend API | T101 initial card | T102 purchase panel
```

### Parallel Example: US9

```text
T104 complete HTTP isolation matrix | T105 repository scoping matrix
```

### Parallel Example: US10

```text
T108 restart persistence | T109 audio manifest | T111 login performance | T112 secret exposure
T113 accessibility primitives | T114 responsive styles
```

## Implementation Strategy

### Minimum Independently Demonstrable Increment

1. Complete Setup.
2. Complete Foundation.
3. Complete US1.
4. Stop and validate registration, session persistence, logout and recovery independently.

This is the smallest secure demonstrable increment. It is not the complete expense-management MVP.

### Core Expense MVP

1. Add US2 and US3 for the board/person boundary.
2. Add US4 for exact expense entry.
3. Add US5 for corrections.
4. Add US7 for monthly control.
5. Validate the applicable US9 isolation matrix.

### Full Spec Delivery

1. Add US6 and US8 independently after their prerequisites.
2. Complete the consolidated US9 matrix.
3. Complete US10 and all Polish gates.
4. Do not add roles, debt settlement, bank/wallet integrations, currency conversion, native apps or advanced category management.

## Notes

- `[P]` means file-level parallelism is safe; it does not waive logical prerequisites.
- Every user-story task uses its original `[USn]` identifier from `spec.md`, even when dependency order differs from document order.
- Critical tests must be committed or otherwise evidenced in their failing state before the paired implementation.
- The backend remains the source of truth for authorization, money, distribution and derived totals.
- Repositories never commit; each mutating application use case owns one transaction.
- Stop at any checkpoint to validate the corresponding story independently.
