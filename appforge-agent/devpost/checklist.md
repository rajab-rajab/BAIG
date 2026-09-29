---
doc: checklist
status: approved
---

# Build Checklist

Build mode: fast

## Slices

- [x] **1. BuildTrace can generate, inspect, and initialize the local demo project offline**
  Becomes usable: A runnable BuildTrace desktop window where the user can select **Use Offline Template**, watch the three-file build sequence complete, inspect the written files, and see `main.py init` run in the embedded terminal.
  Why now: This delivers the unique kernel—transparent, real local generation and verification—without depending on credentials or network access. It also proves the CustomTkinter layout, payload validation, safe writes, and subprocess streaming as one usable flow.
  PRD ref: `prd.md > The Core Journey` (steps 1–5), `Features and Behavior > Transparent project generation`, `Features and Behavior > Local execution and proof`
  Spec ref: `spec.md > AppShell`, `BuildInputPanel`, `BuildController`, `FallbackProvider`, `PayloadValidator and ProjectWriter`, `FileInspector`, `TerminalRunner`, `Generated Task Manager`, `File Structure`
  Build: Scaffold the CustomTkinter host and dark three-panel layout; add the checked-in fallback payload and generated task-manager contract; validate and write the three files to `output/buildtrace_app/`; show ordered progress and inspector tabs; stream the initialization subprocess into the terminal.
  Verify (mechanical): Run the generated task-manager tests, launch the host app in offline mode, confirm the three expected files exist under `output/buildtrace_app/`, and verify `python main.py init` exits successfully from that directory.
  Learner check: Launch BuildTrace, choose **Use Offline Template**, then confirm the visible progress turns green, each file appears in a tab, and the terminal reports successful initialization.
  Commit: `Build offline project generation flow`

- [ ] **2. The embedded terminal proves the generated task manager persists work**
  Becomes usable: After an offline build, the user can enter the specified add and list commands in BuildTrace and visibly see a stored SQLite task in the terminal.
  Why now: The first slice proves file creation; this slice closes the demo's proof loop by showing that the generated code actually accepts commands and retains task data.
  PRD ref: `prd.md > The Core Journey` (steps 6–7), `Features and Behavior > Local execution and proof`
  Spec ref: `spec.md > TerminalRunner`, `Generated Task Manager`, `Data Model > Generated task data`, `Important Failure Modes`
  Build: Add the controlled terminal command field, command parsing/allowlist, line-by-line process output, and generated CLI behavior for `init`, `add`, `list`, and `complete`; surface execution errors in red without blocking the UI.
  Verify (mechanical): In the generated output directory, run init, add `Submit Devpost Video`, and list; assert that task ID 1 and its title appear, and run automated tests for generated SQLite persistence and rejected terminal commands.
  Learner check: In the terminal panel, enter `python main.py add "Submit Devpost Video"` and `python main.py list`; confirm the created ID and formatted task row appear.
  Commit: `Add embedded task manager verification`

- [ ] **3. BuildTrace uses live OpenAI generation when available and handles failures clearly**
  Becomes usable: With a configured key, the app can request the three-file payload from OpenAI; without a key, it clearly offers offline generation; failed live requests fall back without losing the demo flow.
  Why now: The reliable offline core already works, so the external-service risk is isolated and easy to diagnose without jeopardizing the proof.
  PRD ref: `prd.md > Features and Behavior > Build request and readiness`, `States and Boundaries`
  Spec ref: `spec.md > HeaderStatus`, `GenerationService`, `External Services and Dependencies > OpenAI Chat Completions API`, `Important Failure Modes`, `Decisions and Open Issues`
  Build: Add safe environment and `.env` key detection, readiness/error messaging, the OpenAI Chat Completions request with JSON-mode parsing, the ten-second timeout, and fallback routing for API failures; keep secrets out of logs and tracked files.
  Verify (mechanical): Run unit tests for no-key/offline state, malformed payload rejection, and simulated timeout/auth/quota fallback. If the learner authorizes reuse or creation of an API key, run one live request and validate its response before writing files; otherwise verify the offline route only.
  Learner check: Start the app with no key and confirm **Fix Settings to Build** plus **Use Offline Template** appear; if using a key, run a live build and say whether the readiness and progress feedback make sense.
  Commit: `Add resilient OpenAI generation`

- [ ] **4. The finished dashboard is polished and ready for the one-minute demo**
  Becomes usable: The full core journey has the approved dark developer-console visual hierarchy, clear active/verified/failed states, and concise setup instructions so it can be recorded reliably.
  Why now: Visual polish lands after the interaction is real, so it refines proven behavior rather than decorating unverified scaffolding.
  PRD ref: `prd.md > Look and Feel`, `What We're Building`, `States and Boundaries`
  Spec ref: `spec.md > Look and Feel`, `Components > ProgressTracker`, `Important Failure Modes`, `Where It Runs and How Someone Tries It`
  Build: Apply the exact palette, typography fallbacks, crisp panel borders, status treatments, and active-step pulse; complete README setup/demo instructions; add regression tests and a final offline end-to-end verification command.
  Verify (mechanical): Run the full automated test suite and the offline end-to-end flow; inspect that the app starts, writes only inside `output/buildtrace_app/`, initializes the generated app, and displays add/list results without exceptions.
  Learner check: Run the whole one-minute flow from launch through add/list, then report anything confusing, visually weak, or unreliable before the final review.
  Commit: `Polish BuildTrace demo experience`

## Hands-on Checkpoints

- [ ] Early usable behavior explored — after slice 2, when the offline build and task-persistence proof can shape the remaining live-generation and polish work
- [ ] Final kick-the-tires exploration and feedback completed

## Final Review

- [ ] Final review complete — feedback resolved and learner confirms ready to ship

## Code Tour and App Map

- [ ] Learning activity complete — guided route, focused alternative, prior practice connected, or brief recap
- [ ] Optional edit and transfer reflection addressed — offered/declined/already covered/not applicable as appropriate
- [ ] `devpost/app-map.html` generated from finished code, checked, and shown, including a project-grounded practice to reuse

Activity and evidence: [what actually happened; real document/test/code references; unfinished work if interrupted]
Route and stops: [actual paths and symbols; guided stops completed, or reference-only route]
Edit outcome: [tried/kept/reverted/declined/not applicable; verification if changed]
Reflection: [offered/answered/declined/already covered — personal answer belongs only in the ignored profile]
Activity mode: [live app and editor, explicit static fallback, focused alternative, prior practice, or recap]

## Revisions
