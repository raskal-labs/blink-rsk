# iOS integrations — Home Assistant, Shortcuts, links and widgets

**Captured:** 2026-10-13 · **Status:** Proposed, unless explicitly marked otherwise  
**Scope:** Research and staged product integration for Blink-RSK as a personal iOS workspace. This is NOT implementation authorization.  
**Parent:** [Product roadmap](../ROADMAP.md)

## Purpose and decision

**Integrate before merging.** Maintain the working Blink-derived terminal and File Provider, and let Home Assistant, iOS and existing homelab services continue doing what they do well. Bring their useful interactions into the personal iOS workspace through secure, replaceable interfaces.

The initial notion of merging the whole Home Assistant Companion app into Blink is **superseded**. It is not needed to test or deliver useful Home Assistant interactions.

The personal iOS app's eventual composition—Blink as host, component, or coexisting independent app—remains **Unknown**. Avoid pre-committing to a rewrite.

## Screenshot: SideStore signing state (dated observation)

User-supplied SideStore My Apps screenshot at approximately **2026-10-13 20:49 PDT**:

| Observed field | Value | Interpretation |
| --- | --- | --- |
| iOS | 27.0 (24A437) | Device screenshot only |
| SideStore | `0.7.0-20260918.492+12a496ca` | Version shown in footer |
| LiveContainer | `3.8.10-Release (main/4dbe0f9)` | Version shown in footer |
| Active list | **Blink**, **LiveContainer** | Two entries displayed; SideStore itself is not listed there. **Do not** infer a free third native app slot. |
| App IDs remaining | **5** | Supersedes earlier snapshot of 4; exact registered bundle/extension IDs require **View App IDs** inspection. |
| Expiry indicator | **7 DAYS** on each listed app | UI readout only; not proof the next automatic renewal will succeed. |
| Updates | `No Updates Available` | Store update status, not an extension or entitlement test. |

