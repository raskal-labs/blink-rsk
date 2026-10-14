# Blink-RSK — Product roadmap

**Updated:** 2026-10-13  
**Status:** Proposed (product direction); individual capabilities have their own statuses below  
**Primary repository:** [raskal-labs/blink-rsk](https://github.com/raskal-labs/blink-rsk)  
**Audience:** Private/personal iOS installation; not currently intended for distribution.

## 1. Direction

Evolve Blink-RSK from a SideStore-compatible Blink Shell build into a **personal, general-use iOS workspace** for computers, files, code, services, projects, and automations.

**Working product name:** RSK.AL (Proposed). PORYGON and P2 remain naming candidates, but may fit the separate agent/orchestration system better. Do not change the application's bundle ID, App Group, keychain identity, extensions, or SideStore registrations merely to rebrand.

**Design intent:** Keep Blink's mature terminal, SSH, Mosh, SFTP/File Provider, sessions, and Blink Code components. Add a thin, discoverable user interface and useful integrations incrementally; run heavier operations on GameCube or the appropriate service. This is *not* a commitment to rewrite Blink or build a replacement operating system.

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

## 2. Baseline reconciliation (as of 2026-10-13)

| Capability / artifact | Status | Evidence / next distinction |
| --- | --- | --- |
| macOS GitHub Actions builds from pinned upstream Blink 18.7.0 | Verified | CI and archived artifacts recorded in [Phase 01](docs/PHASE-01.md) on its working branch; Xcode 26.6 was used. |
| A SideStore-installed Blink-RSK build launches and SSH/SFTP/SCP can work on iPhone | Verified | User observed working connections and transferred `hd-receipts.zip` from a local `iPhone` bookmark to GameCube `/lab`. |
| Local file operations and persistence | In Progress | User reported successful local file operations and a persistence check. Record an exact acceptance receipt identifying the installed IPA/build, location and operations before promoting release status. |
| iOS Files.app remote File Provider | In Progress | Earlier FP Test stayed at Loading; later device work showed GameCube's remote root. Reconcile which installed IPA passed listing, disposable upload/download/rename/delete, refresh and app relaunch. Do not treat “Validate Connection” as proof. |
| 2026-10-12 signing/FP candidate IPA | Verified | Structurally built/archived; *native installation and acceptance for this exact SHA remain Unknown* in [Codex runbook](docs/CODEX-PHASE-01.md). |
| Touch scrolling/selection/keyboard behavior | Blocked | Intermittent freezes, difficult history selection and keyboard focus behavior remain unresolved; [issue #3](https://github.com/raskal-labs/blink-rsk/issues/3). |
| SSH keys and host profiles across GameCube, u64, T480, Oxygen | In Progress | Several connections have been configured; inventory and test each separately. Oxygen's phone-hotspot IP is not stable. |
| Branding, general workspace navigation, service integrations | Proposed | No implementation should be inferred from this roadmap. |
| `blink-rsk-release` as second GitHub repository | Unknown | Local artifact archive on GameCube is documented as `/lab/blink-rsk-release`; the separately named GitHub repository could not be verified through the available GitHub connection. Do not assume it is an accessible canonical source repo. |

**Record reconciliation:** [issue #2](https://github.com/raskal-labs/blink-rsk/issues/2) and the Phase 01 runbook are the authoritative *execution history*, but some device tests happened afterward. Reconcile their status with dated observations rather than rerun the entire signing investigation or prematurely close the issue.

## 3. Milestone roadmap

Milestones are **dependency ordered, not date estimates**. Ship one narrow increment at a time.

### M0 — Close and protect the working foundation
**Status:** In Progress  
**Goal:** A reproducible and restorable build, with a short acceptance record for the installed app.

- Reconcile the actual installed IPA/version/SHA with the latest candidate and archived rollback build.
- Confirm iPhone launch/restart, SSH, Mosh where available, original keys and host profiles, SFTP/SCP, and iOS Files *listing and transfers*; preserve earlier successful test evidence.
- Verify storage persistence, Files provider relaunch/refresh, SideStore refresh/signing, app configuration backup/migration feasibility.
- Audit App Group, keychain group and extension identities *without* altering them unnecessarily; do not expose secrets.
- Record known-good release/tag, source revision, manifest, SHA and tested iOS version.
- Resolve or narrow [issue #2](https://github.com/raskal-labs/blink-rsk/issues/2), and sync its acceptance checklist.

**Exit gate:** One known restorable IPA, explicit test matrix and remaining limitations. Stop on unaccepted data-loss or provisioning risk.

### M1 — Daily terminal usability
**Status:** Proposed; issue #3 is already open  
**Goal:** Remove high-frequency frustrations with minimal terminal regressions.

**Priority A:** Fix touch-scrolling freeze; independent Input versus Select/Scroll interaction; dependable Hide/Show Keyboard; accessible Select All (define scope); reliable selection and copying across scrollback; normal arrow-key option. Test local Blink shell, SSH and Mosh, landscape/portrait, software/hardware keyboard.

**Priority B:** Session overview/switcher and recovery; compact contextual action dock; jump to latest output; history search; clear connection status; clipboard Copy / Copy Raw / Share / Save Output; safer large/sensitive paste handling; quick help for gestures and shortcuts.

**Preferred method:** Start with upstream gesture/keyboard/context-bar behavior. Investigate defects separately from UX preferences; do not rewrite terminal rendering or gesture handling prematurely.

**Exit gate:** Scrolling and input pass real-device regression tests and users can switch, select, copy and resume sessions without surprises.

### M2 — Personal identity and coherent navigation
**Status:** Proposed  
**Goal:** Make this unmistakably the user's own app without destabilizing identities or replacing the terminal.

- Choose final name/icon/wordmark (RSK.AL currently strongest proposal), monochrome/adaptive themes, launch appearance, About, useful app settings.
- Retain existing signing/bundle/App Group identifiers during early rebrand; visible name and icon can change independently.
- Provide a compact **workspace entry point**, not an obligatory heavyweight home screen: Terminal, Files, Projects, Devices, Actions and Tools are candidate destinations.
- Add a command palette / contextual launcher and favorites/recent items, with phone-first ergonomics. Every module should remain optional and terminal access one gesture away.
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
- **Automation:** App Shortcuts/Siri/Shortcuts/share-sheet/Home Screen actions where supported; first expose concrete user workflows rather than invent a universal automation engine.
- **Polaris/Porygon:** the app is a client and invocation surface, not an independent secret-holding agent brain. Respect project ownership and approval queues.

**Exit gate:** Useful cross-system actions with explicit ownership, authentication, error feedback, and no duplicate canonical state.

### M5 — Optional richer environment
**Status:** Proposed / exploratory  
**Goal:** Advance only after real use demonstrates demand.

Candidates: personalized dashboard/widgets, lightweight notes/inbox/capture, search across selected known services, extensible action definitions, terminal-to-structured result views, TUI-like navigation, phone-friendly shortcuts/T9/pointer modes, external-display workflows, remote desktop or richer code views, media previews, and narrowly scoped AI assistance.

**Do not precommit:** local AI runtime/JIT, replacing iOS Files, a custom SSH stack, a general browser/IDE rewrite, permanent autonomous agents, or wholesale modification of iOS restrictions. These are separate research proposals, not required milestones.

## 4. Priority ordering (cross-cutting backlog)

| Tier | First tasks | Why |
| --- | --- | --- |
| **P0 — Protect** | Verify build/data/Files receipts; signing/refresh and backup/restore; preserve known-good rollback | Prevent regression and lost access |
| **P1 — Friction** | Scrolling; input/selection/keyboard; sessions; paste/copy; host connection feedback | High daily impact, bounded changes |
| **P2 — Discoverability** | Branding; contextual dock; palette; favorites; helpful existing features | High value without full rewrite |
| **P3 — Workflows** | Transfers; `code`/code-server; useful shell gaps; iOS Shortcuts | Reduces app switching |
| **P4 — Integration** | Atlas/Polaris, devices, HA, infrastructure, project actions | Benefits from stable navigation/auth |
| **P5 — Experiments** | Rich dashboards, visual controls, AI/native integrations, alternative input | Validate demand before complexity |

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

1. **Reconcile Phase 01 acceptance**, not repeat Phase 01: identify installed IPA; record user-tested success on local files, remote files, SCP and persistence; classify any remaining File Provider or signing unknowns. Update issue #2 and tag only if acceptance is satisfied.
2. **Make issue #3 the next focused UX project:** reproduce the scrolling freeze and compare upstream, then fix/verify scrolling before layering a redesigned action dock or keyboard mode.
3. **Audit already-present features** (gestures/context bar, Snips, Blink Code, File Provider, themes, bookmarks, Shortcuts and commands) and map *exposed/hidden/disabled/unsupported* before any new UX code.
4. **Choose a small branded slice** (display name/icon/About, not bundle identity) and a first command-palette prototype after the stability gates.
5. **Implement the first end-to-end nonterminal workflow**: file transfer or edit-on-GameCube, then assess whether the proposed workspace/navigation architecture is genuinely needed.

## 8. Sources and linked tasks

- [Phase 01 issue #2](https://github.com/raskal-labs/blink-rsk/issues/2)
- [Terminal UX issue #3](https://github.com/raskal-labs/blink-rsk/issues/3)
- [Phase 01 background](https://github.com/raskal-labs/blink-rsk/blob/phase/01-upstream-parity/docs/PHASE-01.md)
- [Phase 01 Codex runbook](https://github.com/raskal-labs/blink-rsk/blob/phase/01-upstream-parity/docs/CODEX-PHASE-01.md)
- [Blink upstream repository](https://github.com/blinksh/blink) and [documentation](https://docs.blink.sh/)
- [Blink Files.app integration](https://github.com/blinksh/docs/blob/master/src/pages/advanced/files-app.md)
- [Blink Code documentation](https://docs.blink.sh/advanced/code)

*Roadmap decisions and statuses should change as real device evidence and user priorities change; the product direction is intentional, but the unbuilt modules are not commitments.*
