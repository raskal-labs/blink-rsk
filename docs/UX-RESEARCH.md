# RSK.AL — UX complaints, upstream work and related implementations

Status: Living research ledger · Captured: 2026-10-12 · Research basis: public Blink issues/PRs and public third-party source/docs
Related: [product direction](PRODUCT-DIRECTION.md) · [canonical roadmap](../ROADMAP.md) · [iOS integration research](IOS-INTEGRATIONS.md)
This is a bounded investigation, not a statistically representative survey or a claim that every report reproduces on our pinned build.

## Workflow / evidence standard

For each finding record: source URL, observed date/version, issue or commit/PR state, user-visible symptom, our pinned-code applicability, hypothesis, test, and final iPhone verdict. "Open PR" means proposed code, not released upstream. Search exact/related successes and failures before bespoke diagnostics; check one variable per test; re-research after 1–2 failed hypotheses.

## Community-reported UX problems

| Issue | Evidence | Blink/iOS context | RSK response | State |
| --- | --- | --- | --- | --- |
| Keyboard reappears after tap | [#2289](https://github.com/blinksh/blink/issues/2289) | Aug 2026; 18.6.3/iOS 26.6.1; maintainer proposed keyboard lock for 18.8 | Explicit optional lock, keyboard focus/selection testing | Report verified; implementation **Unknown** |
| Long selection truncated on copy | [#2278](https://github.com/blinksh/blink/issues/2278) | Jul 2026 18.6.2; 300 lines sometimes copied only tail; reporter says returned on iOS 27 | Exact-byte 300-line/wrapped/Unicode/tmux test, Copy Raw, export | Report verified; fix **Unknown** |
| Scroll can freeze terminal | [#2267](https://github.com/blinksh/blink/issues/2267) | Jun 2026 18.6.2; intermittent with Hermes/Vim, stalled until restart | Gestures + renderer repro on SSH, Mosh, tmux, Hermes/Vim | Report verified; reproduction **Unknown** |
| Foreground/keyboard damages viewport | [#2293](https://github.com/blinksh/blink/issues/2293), [#2294](https://github.com/blinksh/blink/issues/2294) | Sep–Oct 2026 18.7.1/iOS 26.6.x; some third-party keyboards and Mosh/tmux | App return, viewport resize, cursor and scrollback-state regression tests | Report verified; local state **Unknown** |
| Mouse movement/modifiers/right tap | [#2295](https://github.com/blinksh/blink/issues/2295), [#2296](https://github.com/blinksh/blink/issues/2296) | Oct 2026; gestures and mouse event modifiers | Test, then optional discoverable touch alternate click | Report verified; local state **Unknown** |
| Deep links/Shortcuts disrupted | [#2253](https://github.com/blinksh/blink/issues/2253), [#2290](https://github.com/blinksh/blink/issues/2290) | 2026; legacy x-callback restoration reported in 18.7.1 pending Intents | Exact host/session link, safe quoting, new-vs-reuse, explicit execution | Report verified; current-IPA state **Unknown** |
| Scrolling shortcut expectations | [#2261](https://github.com/blinksh/blink/issues/2261) | May 2026; iPad/tmux page-scroll shortcuts | Discoverable bindings, fine scrolling | Report verified; local state **Unknown** |
| Features hard to discover | Blink App Store user reviews and issues | Distinct from code lacking a feature | Guided shortcuts, command palette, progressive disclosure | Qualitative theme; do not claim prevalence |
| Pricing/subscriptions | App reviews, community discussions | Private self-built fork has a different context | Low priority, keep appropriate notices | Not a primary UX implementation target |

## Candidate upstream changes — inspect before adapting

| Candidate | Source | Public state at capture | Integration notes |
| --- | --- | --- | --- |
| Floating, draggable touch D-pad | [PR #2291](https://github.com/blinksh/blink/pull/2291) | Open; author reports hold-repeat/VoiceOver/keyboard-hide handling | Promising patch; check focus, orientation, existing modifier path and physical keyboard |
| Fine-grained line scrolling | [PR #2255](https://github.com/blinksh/blink/pull/2255) | Open; adds Cmd+Swipe, Cmd+Arrow | Adapts hterm scrolling; evaluate no-hardware-keyboard gesture and Swift project diff hygiene |
| Synchronized-output render smoothing | [PR #2287](https://github.com/blinksh/blink/pull/2287) | Open; iOS 27 simulator and iPad testing claimed by author | Potential TUI tear fix; rendering/JS global state/watchdog must be scrutinized |
| Dictation SmartKey | [PR #2297](https://github.com/blinksh/blink/pull/2297) | Open; author reports device test on iOS 26 | Future opt-in; permission, privacy, transcription/editing semantics |
| Keyboard lock | [Issue #2289](https://github.com/blinksh/blink/issues/2289) | Maintainer stated targeting 18.8; no public implementation verified here | Do not invent a committed fix; review future release/branches |
| URL/Intents | [Issue #2253](https://github.com/blinksh/blink/issues/2253) | Maintainer reported legacy restored in App Store 18.7.1; new Intents pending | Pinned 18.7.0 source != App Store 18.7.1; test before porting |

Baseline upstream pinned to [blinksh/blink@a90b4423](https://github.com/blinksh/blink/tree/a90b4423c8b7a86770c24a7eaa6c13b0a5904b18), 18.7.0 (1097). The public raw branch was observed still at that revision on Oct 12; do not conflate announced App Store features with source released on raw.

## Related projects and what to reuse

| Project | Research opportunity | Caveat |
| --- | --- | --- |
| [NewsGuyTor GPL Builder](https://github.com/NewsGuyTor/Blink-Shell-GPL-Builder) | Sideload and packaging source/history | Earlier test had Files failures; diffs may remove features and migrations. Our current minimal signing patch is preferred. |
| [rootshell](https://github.com/kitknox/rootshell) | Native tabs/exposé, project grouping, agent inbox, session continuity, theming, clipboard/host workflows | Large Ghostty/Metal-based app; ideas/components, not drop-in renderer |
| [Geistty](https://github.com/daiimus/geistty) | Session management, tmux control mode, touch panes, native keyboard and command palette | Uses Ghostty; project says experimental/on hold |
| [Geistty File Provider learnings](https://github.com/daiimus/geistty/blob/main/FILE_PROVIDER_LEARNINGS.md) | **Important failed-case evidence:** SFTP sync anchors, SQLite/working set, error resolution, aggressive Files cache | Their attempted File Provider was archived after persistent "Syncing Paused"; do **not** replace our working provider |
| [gterm](https://github.com/madeye/gterm) | Custom iOS symbol/accessory keyboard, SSH UI, unsigned IPA sideload flow | Ghostty/Zig passthrough architecture; not a direct Blink patch |
| [a-Shell](https://github.com/holzschu/a-shell) | Expanded iOS Unix/ios_system features and Shortcuts patterns | Distinct sandbox and tooling; verify selected commands individually |
| [Shio](https://github.com/shio-sh/shio) | Projects-first workspace, Shortcuts, tmux, widgets/Live Activities and restrained product scope | Maintainer deliberately removed agent supervision: preserve terminal-first boundaries; Ghostty backend |
| [SimpleSSH](https://github.com/miguelju/simplessh_ios) | Lightweight SwiftUI styling/toolbar/host UI, Liquid Glass | Examine source and maintenance before reuse |
| [Code App](https://github.com/thebaselab/codeapp) | Future native editing/IDE and embedded terminal | Separate large IDE; don't import as a prerequisite |
| [Blink Snips index](https://github.com/blinksh/snippets) | Existing templated commands; no need to recreate a command-snippet library | Index WIP and availability/import should be tested |

All third-party reuse requires a licence/notice review and compatibility check. Separate "inspired by design" from direct code reuse, and never assume Ghostty/native renderer changes are compatible with Blink's hterm/WebView.

## Product research conclusions

- Blink's minimalism is a strength; discoverability and touch precision are high-return targets.
- Existing commands/settings/selection tools are cheaper to surface than rebuilding them.
- Preserve working native Files; borrow only relevant failure lessons from other File Provider implementations.
- Strong candidate for the first usability milestone: contextual dock + keyboard lock/hide + stable text selection; then session overview and shortcuts.
- Avoid bundling unverified PRs wholesale, mixing multiple renderer/input changes, or attempting new provisioning flags to fix cosmetic issues.

## iOS workflow measurement (proposed)

The broader Home Screen / Control Centre study should compare app and system entry points using observable interaction cost, not subjective icon preference alone. Candidate inputs: app usage and pickup summaries, inventory of installed extensions and Shortcuts, task-specific navigation recordings, opted-in Blink action counts and relevant HA/host actions. Screenshots and selected test workflows are acceptable when telemetry is inaccessible. Do **not** infer touch coordinates, precise app-launch counts, Siri personal-context data, or cross-app event streams from APIs that do not expose them. Record baseline, alternative, device conditions and uncertainty; move only demonstrated improvements into the canonical roadmap.

## Research follow-ups

- [ ] Check upstream 18.8 publicly accessible source for the keyboard lock; verify its actual commit/release.
- [ ] Diff each promising PR against pinned hterm/SmartKeys/input paths; rate portability/risk.
- [ ] Run device regression matrix: 300-line selection (UTF-8/wrap/tmux), app background/foreground, output flood, selection mode, SFTP File Provider, keyboard presence.
- [ ] Compare missing/hard-to-discover UI with rootshell/gterm/Geistty/Shio actual code, not just marketing claims.
- [ ] Reassess candidate ranking after measured regressions. Record results and dates here; move confirmed milestones into the [root roadmap](../ROADMAP.md), actionable implementation into GitHub issues, and test receipts into Phase 01 evidence records.

## Entry template

### YYYY-MM-DD — finding or experiment
Source/version: URL, app revision, iOS, signing conditions.
Symptom / expected:
Hypothesis and cheapest isolating test:
Result: Verified / Blocked / Unknown; artefact/log links.
Effect on priority and next step:
