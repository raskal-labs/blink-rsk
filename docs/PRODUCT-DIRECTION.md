# RSK.AL / Blink-RSK — product direction and decision record

Status: Living design document · Initial capture: 2026-10-12 · Owner: Raskal Labs
Implementation repository: raskal-labs/blink-rsk · Companion release/archive: blink-rsk-release
Related: [canonical roadmap](../ROADMAP.md) · [iOS integrations](IOS-INTEGRATIONS.md) · [UX research](UX-RESEARCH.md)

## Purpose and scope

Build a private, personally used, Raskal-branded iPhone terminal and lab interface on a known-working Blink Shell source foundation. The desired result is an excellent, fast, dependable native-feeling terminal that optionally exposes Raskal/Scout/Atlas and P2 capabilities, *not* a dashboard that compromises terminal reliability.

The user does **not intend to distribute** the application. This changes public marketing priorities, but does not remove GPL attribution obligations if it is conveyed to others, or Apple signing, capability, privacy, security and SideStore constraints.

## Authority and interaction boundaries (proposed clarification)

Blink-RSK owns its own local UI, terminal, sessions and file handoffs. It is an **interaction client**, not a replacement for Home Assistant, GameCube, Atlas, Polaris, Scout or Porygon. Those services retain their own records, job execution, permissions and event histories; the iPhone stays useful without any of them.

The same *bounded* action may eventually be available through Blink's palette, a Siri/App Intent, Shortcut, external deep link or widget. Shared presentation does not imply shared authority. Native navigation, read-only status and privileged remote execution have separate requirements; no external URI, beacon event, prediction or notification should become a blanket shell-execution grant.

Use existing iOS extensions and third-party apps first. The canonical [iOS integration research](IOS-INTEGRATIONS.md) holds the Siri/Pushcut/widgets/context investigations; additions remain **Proposed** until effective iPhone signing and on-device evidence justify them. WidgetKit, Control Centre extensions and background delivery require their own feasibility gates.

## Design principles (accepted direction)

1. Terminal-first: unobstructed fullscreen working mode and correctly functioning SSH, Mosh, tmux, Vim, other TUIs, Files SFTP and external keyboard.
2. Progressive disclosure: concise, discoverable interface around the terminal, not permanent dashboard chrome.
3. Touch-first and keyboard-complete; explicit Input vs Select/Scroll modes are a high-priority *proposal*, not an implemented decision.
4. Prefer exposing existing commands and actions, then adapting upstream code, then creating new implementations. Preserve upstream sync/rebase ability where practical.
5. Concrete runtime evidence outranks successful CI or source presence. Feature states: Mentioned, Proposed, In Progress, Verified, Blocked, Unknown. "Exists in source" is not "verified on this iPhone."
6. No automatic command execution by AI or prediction. All high-impact actions explicit, reversible where possible; protect credentials.
7. Preserve effective signing identity: current main and two extension bundle identifiers, App Group and keychain semantics, migration, existing Files domain and user data. Visual identity may change independently.
8. Economize CI builds, user interaction and SideStore App-ID budget. Reuse current installed app and known-good IPA; no speculative side-by-side installs.

## Product and naming decisions

| Topic | Decision / status | Notes |
| --- | --- | --- |
| Personal use | **Decided** | No public distribution planned. |
| Umbrella identity | **Preferred: Raskal Labs** | Developer/organization identity, not necessarily app title. |
| App name | **Undecided** | Candidates RSK.AL, PORYGON, P2, Raskal Labs; "RSK.AL" is a provisional working label only. |
| Separation of roles | **Proposed** | RSK.AL = shell/workspace; P2/Porygon = optional intelligence and wider agent layer; Raskal Labs = maker. If terminal becomes Porygon's primary iOS shell, revisit name. |
| Logo | **Concept generated, not finalized or committed** | Faceted metallic/crystal R + rocket/terminal prompt; dark background, cyan/teal, violet/magenta prismatic edges. Refine for small-size legibility and originality. |
| Branding | **Planned** | Icon, visible name, launch/splash treatment, Files location display, About/version strings, themes, typography, menus, docs; keep internal bundle IDs unchanged initially. |
| Lab visual direction | **Accepted direction, not an implementation spec** | High-budget contemporary low-poly/PS1-inspired forms, restrained refractive iridescent glass, translucence/parallax, geometric project icons, rich typography, deliberate colour; not gaudy cyberpunk chrome or unreadable decorative effects. |
| Distribution policy | **Private** | GPL compliance / acknowledgments still matter; do not infer trademark permissions or entitlement exemptions from private use. |

