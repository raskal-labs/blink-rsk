# RSK.AL / Blink-RSK — product direction and decision record

Status: Living design document · Initial capture: 2026-10-12 · Owner: Raskal Labs
Implementation repository: raskal-labs/blink-rsk · Companion release/archive: blink-rsk-release
Related: [ROADMAP](ROADMAP.md) · [UX research](UX-RESEARCH.md) · feature inventory and verification/state (planned documents; not yet created)

## Purpose and scope

Build a private, personally used, Raskal-branded iPhone terminal and lab interface on a known-working Blink Shell source foundation. The desired result is an excellent, fast, dependable native-feeling terminal that optionally exposes Raskal/Scout/Atlas and P2 capabilities, *not* a dashboard that compromises terminal reliability.

The user does **not intend to distribute** the application. This changes public marketing priorities, but does not remove GPL attribution obligations if it is conveyed to others, or Apple signing, capability, privacy, security and SideStore constraints.

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

Current upstream roadmap has four stages (parity, local Unix tools, homelab integration, UI/T9). Research, prototype and design can proceed out of numerical stage order; implementation acceptance gates remain conservative. Do **not** defer all core UX improvements to Stage 4: slot small P0/P1 improvements into the first branded build after preserving the working Phase 01 milestone.

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

Update this document when scope, naming, visual design, or explicit decisions change. Track source links/repro steps in UX-RESEARCH; code capabilities in FEATURE-INVENTORY and evidence/checkpoint in PROJECT-STATE **once those documents exist**; until then use existing tracked acceptance/phase documents. Execution phases belong in ROADMAP. When promoting a proposal to Decided/Verified, record the date, responsible change/commit or on-device evidence, and follow-on work. Do not silently convert assistant recommendations into user decisions.