**Important distinction:** Free-account limits on simultaneously installed apps, registered identifiers, and individual app-extension bundle identities are not interchangeable. Check the live counters and registered IDs immediately before any install or entitlement/extension experiment. The [SideStore FAQ](https://docs.sidestore.io/docs/faq) describes free-account limits, including SideStore itself.

**Never create a new native app/widget target, switch signing identity, overwrite installed data, or consume an App ID as an unannounced experiment.** Keep the File Provider and rollback assets safe.

## Existing interoperability surfaces (do not reproduce as custom features yet)

| Surface | Recommended approach | Status |
| --- | --- | --- |
| HA scripts, automations, sensors and entities | Use the existing Home Assistant installation on GameCube as the canonical home-automation engine | Proposed integration |
| HA iOS widgets, Siri, Shortcuts, Control Center and actionable notifications | Test the official Home Assistant Companion app before building any RSK-native equivalent | Proposed / capabilities require specific-device check |
| Blink sessions, SSH/Mosh and SFTP/File Provider | Keep Blink as the stable interactive endpoint | Existing working capabilities; detailed build acceptance still In Progress |
| Saved-host and session deep links | Inspect new upstream Blink link/Intents code before any custom URL dispatcher | Proposed source audit |
| Server automation, policy, scheduling and logs | Reuse HA scripts and authenticated server-side actions on GameCube; Atlas/Polaris manage their own domains | Proposed |
| Native RSK WidgetKit extension | Optional independent spike; no implied signing success | Unknown |
| Dynamic Island / Live Activities | Optional later feature; verify entitlement/background behaviour and need | Mentioned |
| Godot apartment digital twin | Potential HA client in the *Godot project*, not a reason to embed a game engine in Blink-RSK | Mentioned / outside immediate scope |

No reliable always-on arbitrary background SSH execution should be assumed on iOS.

## iOS capability and interaction audit (proposed, non-build work)

**Goal:** improve the entire iPhone experience, not merely the Blink icon layout. Inventory the current Home Screen, Lock Screen, Control Centre, Action Button, Share Sheet, Files locations, Siri/Spotlight actions, available widgets and app extensions. Include capabilities from apps not currently installed and privileged system roles (Network Extension, Screen Time, credentials, File Provider, etc.), but distinguish entitlement from functional permission on this exact device.

For each candidate record: installed/configured/unused/unknown; required iOS role or extension; native or server-side ownership; Shortcuts/App Intents availability; signing and recurring costs; competing existing tool; observable benefit and device evidence. Use [UX research](UX-RESEARCH.md) for lengthy study notes and the [canonical roadmap](../ROADMAP.md) for justified milestones. Avoid a separate sprawling feature checklist until repeated audits demonstrate the need.

**Objective measurement:** Screen Time summaries, Battery activity, layouts, Shortcuts executions, selected Home Assistant events and explicitly instrumented Blink actions may reveal workflow cost. These data do not grant Blink access to other apps' taps, a complete usage ledger, or Siri's private personal context. Siri prompts are discovery tests, not guaranteed introspection APIs. Any Blink telemetry must be opt-in, minimal, locally controlled and removable.

### Pushcut, events and indoor proximity

- **Pushcut:** evaluate its actionable notifications, URL/webhook actions, widgets, iBeacon proximity and iOS Automation Server against already-available HA Companion notifications, Shortcuts and GameCube. Reuse providers first; do not make an always-on iOS executor a prerequisite for Blink.
- **Event inbox (Proposed):** a small view of *selected* HA/Atlas/host events with source IDs, timestamps, receipts and deep links, not another authoritative event ledger or a new APNs service. Start read-only after the external action/notification pilot passes.
- **Context awareness (Proposed):** suggest or order actions by verified network, VPN, Focus or HA signals. Optional Core Location/iBeacon monitoring is a separate on-device experiment requiring permission, background-behaviour, signal-overlap and battery checks; proximity is never an authorization factor for sensitive actions.
- **Unified entry points (Proposed):** a small typed catalogue of *existing* Blink navigation and approved remote actions could be exposed via command palette, App Intents, Home Screen quick actions and later widgets. Separate navigate/query/execute security scopes, use allowlisted targets, and never place bearer tokens or arbitrary shell commands in external URLs.

## New primary source finding: Blink session links and App Intents

### Verified source existence, not verified compatibility

- Blink's App Store **18.7.1** explicitly restored the `blinkshell` callback scheme. See [Blink issue #2253](https://github.com/blinksh/blink/issues/2253) (maintainer confirmation 2026-09-17) and the App Store release history.
- On **2026-10-12**, upstream commit [`7a427f3db37ec25869b24226905d89103a8ad99d`](https://github.com/blinksh/blink/commit/7a427f3db37ec25869b24226905d89103a8ad99d) introduced a richer *source implementation*:
  - `blinkshell://run?cmd=...` — open a command session;
  - `blinkshell://host/<alias>` — connect to a saved host, with Mosh and command options;
  - `blinkshell://focus?id=...` — return to an identified session;
  - **Run Command on Host**, **Run Script on Host**, and **Open Terminal Session** App Intents/Shortcuts, with a host picker; legacy Fleet shortcuts retained.
- The commit's link actions default **off**. It implements a confirmation path if the key is absent; a matching user key permits no-prompt execution. This feature is **not** assumed present in Blink-RSK's pinned 18.7.0 source, nor installed/tested via SideStore.
- Source security concern: the general Shortcuts runner passes `acceptUnknownHostKeys: true` for host actions in the observed patch. For unattended RSK use, verify the trust-on-first-use policy against the desired SSH host-key security standard; prefer known-host verification or an explicit enrollment flow. **Do not silently copy this behaviour.**
- A URL-carried execution key can leak via links/logs/sync and may become an arbitrary-command capability; scrutinize the model. Prefer fixed, allowlisted actions, scoped server authorization, audit events, and explicit confirmation when risk warrants it. Separate navigation-only links from command execution.
- Inspect upstream commit's source dependencies, `SceneDelegate`, `SpaceController`, `SessionLink`, Intents, persistent settings and tests; confirm compatibility with the pinned baseline, custom signing, URL scheme registration, File Provider, keys and Mosh. Avoid blindly merging a new moving branch.
- Upstream statements about future Intents do not prove an App Store release or SideStore runtime functionality. The above is **Verified source evidence; device feasibility remains Unknown**.

Source context: [Blink #2253](https://github.com/blinksh/blink/issues/2253), [Blink #2290](https://github.com/blinksh/blink/issues/2290), [commit 7a427f3](https://github.com/blinksh/blink/commit/7a427f3db37ec25869b24226905d89103a8ad99d).

**Source availability rechecked 2026-10-23 on GameCube:** GitHub's public branch/tag listings still expose `raw` at `a90b4423` and no named 18.7.1 release ref. The October 12 commit above is nevertheless retrievable by its exact SHA; do not equate missing branch/tag names with all newer source being unavailable. Its project still declares app version 18.7.0/build 1097. `Settings/Model/BookmarkedLocationsManager.swift` has the same blob SHA (`baf1ab7111ab9422de6b29f82c570860a2ee8fe7`) at both commits, including the destructive filtering of inaccessible bookmarks. This confirms availability of the newer link/Intents patch, not the later bookmark hardening described in [discussion #2247](https://github.com/blinksh/blink/discussions/2247), exact App Store source parity, or safe compatibility. Review callback restoration, richer Intents and bookmark recovery separately.

## October 24 bounded candidate decision

**Status: In Progress.** The user's combined work order supersedes the earlier read-only I1 sequencing for this batch and authorizes one CI candidate build after preflight, with no installation or merge. [The implementation record](phase-01/SESSION-ACTIONS-CANDIDATE.md) documents the exact source review and limitations. The public ref recheck still found no named 18.7.1/restoration source or compatible bookmark repair.

Selectively adapt the host picker, Open Terminal Session, Run Command/Script on Host and named session/focus behavior from `7a427f3`, retaining the `a90b4423` source pin. URLs support saved-host/focus navigation only and reject command/key payloads. Shortcuts commands/scripts require foreground confirmation and run through the existing verified-host SSH terminal; output stays there. No Fleet system, headless runner, URL secret, automatic unknown-key acceptance, new target or signing change is imported. The single [candidate CI run](https://github.com/raskal-labs/blink-rsk/actions/runs/40128366917) passed native tests, iOS compilation and packaging; [PR #7](https://github.com/raskal-labs/blink-rsk/pull/7) remains unmerged. Source/build results are Verified. On October 26 the user also confirmed host/session links and discovery/basic execution of all three actions on the current iPhone installation. Detailed safety, recovery and refresh acceptance remain separate; the exact installed IPA SHA is not independently established. See the [device record](phase-01/SESSION-ACTIONS-CANDIDATE.md#october-26-links-and-shortcuts-success). Background execution and output-returning actions require separate lifecycle/authentication work.

## Narrow staged roadmap

| Step | Status | Sequence, dependencies, exit criteria |
| --- | --- | --- |
| I0 — Existing iOS/HA flow | Proposed | **Without a Blink rebuild**, configure one HA action/widget, run one safe GameCube-side script, collect a result, and send an actionable notification using the official Companion app. Opening a known Blink session is an optional extension until link feasibility is established. Exit: repeatable approved action and visible result. |
| I1 — Session link / Shortcuts source audit | In Progress | Read and security-review upstream 7a427f3 plus the 18.7.1 callback change; test any already-installed scheme without arbitrary commands; choose a small, separately reviewable compatibility patch *only after* M0 accepts the installed build. Exit: evidence-backed go/no-go for a safe saved-host/session navigation mechanism; no build is authorized here. |
| I2 — End-to-end cross-app workflow | Proposed | Join I0 and I1 if links work: **Atlantis backup failure → HA notification → View Logs opens the correct Blink session**; Retry maps to a named approved server action. Exit: proper host/session targeting, bounded authority, explicit action status and audit trail. Fallback: open Blink manually from notification context if no safe deep-link route exists. |
| I3 — Native WidgetKit feasibility | Unknown | Only if official HA widgets fail to serve a concrete use case; independently check current ID/slot budget, legitimate provisioning and App Group sharing, gallery registration, refresh, locked-device interaction and a full seven-day re-sign cycle. Use isolated branch/candidate and explicit approval; do not destabilize installed Blink. Stop on repeated entitlement or App Group failures. |
| I4 — Optional HA CLI / structured action UI | Proposed, conditional | Investigate `ha status`, `ha entities`, `ha run`, authenticated API client and a small in-app action view only if real workflows need them. Do not invent a second automation engine. |
| I5 — General-purpose extensibility | Mentioned | Server-driven read-only widgets, dashboards, search, capture, rich data rendering, reusable action descriptions, Live Activities. Reassess after two independent integrations reveal the same abstraction is useful. |

**Dependencies:** Main roadmap M0 stability and M1 interaction fixes are not replaced by these steps. I0 can proceed separately using existing HA and app surfaces; I1 is a read-only audit until M0 clears any build-risk. No future module has blanket permission for unrestricted remote commands.

## Example: Atlantis failure, minimal integration

1. GameCube produces an Atlantis failure event, including an opaque job/reference ID rather than sensitive logs in URLs.
2. Home Assistant delivers an actionable notification through its official iOS app.
3. **View Logs** opens or directs the user to the known Blink host/session (subject to I1 verification).
4. **Retry** calls a named, server-validated recovery action; it is not a `shell` field supplied in a notification.
5. HA/Atlas/Polaris surfaces a canonical status/event/receipt according to existing project ownership.
6. Optional later widget reads the last **verified** backup status.

**Success condition:** helpful workflow through existing services, not a rewritten HA app.

## Known native and signing risks

- WidgetKit requires an actual app widget extension, not just a LiveContainer guest script.
- SideStore free-account signing of extension App Groups is not assumed reliable: [SideStore issue #1437](https://github.com/SideStore/SideStore/issues/1437) reports a widget unable to read its shared UserDefaults when sideloaded (opened 2026-08-20; closed, resolution unverified).
- Widget timelines are scheduled by iOS; a widget is not a permanent real-time service.
- Native widget registration, Interactive WidgetKit intents, locked-device actions and data sharing each need distinct on-device evidence.
- The RSK build cannot borrow HA Companion's APNs identity/token. Continue using the official Companion app for remote push unless there is a separately justified native push solution.
- Keep admin keys/tokens off widget surfaces; avoid copying HA long-lived tokens into URL parameters, logs, clipboard or public docs.
- For any app URI intent, validate parsed host/path/action IDs; distinguish navigation from execution; avoid arbitrary `cmd=` strings from third parties.
- Avoid high-risk infrastructure actions without confirmation, explicit scope and server-side authorization.

## Historical app/tool comparison (research notes only)

Source capsule listed **Scriptable** (last reported 1.7.19 / 2024-09-30; formal maintenance status Unknown), **Widgy** (visual programmable widgets), **Pushcut** (actionable notifications, automation server, beacon triggers), **WidgetPack** (Shortcut-driven widgets), **WidgetDash** (API-driven sensor widgets), and **Home Assistant Companion** (existing free integration).

Prices, free limits and version numbers from the earlier capsule have **not been refreshed** and must be verified when a purchase or tool choice matters. Maintain a bias toward free and official HA capabilities, but do not make one-app consolidation an objective of its own.

Useful examples to revisit, **external URLs not independently validated as implementations**:

- [Home Assistant animated 3D apartment floorplan](https://www.reddit.com/r/homeassistant/comments/1wzc637/my_floorplan_dashboard_got_out_of_hand_live/)
- [Nintendo 3DS Pokémon-style HA controller](https://www.reddit.com/r/homeassistant/comments/1wqty9u/nintendo_3ds_home_assistant_and_pok%C3%A9mon/)
- [HA CarPlay widget exploration](https://www.reddit.com/r/homeassistant/comments/1tj8gq3/carplay_widgets/)
- [Scriptable HA sensor example](https://github.com/olahellgren/home-assistant-sensor-widget-scriptable)
- [Pixel-art HA floorplan](https://strawberrysec.net/homelab/Home-Assistant-Pixel-Floorplan/)
- [GlassHome](https://glasshome.app/)
- [HA Neon Cards](https://github.com/cerealkiller57540/Home-Assistant-Neon-Cards)

## Placement and tracking

This document contains **research, source receipts and workstream decisions**, not a second global roadmap. The main [ROADMAP.md](../ROADMAP.md) links here under M4 and M5; issues #2 (signing/Files) and #3 (terminal UX) are unchanged. Do **not** create one issue per speculative widget feature. Promote an integration to a task only when its scope, reason, safety gates and acceptance criteria are concrete.

**Immediate best experiment:** I0, one existing Home Assistant workflow with no new IPA, followed by the read-only I1 source evaluation. Preserve the current Blink release and SideStore App ID budget.