## UX goals and prioritized backlog

### P0 — interaction/reliability first

- Reliable keyboard hide/show and *optional keyboard lock*, preventing taps from constantly summoning it; retain input responsiveness when intended.
- Reliable select-all, copy/copy-raw, large scrollback text, scrolling, search, jump to live bottom; verify iOS 27 regression.
- Tab/session close/open/switch/rename, explicit close-vs-disconnect, discoverable session overview, and stable background/foreground terminal layout.
- Minimal contextual command dock with Escape, Control, arrows, clipboard, selection, keyboard and session actions; collapsible and not an obstruction.
- Safe, optional preview for multiline/escape-containing pastes; do not silently rewrite commands or interfere with bracketed paste/interactive apps.

### P1 — small native-feeling wins

- Favourites/recents for hosts, clear local vs remote host/status and SSH/Mosh/reconnect state.
- Searchable command palette for app actions, Snips, host switching and (clearly separate) command insertion.
- Symbol strip for programming punctuation; adaptive one-handed layout; physical keyboard and VoiceOver support.
- Inline shortcut/gesture reference grounded in actual configured actions.
- Read-only diagnostic report: app/build/ref, iOS, connection category, runtime capabilities; exclude secrets.
- Make existing Copy Raw, Share Selection, File Provider/SFTP transfer progress and native Files handoff discoverable.

### P2 — medium and exploratory

- Reliable session restore vs reattach semantics (remote tmux/Mosh differ from app-local tab restoration).
- Per-workspace views for infrastructure, development and minimal terminal; maintain simple fullscreen default.
- Structured machine/human outputs from Scout, RSK, Atlas; command progress and reporting aligned with wider lab.
- Shortcuts/App Intents and safe deep links to host/session/workspace. Require explicit user control for command execution.
- Contextual T9/Momentum Rail/operator clutch/ghost completion, QWERTY fallback; do not insert predictions unsolicited.
- Optional P2 assistant for selection -> Explain/Inspect/Propose. No permanent autonomous agent/unchecked shell authority.

## Cost discipline and build stages

The historical four-stage roadmap (parity, local Unix tools, homelab integration, UI/T9) is superseded by the root [M0–M5 roadmap](../ROADMAP.md). Research, prototyping and design may proceed out of milestone order; implementation acceptance gates remain conservative. Do **not** defer core UX improvements behind branding: prioritize verified P0/P1 fixes after protecting the working Phase 01 baseline.

Near-term milestone (provisional): "Identity & Usability" — initial visible Raskal branding plus a bounded set of P0 controls, tested against native Files and remote interactive apps. Do not combine a renderer replacement, new File Provider, session rewrite and visual redesign into a single release.

## Integration boundaries

- Canonical device/host facts belong to Raskal inventory/Atlas/infra; do not hardcode sensitive IPs or keys into app builds.
- Filesystem surveying/scanning now belongs to **Scout**; RSK consumes Scout's findings and exposes interfaces, rather than owning a new conflicting scanning pipeline. Existing roadmap language predating Scout must be corrected.
- P2/Porygon is optional and permission-scoped; the app remains useful offline and without AI.
- Reuse the existing iOS Files provider for file browsing; prefer transfer status/handoff instead of duplicating a whole file browser.
- Preserve documented upstream and third-party licence/credit notices.

## Open decisions (ask only when consequential)

- Final display name and relationship to P2/Porygon; final small-size icon; Files provider visible name.
- Dock default affordance and user-customizable actions; two-mode selection/typing details.
- Whether contextual T9 is worth implementation after usability benchmark.
- Exact safe automation policy, deep-link command confirmation and SSH agent forwarding posture.
- Configuration export/import support after actual read-only audit and round-trip verification.

