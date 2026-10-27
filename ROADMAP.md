# Blink-RSK — Product roadmap

**Updated:** 2026-10-26 (upstream provider cleanup backport prepared; Files sync still Blocked)
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
| Local file operations and bookmark persistence | In Progress | Earlier local operations and an initial persistence check succeeded. Later reports show inaccessible folder links and an empty Bookmarks list. Bookmark preservation/reselection is implemented in the unmerged October 24 candidate with 24 local manager regressions; Xcode 26.6 native tests and full iOS build passed in [run 40128366917](https://github.com/raskal-labs/blink-rsk/actions/runs/40128366917); October 25 user feedback reports bookmarks persisting well; full failure/recovery and refresh acceptance remain In Progress, and exact installed IPA identity remains Unknown. Details belong in issue #2. |
| Host/session links and three foreground Shortcuts actions | Verified | October 26 user confirms links work and explicitly confirms all three actions appear and run. Basic user-reported functionality only; exact installed IPA SHA, cancellation/negative-input/host-key checks and refresh remain unestablished. Earlier link/discovery blocker is superseded; no additional source fix/build was performed. [Acceptance evidence](docs/phase-01/SESSION-ACTIONS-CANDIDATE.md#october-26-links-and-shortcuts-success). |
| iOS Files.app remote File Provider | Blocked | October 26 screenshot shows a 28-item listing and “Syncing 1 item to Blink”; user reports no initiated transfer and confirms the item remains persistently stuck. The queued operation and cause are Unknown. Listing visibility is evidence, but fresh child enumeration, read/write completion and reopening remain unverified. Upstream `7e28d172` startup-cleanup disable is now backported in draft PR #7 with local parity/guard/syntax checks; it is absent from the October 24 IPA, and a new Apple build and device recovery remain unverified. [Implementation and acceptance gates](docs/phase-01/FILES-PROVIDER-UPSTREAM-RESEARCH.md#october-26-implementation-follow-up); [device evidence](docs/phase-01/SESSION-ACTIONS-CANDIDATE.md#october-26-persistent-files-sync-stall). |
| 2026-10-12 signing/FP candidate IPA | Verified | Structurally built/archived; *native installation and acceptance for this exact SHA remain Unknown* in [Codex runbook](docs/phase-01/CODEX-PHASE-01.md). |
| Touch scrolling/selection/keyboard behavior | Proposed | Investigate reported scrolling behavior across local shell, SSH and Mosh, first outside Zellij/tmux. Whether Blink, Mosh or the remote application causes it remains Unknown; no scrolling code fix is assumed. Selection and keyboard improvements remain Proposed in [issue #3](https://github.com/raskal-labs/blink-rsk/issues/3). |
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
- Ensure saved folder bookmarks survive temporary access failures and can recover (**In Progress**; issue #2); verify across relaunch and refresh. Preserve earlier successful file-operation evidence and check current Files provider browse/transfer/reopen separately.
- Verify other storage persistence, SideStore refresh/signing, app configuration backup/migration feasibility.
- Audit App Group, keychain group and extension identities *without* altering them unnecessarily; do not expose secrets.
- Record known-good release/tag, source revision, manifest, SHA and tested iOS version.
- Resolve or narrow [issue #2](https://github.com/raskal-labs/blink-rsk/issues/2), and sync its acceptance checklist.

**Exit gate:** One known restorable IPA, explicit test matrix and remaining limitations. Stop on unaccepted data-loss or provisioning risk.

### M1 — Daily terminal usability
**Status:** Proposed; former issue #3 returns HTTP 410 (deleted), observed October 26

**Goal:** Remove high-frequency frustrations with minimal terminal regressions.

**October 26 source review:** [upstream issues/discussions and personal-branch findings](docs/TERMINAL-UX-UPSTREAM-REVIEW.md) identify two tiny source corrections, a contained optional D-pad and existing controls worth exposing. Long-selection copying and scroll freezes still lack a demonstrated repair. This is research, not implementation authorization; the queued Files fix remains deferred to the next iteration's build.

**Priority A:** Investigate scrolling behavior across local Blink shell, SSH and Mosh, first outside Zellij/tmux; distinguish client defects from transport/application behavior before proposing a code fix. Other proposed improvements: independent Input versus Select/Scroll interaction; dependable Hide/Show Keyboard; accessible Select All (define scope); reliable selection and copying across scrollback; normal arrow-key option. Test landscape/portrait and software/hardware keyboard.

**Priority B:** Session overview/switcher and recovery; compact contextual action dock; jump to latest output; history search; clear connection status; clipboard Copy / Copy Raw / Share / Save Output; safer large/sensitive paste handling; quick help for gestures and shortcuts.

**October 27 clarification:** include an explicit Select All/Copy All control in the proposed clipboard scope. Local retained-buffer export and remote tmux/Zellij history over Mosh are different operations; neither may promise to recover output the client never received. [Source review and scope](docs/TERMINAL-UX-UPSTREAM-REVIEW.md#october-27-follow-up-other-complaints-copy-all-and-mosh-history).

**Preferred method:** Start with upstream gesture/keyboard/context-bar behavior. Investigate defects separately from UX preferences; do not rewrite terminal rendering or gesture handling prematurely.

**Exit gate:** Scrolling and input pass real-device regression tests and users can switch, select, copy and resume sessions without surprises.

### M2 — Personal identity and coherent navigation
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

**Current device feedback and associated tasks (reconciled October 27):** Host/session links and all three Shortcuts actions are **Verified** by user report: they appear and run. The October 25 discovery failure is historical and superseded; no registration repair is currently needed. Bookmarks remain **In Progress** with positive persistence feedback; failure/recovery and refresh checks remain. Files.app sync is **Blocked** by the persistent pending item, tracked separately. Remaining tasks under [issue #2](https://github.com/raskal-labs/blink-rsk/issues/2): detailed cancellation/invalid-input/SSH trust checks, bookmark recovery and refresh, independent Files.app transfers/reopen, and installed-artifact reconciliation. See [Shortcuts success and remaining acceptance](docs/phase-01/SESSION-ACTIONS-CANDIDATE.md#october-26-links-and-shortcuts-success).

**Current bounded batch (In Progress):** The October 24 work order combines bookmark recovery with a contained foreground adaptation of the October 12 session-link/Shortcuts changes, unmerged [PR #7](https://github.com/raskal-labs/blink-rsk/pull/7) and one successful authorized candidate CI build. URLs navigate only; command/script actions confirm in Blink and retain SSH verification. Background execution/output capture is deferred. Exact 18.7.1 callback restoration remains unestablished. Installation requires separate data-safe approval; merge awaits device acceptance. See [candidate evidence](docs/phase-01/SESSION-ACTIONS-CANDIDATE.md).

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

1. **M0 reliability and acceptance (issue #2):** bookmark repair is implemented and built; the user reports persistence improving and confirms links/all three Shortcuts work. Finish bookmark failure/recovery and refresh checks while preserving that positive evidence. Files sync is Blocked by the persistent pending item; the startup-cleanup backport is queued, with its build explicitly deferred to the next iteration. Verify transfers/reopen after native validation and an approved update; preserve rollback and earlier successful tests.
2. **M1 usability:** use the [October 26 source review](docs/TERMINAL-UX-UPSTREAM-REVIEW.md) to choose a bounded follow-up. Compare scrolling in local shell, SSH and Mosh, expose existing controls where sufficient, and keep selection/keyboard defects separate. The previously linked issue #3 is deleted; this review does not recreate it.
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
