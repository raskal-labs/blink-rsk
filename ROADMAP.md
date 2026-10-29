# Blink-RSK — Product roadmap

**Updated:** 2026-10-28 (customization candidate compiled, signed, packaged and archived; device results pending)
**Status:** Proposed (product direction); individual capabilities have their own statuses below  
**Primary repository:** [raskal-labs/blink-rsk](https://github.com/raskal-labs/blink-rsk)  
**Audience:** Private/personal iOS installation; not currently intended for distribution.

## 1. Direction

Evolve Blink-RSK from a SideStore-compatible Blink Shell build into a **personal, general-use iOS workspace** for computers, files, code, services, projects, and automations.

**Working product name:** RSK.AL (Proposed). PORYGON and P2 remain naming candidates, but may fit the separate agent/orchestration system better. Do not change the application's bundle ID, App Group, keychain identity, extensions, or SideStore registrations merely to rebrand.

**Design intent:** Keep Blink's mature terminal, SSH, Mosh, SFTP/File Provider, sessions, and Blink Code components. Add a thin, discoverable user interface and useful integrations incrementally; run heavier operations on GameCube or the appropriate service. This is *not* a commitment to rewrite Blink or build a replacement operating system.

**Document ownership:** [Product direction](docs/PRODUCT-DIRECTION.md) records boundaries and decisions; [iOS integrations](docs/IOS-INTEGRATIONS.md) and [UX research](docs/UX-RESEARCH.md) record evidence and open investigations; [AGENTS.md](AGENTS.md) defines agent safeguards. [docs/ROADMAP.md](docs/ROADMAP.md) is historical, not a second active plan. Confirmed implementation details belong in GitHub issues.

### Principles and constraints

1. **Preserve the working app.** Every development milestone starts from a tagged, reproducible, installed baseline with a rollback artifact. Never equate CI success with iPhone success.
2. **Local-first, interoperable and replaceable.** Prefer SSH, Mosh, SFTP, Git, HTTPS APIs, iOS Shortcuts and existing services; no unnecessary proprietary backend or duplicated state. GameCube/Atlas remain authorities for their data.
3. **Useful immediately.** Prioritize recurring friction (scrolling, keyboard, selection, sessions, transfers) over aesthetic or architectural changes.
4. **Inspect before implementing.** Blink already contains features that may be hidden, undocumented, disabled, or awkward to reach. Expose or configure first; patch only when evidence justifies it.
5. **Least privilege and safe control.** No sharing private keys or secrets in Git/artifacts; verify SSH host identity; confirm before destructive commands; give remote actions explicit target and scope.
6. **Low build/test cost.** Reuse existing evidence and artifacts, search other people's resolved cases before bespoke diagnostics, batch tests and questions, and limit speculative CI builds.
7. **SideStore is a real constraint.** Active application slots, registered App IDs (including extensions), provisioning/entitlements, and refresh lifetime are separate concerns. Avoid new IDs or parallel installs by default.
8. **One coherent experience, not one giant implementation.** Lightweight native entry points can lead to Blink-native features, remote web views, Shortcuts, or existing iOS apps.
9. **Keep status honest.** Only use: Mentioned, Proposed, In Progress, Verified, Blocked, Unknown.

## 2. Baseline reconciliation (2026-10-13 evidence; 2026-10-23 clarification)

**New SideStore screenshot (2026-10-13 ~20:49 PDT):** Blink and LiveContainer are the two apps *listed* as Active, **5 App IDs remaining** (previous snapshot: 4), both showing **7 DAYS** to expiry; SideStore **0.7.0-20260918.492+12a496ca** and LiveContainer **3.8.10-Release** on iOS 27.0. SideStore itself is not listed, so do **not** infer a free third app slot. App IDs remaining are not a breakdown of extension IDs; seven days displayed are not proof refresh will succeed. For details and signing constraints see [iOS integration evidence](docs/IOS-INTEGRATIONS.md).


| Capability / artifact | Status | Evidence / next distinction |
| --- | --- | --- |
| macOS GitHub Actions builds from pinned upstream Blink 18.7.0 | Verified | CI and archived artifacts recorded in [Phase 01](docs/phase-01/PHASE-01.md) on its working branch; Xcode 26.6 was used. |
| A SideStore-installed Blink-RSK build launches and SSH/SFTP/SCP can work on iPhone | Verified | User observed working connections and transferred `hd-receipts.zip` from a local `iPhone` bookmark to GameCube `/lab`. |
| Local file operations and bookmark persistence | Verified | Positive persistence feedback followed by user-reported functional acceptance of the combined candidate. This is not an independent installed-checksum, exhaustive recovery or SideStore-refresh measurement. [Acceptance record](docs/phase-01/SHORTCUTS-EXPANSION-CANDIDATE.md#device-acceptance--2026-10-27). |
| Host/session links and three foreground Shortcuts actions | Verified | October 26 user confirms links work and explicitly confirms all three actions appear and run. Basic user-reported functionality only; exact installed IPA SHA, cancellation/negative-input/host-key checks and refresh remain unestablished. Earlier link/discovery blocker is superseded; no additional source fix/build was performed. [Acceptance evidence](docs/phase-01/SESSION-ACTIONS-CANDIDATE.md#october-26-links-and-shortcuts-success). |
| iOS Files.app remote File Provider | Verified | Combined candidate accepted by user report; owner closed issue #2. The withdrawn October 26 sync report remains superseded. No fabricated per-transfer result or causal claim for startup cleanup; detailed per-case evidence remains separate. |
| 2026-10-12 signing/FP candidate IPA | Verified | Structurally built/archived; *native installation and acceptance for this exact SHA remain Unknown* in [Codex runbook](docs/phase-01/CODEX-PHASE-01.md). |
| Touch scrolling/selection/keyboard behavior | Proposed | Investigate reported scrolling behavior across local shell, SSH and Mosh, first outside Zellij/tmux. Whether Blink, Mosh or the remote application causes it remains Unknown; no scrolling code fix is assumed. Selection and keyboard improvements remain Proposed in [issue #3](https://github.com/raskal-labs/blink-rsk/issues/3). |
| SSH keys and host profiles across GameCube, u64, T480, Oxygen | In Progress | Several connections have been configured; inventory and test each separately. Oxygen's phone-hotspot IP is not stable. |
| Branding, general workspace navigation, service integrations | Proposed | No implementation should be inferred from this roadmap. |
| `blink-rsk-release` as second GitHub repository | Unknown | Local artifact archive on GameCube is documented as `/lab/blink-rsk-release`; the separately named GitHub repository could not be verified through the available GitHub connection. Do not assume it is an accessible canonical source repo. |

**Record reconciliation:** [issue #2](https://github.com/raskal-labs/blink-rsk/issues/2) and the Phase 01 runbook are the authoritative *execution history*, but some device tests happened afterward. Reconcile their status with dated observations rather than rerun the entire signing investigation or prematurely close the issue.

## 3. Milestone roadmap

Milestones are **dependency ordered, not date estimates**. Ship one narrow increment at a time.

### M0 — Accepted working foundation and ongoing safeguards
**Status:** Verified for user-reported functional acceptance; unmeasured lifecycle evidence remains separate
**Goal:** A reproducible and restorable build, with a short acceptance record for the installed app.

- Reconcile the actual installed IPA/version/SHA with the latest candidate and archived rollback build.
- Confirm iPhone launch/restart, SSH, Mosh where available, original keys and host profiles, SFTP/SCP, and iOS Files *listing and transfers*; preserve earlier successful test evidence.
- Ensure saved folder bookmarks survive temporary access failures and can recover (**In Progress**; issue #2); verify across relaunch and refresh. Preserve earlier successful file-operation evidence and check current Files provider browse/transfer/reopen separately.
- Verify other storage persistence, SideStore refresh/signing, app configuration backup/migration feasibility.
- Audit App Group, keychain group and extension identities *without* altering them unnecessarily; do not expose secrets.
- Record known-good release/tag, source revision, manifest, SHA and tested iOS version.
- Resolve or narrow [issue #2](https://github.com/raskal-labs/blink-rsk/issues/2), and sync its acceptance checklist.

**Exit gate:** One known restorable IPA, explicit test matrix and remaining limitations. Stop on unaccepted data-loss or provisioning risk.

### M1 + M2 — Combined customization
**Status:** In Progress (seven-workstream native candidate available; device validation pending)

**Accepted direction:** touch controls, terminal usability, workspace UI and appearance in one coherent milestone, preserving the terminal-first experience and current app/provider identities. The user accepted the previous batch and asked to move forward. Existing M1/M2 detail below remains the research backlog; it is not blanket authorization to import all experiments.

**Scope correction:** the user rejected the small controls/launcher batch as too small and asked to “go big” for the next build. Supersede that first-batch proposal with a substantial combined customization release. The target below is one coherent candidate across all seven workstreams, developed in separately reviewable commits. These are implementation targets, not claims that the features already exist or passed device checks.

| Workstream | Next-build target | Source basis and required boundary |
| --- | --- | --- |
| Customizable touch controls | Collapsible action dock with editable order/visibility, saved profiles, size/placement preferences, common modifiers/navigation keys and optional separate D-pad with repeat. | Extend the existing action/key encoding; selectively adapt the reviewed D-pad, not its entire fork. Repeat must stop on release, view dismissal, app backgrounding and session switch. Keep VoiceOver and portrait/landscape use practical. |
| Input and keyboard control | Explicit Input versus Select/Scroll interaction, dependable keyboard hide/show, optional keyboard lock with an obvious unlock control, discoverable gesture/key bindings. | Compose with existing Snips/overlay focus capabilities; do not treat layout lock as keyboard lock or blindly block every first responder. Preserve external-keyboard use and restore the intended mode after sheets, foregrounding and session changes. |
| Selection, copying and output | Explicit Select All, Copy All retained text and Copy Screen; local jump-to-bottom; adjustable selection plus Copy/Copy Raw/Share/Save output with a preview for large retained exports and visible limits. | Read retained rows rather than use DOM selection for every export. Correct and test the reproduced Select All branch bug. Wrapped lines, Unicode, alternate screen and history limits need distinct fixtures. This does not promise repaired arbitrary drag-selection truncation or remote history recovery. |
| Paste reliability | Optional preview for multiline/escape-containing pastes and a bounded, ordered, cancellable delivery path for large input, with progress/error feedback. | Adapt the reviewed partial-write lead, not its unbounded retry/sleep loop. Fault-inject partial writes, EINTR/EAGAIN and closed pipes. Preserve exact bytes, bracketed-paste semantics and interactive-app behavior; never run a preview automatically. |
| Session management | Visible session overview with titles/user labels, switch/rename/reorder/new/close actions, honest local/SSH/Mosh context and clear close-versus-disconnect semantics. | Reuse SessionRegistry/TermController and per-window identity. Keep user labels distinct from OSC titles and Shortcuts link IDs. Serialize rapid create/switch/close transitions without adopting fork behaviors that erase sessions on upgrade or kill temporarily disconnected Mosh sessions. |
| Workspace and action navigation | A coherent optional workspace surface for sessions, saved hosts/favorites/recents, bookmarked folders, Snips and existing actions; searchable action palette and consistent return-to-terminal controls. | Use existing host/bookmark/navigation/typed-action machinery, not a second credential/file-sync store. A saved host is not proof of a live connection. Keep command insertion/execution explicit and external links navigation-only. Preserve unavailable bookmarks. |
| Appearance and customization | A coordinated workspace/dock/settings visual treatment with light/dark choices, accents and density; named terminal/control presets; theme/font/cursor/bold preview and explicit per-session versus future-session apply behavior. | Extend TerminalStyle/TerminalStyleStore and existing theme/font management. Preserve current custom settings and make resets explicit. App-wide visuals should change meaningfully; merely linking to the existing Style screen is insufficient. Final public name/icon is a separate choice; internal bundle/App Group/keychain identities stay fixed. |

**October 28 source checkpoint:** the user chose the roadmap batch. Three separately guarded customization patches now implement the seven workstreams above, composed with the six accepted foundation patches. Local model/JavaScript/real-pipe regressions and all existing combined preflight checks pass on exactly 31 source paths. Native Apple UI/queue validation, iOS compilation, metadata/packaging and device behavior remain Unknown; no new CI dispatch or device operation occurred. [Concrete behavior, constraints, exact local receipts and combined device checklist](docs/customization/CUSTOMIZATION-CANDIDATE.md). Session context is command state plus labeled launch targets, not invented live transport state; close uses existing terminal lifecycle, with remote detach left to the remote application. Retained export is bounded local text. Dock/D-pad respect viewport and explicit layout-lock limits.

**October 28 native checkpoint:** the user explicitly authorized one candidate CI build from `71c12fb`. [Run 40798686069](https://github.com/raskal-labs/blink-rsk/actions/runs/40798686069) passed all native preflight, iOS compilation, signature/identity checks, eight-action App Intents metadata and packaging. [Candidate](https://github.com/raskal-labs/blink-rsk/actions/runs/40798686069/artifacts/12865551302), IPA SHA `b06e36bc4a0b6c11fce8fa94dfc04a665dafab221497611992fbb0ed2d4398b2`. Independent downloaded-package and exact native receipt checks pass; [archive, provenance and combined device checklist](docs/customization/CUSTOMIZATION-CANDIDATE.md#native-candidate--2026-10-28). This supersedes the source checkpoint's pending native gates; device behavior remains Unknown. One dispatch used, no retry/install/reset/identity change/merge; draft PR #8 remains unmerged.

**Build-size rule:** do not produce an interim candidate after only hide/show, a jump button and links to Settings. Assemble the compatible targets above, exercise their interactions, then prepare one combined candidate handoff. Split/defer a target only for a documented source/platform/correctness constraint and finish the remaining substantial scope; do not silently reduce the milestone to the earlier tiny batch.

**Focused validation:** profile/preferences round trips and defaults; D-pad repeat cancellation; keyboard/input/selection state with Snips and external keyboard; retained-text and Select All fixtures; fault-injected ordered paste; session lifecycle and existing cold/warm App Intents; workspace navigation and bookmark preservation; style apply scope/preview. Run all existing patch/Shortcuts/provider checks, native compilation, App Intents metadata, identity/extension checks and packaging before device acceptance. Source, native and device results remain separate. Keep the accepted IPA/rollback archive intact.

**Research boundaries:** renderer/backpressure replacements and claims to repair scrolling freezes, complete native Mosh scrollback/mouse experiments, remote multiplexer-history retrieval, new cloud integrations, new extensions and identity/migration changes are not automatically imported by “go big.” Retain their research. Local retained-buffer copying and explicitly targeted remote tmux/Zellij history are different workflows. No CI dispatch, installation, reset or merge occurs in this scope revision.

#### M1 — Daily terminal usability
**Status:** Proposed; former issue #3 returns HTTP 410 (deleted), observed October 26

**Goal:** Remove high-frequency frustrations with minimal terminal regressions.

**October 27 scope:** the combined Shortcuts batch includes only the two reviewed Snips resign lines and gesture-detachment correction, with separate guards/provenance. They establish no scrolling-freeze fix. The provider backport joins the same single authorized candidate build; October 26 deferral is superseded. The next agreed milestone combines touch controls, terminal usability, workspace UI and appearance; the M1/M2 research below feeds that milestone and adds nothing speculative to this build.

**Priority A:** Investigate scrolling behavior across local Blink shell, SSH and Mosh, first outside Zellij/tmux; distinguish client defects from transport/application behavior before proposing a code fix. Other proposed improvements: independent Input versus Select/Scroll interaction; dependable Hide/Show Keyboard; accessible Select All (define scope); reliable selection and copying across scrollback; normal arrow-key option. Test landscape/portrait and software/hardware keyboard.

**Priority B:** Session overview/switcher and recovery; compact contextual action dock; jump to latest output; history search; clear connection status; clipboard Copy / Copy Raw / Share / Save Output; safer large/sensitive paste handling; quick help for gestures and shortcuts.

**October 27 clarification:** include an explicit Select All/Copy All control in the proposed clipboard scope. Local retained-buffer export and remote tmux/Zellij history over Mosh are different operations; neither may promise to recover output the client never received. [Source review and scope](docs/TERMINAL-UX-UPSTREAM-REVIEW.md#october-27-follow-up-other-complaints-copy-all-and-mosh-history).

**Preferred method:** Start with upstream gesture/keyboard/context-bar behavior. Investigate defects separately from UX preferences; do not rewrite terminal rendering or gesture handling prematurely.

**Exit gate:** Scrolling and input pass real-device regression tests and users can switch, select, copy and resume sessions without surprises.

#### M2 — Personal identity and coherent navigation
**Status:** Proposed  
**Goal:** Make this unmistakably the user's own app without destabilizing identities or replacing the terminal.

- Choose final name/icon/wordmark (RSK.AL currently strongest proposal), monochrome/adaptive themes, launch appearance, About, useful app settings.
- Retain existing signing/bundle/App Group identifiers during early rebrand; visible name and icon can change independently.
- Provide a compact **workspace entry point**, not an obligatory heavyweight home screen: Terminal, Files, Projects, Devices, Actions and Tools are candidate destinations.
- Add a command palette / contextual launcher and favorites/recent items, with phone-first ergonomics. Every module should remain optional and terminal access one gesture away.
- **Proposed, not yet an engine:** evaluate a small typed action catalogue for native host/session navigation and a few scoped actions. Reuse the same action definition through an in-app palette, App Intents/Shortcuts and eventually other approved iOS surfaces. Distinguish navigation, read-only queries and privileged execution.
- Preserve upstream fonts, themes, split views, Snips, keyboard shortcuts and external-display support when available.

**Exit gate:** Consistent appearance and navigation, with no regression to core sessions or Files.

### M3 — Files, development and useful built-in tools
**Status:** Proposed  
**Goal:** Make common iPhone-to-server tasks easy without a computer.

- Files: choose source/destination, recent paths/bookmarks, transfers with feedback, preview/share, rename/move/delete with confirmations, retry/error feedback, and distinction between local iPhone storage and remote hosts.
- Explore thin file views over existing Blink SFTP/File Provider rather than a second independent synchronization system.
- Developer workflow: expose existing `code` and `blink-fs`; test GameCube-hosted code-server via secure access; Git/status/diff/commit links; open the current Atlas/RSK/Scout project path.
- Local command gap audit: first `find`, `sort`, `uniq`, `head`, `tail`, `cut`, `tr`, `tee`, SHA-256; only then evaluate `jq`, `sqlite3`, `file`, BLAKE3. Confirm what is already in the pinned `ios_system` build and prefer running heavy utilities remotely.
- Reuse Snips, `fcp`, `browse`, bookmarks and native iOS share/Shortcuts surfaces where already supported.

**Exit gate:** At least three complete real workflows: move a file from iPhone to GameCube; inspect/edit/commit a remote file; capture/share a command result.

### M4 — Connected personal infrastructure
**Status:** Proposed  
**Goal:** A small useful control and observation layer over existing services, not a competing control plane.

- **Devices:** GameCube, u64, T480 and Oxygen host profiles, reachable state, SSH/Mosh launch, known network identity, VPN/hotspot handling and diagnostics. Prefer existing SSH config, DNS, WireGuard and service discovery.
- **Projects:** read-only Atlas project overview, current task/roadmap, useful deep links to canonical documents, GitHub issues and local working directories. Add carefully scoped edit/approve actions only through the canonical Atlas workflow.
- **Operations:** selected Home Assistant, infrastructure health, safe service actions and log views via authenticated existing APIs/SSH. Confirm target/scope; privileged or destructive actions require approval.
- **Automation:** App Shortcuts/Siri/Shortcuts/share-sheet/Home Screen actions where supported; first expose concrete user workflows rather than invent a universal automation engine. **Integrate first:** reuse official Home Assistant widgets, actionable notifications and automations before building our own widget or Pushcut substitute. A first read-only source audit should assess upstream Blink's 2026-10-12 [session-link/App Intents commit](https://github.com/blinksh/blink/commit/7a427f3db37ec25869b24226905d89103a8ad99d) and the restored 18.7.1 callback scheme. Host-key trust and URI-triggered command execution require security review before porting; source existence is not device acceptance.
- **Cross-app pilot:** using existing software and *no new IPA*, verify one safe Home Assistant widget/action → GameCube result → actionable notification. If deep links later prove safe, connect **View Logs** to a named Blink session. Keep the Godot apartment digital twin as its own HA client, not an engine embedded into Blink-RSK. Full integration research and experimental gates: [IOS-INTEGRATIONS.md](docs/IOS-INTEGRATIONS.md).
- **Events and context (research):** evaluate a read-only, source-linked activity view after the notification pilot; retain source-side event history. Investigate existing HA context, network/Focus state, and optional beacon-based suggestions, not implicit permission to execute.
- **Polaris/Porygon:** the app is a client and invocation surface, not an independent secret-holding agent brain. Respect project ownership and approval queues.

**Exit gate:** Useful cross-system actions with explicit ownership, authentication, error feedback, and no duplicate canonical state.

### M5 — Optional richer environment
**Status:** Proposed / exploratory  
**Goal:** Advance only after real use demonstrates demand.

Candidates: personalized dashboard/widgets and Control Centre extensions, lightweight notes/inbox/capture, search across selected known services, terminal-to-structured result views, an event inbox, optional iBeacon proximity and contextual suggestions, TUI-like navigation, phone-friendly shortcuts/T9/pointer modes, external-display workflows, remote desktop or richer code views, media previews, and narrowly scoped AI assistance. Evaluate the surrounding iOS interface and third-party apps before adding native extensions. **Native WidgetKit is a conditional spike, not a commitment:** first establish a use case official HA widgets cannot meet, then check SideStore ID budget, widget registration, App Group entitlement sharing, refresh and an entire reprovisioning cycle. Stop if the free-signing path is unreliable. See [iOS integration research](docs/IOS-INTEGRATIONS.md).

**Do not precommit:** local AI runtime/JIT, replacing iOS Files, a custom SSH stack, a general browser/IDE rewrite, permanent autonomous agents, or wholesale modification of iOS restrictions. These are separate research proposals, not required milestones.

## 4. Priority ordering (cross-cutting backlog)

| Tier | First tasks | Why |
| --- | --- | --- |
| **P0 — Protect** | Verify build/data/Files receipts; signing/refresh and backup/restore; preserve known-good rollback | Prevent regression and lost access |
| **P1 — Friction** | Investigate scrolling behavior; input/selection/keyboard; sessions; paste/copy; host connection feedback | High daily impact, bounded changes |
| **P2 — Discoverability** | Branding; contextual dock; palette; favorites; helpful existing features | High value without full rewrite |
| **P3 — Workflows** | Transfers; `code`/code-server; useful shell gaps; iOS Shortcuts | Reduces app switching |
| **P4 — Integration** | Safe upstream session-link/Shortcuts audit; official HA widget/action/notification pilot; Atlas/Polaris and device actions | Reuse mature capabilities without sacrificing stability |
| **P5 — Experiments** | Rich dashboards, visual controls, AI/native integrations, alternative input | Validate demand before complexity |

**Current device feedback (October 27):** the user reports the combined candidate passing and is ready to move forward; record functional acceptance. Keep earlier explicit link/three-action and bookmark-persistence feedback. Exact installed checksum, refresh and individually unreported negative/recovery outcomes remain follow-up evidence; do not infer per-test results from a general pass. Files sync failure remains withdrawn/superseded, and the withdrawal itself proves no transfer.

**Accepted batch:** user reports the combined candidate passing and is ready to move forward. PR #7 was already merged by the owner at `38cbdb2`; issue #2 is closed. Preserve native build/package evidence and the archived IPA/rollback references; installed SHA and unmeasured refresh/per-case results remain distinct. [Acceptance and scope limits](docs/phase-01/SHORTCUTS-EXPANSION-CANDIDATE.md#device-acceptance--2026-10-27). The next active milestone combines touch controls, terminal usability, workspace UI and appearance.

**Earlier source preflight:** Review the 18.7.1 callback restoration separately from the October 12 session-link/Shortcuts changes. Before implementing bookmark recovery, check existing work and source availability: public `raw` still points to April 14 pin `a90b4423`; October 12 commit `7a427f3` is retrievable by SHA but contains the identical bookmark manager. An exact shipping 18.7.1 source ref and the later documented bookmark fix remain unestablished. Prefer a compatible upstream repair if found; otherwise make the focused patch without automatically changing the baseline. Preservation will not recover already-erased bookmark data; folder reselection may be necessary. This is context and bounded preflight, not a new parity milestone. See issue #2 and [iOS integration research](docs/IOS-INTEGRATIONS.md).

## 5. Product architecture boundaries

- **On iPhone:** native interaction, secure local configuration, terminal renderer, SSH/Mosh, File Provider, Shortcuts entry points, lightweight previews/caches.
- **On GameCube/other hosts:** development/build workflows, indexing, analytics, heavy processing, code-server, project canonical data, durable automation.
- **Atlas:** project documents/tasks/approvals and their canonical state; the app displays and interacts with it.
- **Polaris:** institutional records/registries, evidence and stable source-of-truth services; do not replicate internally.
- **Porygon:** replaceable assistant/agent capability, invoked selectively and subject to authority limits.
- **Home Assistant/u64/Oxygen:** retain ownership of their respective device and infrastructure functions.

Use narrowly scoped adapters to existing commands/APIs. Avoid designing a general plugin runtime until two or more real modules require the same extension boundary. Plan for the limitations of iOS background execution, sandboxing and SideStore entitlements.

## 6. Build, release and task workflow

- `blink-rsk` is the verified source/planning repository. `main` is integration; `phase/01-upstream-parity` remains its execution branch until its closeout decision. The existing archive/baseline branches are historical references, not extra product lines.
- Treat `/lab/blink-rsk-release/` on GameCube as the documented local artifact archive until the status of any separate GitHub `blink-rsk-release` repository is confirmed.
- This roadmap tracks **why and in what order**. GitHub issues track actionable tasks; do not duplicate issue #2's entire diagnostic checklist or issue #3's entire UX criteria here.
- Implement one small vertical slice per PR and test through the existing SideStore app identity wherever safe. Record exact installed build and on-device result before merging/tagging a functional change.
- If blocked, search resolved upstream/SideStore/iOS reports first, then perform the smallest discriminating test; limit repeated builds. Keep raw logs, secrets and private host material off public GitHub.
- Do not make a risky signing, bundle identity, migration, installed-app replacement, or data-deletion decision without user approval.
- Each milestone produces a short human-readable release note and machine-friendly manifest with status, changes, tests, limitations, and next action; compatible with eventual Atlas/Polaris ingestion.

## 7. Immediate next sequence

1. **Accepted foundation:** record the user-reported pass, owner merge/issue closure and archived candidate reference. Carry installed-checksum, refresh and unmeasured per-case checks as follow-up evidence; do not reopen the withdrawn sync blocker or repeat the accepted batch.
2. **Large combined customization milestone (In Progress: native candidate available; device pending):** device-check the seven-workstream target above as one substantial next-build batch: configurable dock/D-pad, input modes/keyboard lock, selection/copy/export, safe large paste, session manager, workspace/palette and meaningful appearance customization. The user rejected the tiny first batch. Keep the accepted app intact and preserve source/native/device evidence; the subsequent single authorized run passed and is archived; no phone operation occurred.
3. **Independent read-only research:** inventory existing Blink/iOS actions, test one official HA → approved GameCube action → actionable notification workflow without a new IPA, and review the upstream session-link/App Intents source for security and compatibility. Capture evidence in [iOS integrations](docs/IOS-INTEGRATIONS.md) and [UX research](docs/UX-RESEARCH.md); no build or new app identity is authorized.

## 8. Sources and linked tasks

- [Phase 01 issue #2](https://github.com/raskal-labs/blink-rsk/issues/2)
- [Terminal UX issue #3](https://github.com/raskal-labs/blink-rsk/issues/3)
- [iOS Home Assistant, Shortcuts, deep-link and WidgetKit research](docs/IOS-INTEGRATIONS.md)
- [Phase 01 background](docs/phase-01/PHASE-01.md)
- [Phase 01 Codex runbook](docs/phase-01/CODEX-PHASE-01.md)
- [Blink upstream repository](https://github.com/blinksh/blink) and [documentation](https://docs.blink.sh/)
- [Blink Files.app integration](https://github.com/blinksh/docs/blob/master/src/pages/advanced/files-app.md)
- [Blink Code documentation](https://docs.blink.sh/advanced/code)

*Roadmap decisions and statuses should change as real device evidence and user priorities change; the product direction is intentional, but the unbuilt modules are not commitments.*