## Maintenance instructions

Update this document when purpose, naming, architectural boundaries or decisions change. Keep detailed iOS experiments in [IOS-INTEGRATIONS](IOS-INTEGRATIONS.md), upstream usability evidence in [UX-RESEARCH](UX-RESEARCH.md), milestones in the [root roadmap](../ROADMAP.md), and accepted work in issues/Phase 01 receipts. Use the project's six statuses; a proposal is not an accepted decision or a verified device capability. Preserve dated reasons when superseding decisions.

## October 24 candidate boundary

The authorized bookmark/session batch keeps the pinned source and existing app identities. Use navigation-only saved-host/focus URLs; offer command/script execution through explicit foreground Shortcuts confirmation and the existing SSH trust flow. No URL-carried execution key, Fleet import, unattended runner or new extension belongs to this batch. Source/build verification is distinct from iPhone acceptance; functional changes remain unmerged until the latter. Details: [candidate record](phase-01/SESSION-ACTIONS-CANDIDATE.md).

## October 27 combined batch and next milestone

The current authorized batch expands foreground Shortcuts with returned SSH results, SFTP files/listing, Mosh/start commands, focus and saved-folder terminal opening. It includes the queued provider backport and only the two narrow Snips/gesture source corrections. One additional candidate CI build follows preflight; October 26 deferral is superseded. Links/all three original actions work and bookmarks have positive persistence feedback; broader acceptance remains separate. The mistaken Files sync report is withdrawn without inventing a transfer result. [Actual scope and device checklist](phase-01/SHORTCUTS-EXPANSION-CANDIDATE.md).

The next agreed milestone combines touch controls, terminal usability, workspace UI and appearance. Preserve M1/M2 research; do not implement it in this build. Select All/Copy All, optional D-pad, keyboard lock, large-paste, renderer/backpressure and Mosh mouse/scrollback experiments are excluded. Local retained-buffer copying is distinct from remote multiplexer history. Keep all app/provider identities, keys, migration and polling intact; no installation, replacement, provider reset or merge is authorized.

**Final October 27 build checkpoint:** the single authorized [run 40621641772](https://github.com/raskal-labs/blink-rsk/actions/runs/40621641772) passed native preflight but failed full iOS compilation on an iOS 18-only IntentFile parameter initializer. Correction `5d69100` passes local preflight and remains native-unbuilt. No candidate IPA, metadata/package acceptance or new device result exists; no second dispatch was made. [Exact results and checklist](phase-01/SHORTCUTS-EXPANSION-CANDIDATE.md).

**Superseding retry checkpoint:** user-authorized [run 40627574155](https://github.com/raskal-labs/blink-rsk/actions/runs/40627574155) compiled and signed the combined candidate. Its final checker failed on `resultValueType` versus Xcode's `outputType`; correction `c3ac048` passed against the same unchanged IPA. CI remains red, but a candidate is available with independently verified metadata/identity/CRC/SHA and explicitly labeled recovered receipts. Device acceptance remains Unknown; no installation/reset/identity change/merge or further build. [Candidate and checklist](phase-01/SHORTCUTS-EXPANSION-CANDIDATE.md#current-retry-result).

## Functional acceptance and customization transition — 2026-10-27

The user reports the combined candidate passing and is ready to move forward. Record functional acceptance as user evidence; retain unmeasured installed-checksum/refresh/per-case limits. PR #7 and issue #2 were already merged/closed by the owner. Keep the existing IPA and rollback archive intact; no new build, installation, provider reset, identity change or merge is inferred or performed.

Begin source/scope review for the agreed combined customization milestone: touch controls, terminal usability, workspace UI and appearance. Prefer extending existing quick actions, keyboard actions and theme/font/style previews. A compact collapsible control surface and lightweight native workspace launcher are proposed first-batch choices in the root roadmap; final detailed selection remains pending the user's preference. Do not turn retained clipboard, D-pad, keyboard-lock, large-paste or rendering/Mosh research into an automatic import.
