# Session links and Shortcuts candidate — 2026-10-24

**Status: In Progress.** This record accompanies the bookmark candidate under [issue #2](https://github.com/raskal-labs/blink-rsk/issues/2). The user's October 24 work order authorizes source work, a PR and **one** candidate CI dispatch after preflight. Installation requires separate data-safe approval; merge awaits device acceptance.

## Source review

Rechecked current PRs, remote heads, upstream branches/tags and relevant source history before editing. `origin/main` remains `02aad479`; PRs #1/#4/#5/#6 are merged and no implementation PR intervened. Reused the pending bookmark patch/tests; left unrelated `docs/UX-RESEARCH.md` changes outside this batch.

Public `raw` remains `a90b4423c8b7a86770c24a7eaa6c13b0a5904b18`, 18.7.0/1097. No named 18.7.1 ref or exact callback-restoration source was established. The available SceneDelegate history shows April removal `796a8789`, then [October 12 integration `7a427f3`](https://github.com/blinksh/blink/commit/7a427f3db37ec25869b24226905d89103a8ad99d). [Issue #2253](https://github.com/blinksh/blink/issues/2253) records the shipping callback restoration separately. This candidate does **not** claim 18.7.1 or legacy x-callback compatibility.

The newer commit's bookmark manager is identical to the pin (`baf1ab7111ab9422de6b29f82c570860a2ee8fe7`). The latest default-branch manager-history entry, `c6187a84`, dates to May 2025 and is already in the pin; it is not a new repair. Existing October 23 upstream/fork investigation found no compatible later repair. This bounded recheck found none either. Keep the focused [bookmark patch](M0-BOOKMARK-RECOVERY.md).

The October integration's new Intents depend on `HeadlessSSHRunner`, `FleetIntentError`, `FleetInterpreter`, `FleetScript` and `ExitTrailer`, plus settings and FleetCore registration. The headless runner adds dedicated-thread/run-loop lifecycle, authentication and exit/output capture; its unknown-key acceptance defaults true. Importing that execution path would require additional lifecycle, cancellation/output-bound and authentication testing. Those are the concrete blockers to claiming upstream-compatible background/output-returning actions in this batch.

## Contained adaptation

Reuse upstream's host entity/query, three action names, session naming/focus pattern and script encoding approach. Preserve the upstream GPL/section-7 notices. The patch adds two main-app Swift files and changes only SceneDelegate, SpaceController and their project registration; no Fleet package, targets, entitlements or URL registration changes.

| Entry point | Candidate behavior |
| --- | --- |
| `blinkshell://host/gamecube?id=logs` | Validate a plain saved alias; reuse that named open session in the current window, or ask **Connect** before opening SSH. `id` is optional. |
| `blinkshell://focus?id=logs` | Focus an existing named session in the current window. Missing/closed session produces an error; no command runs. |
| Open Terminal Session | Open a local terminal, connect to a saved host after confirmation, or reuse/focus a named open session. SSH only. |
| Run Command on Host | Foreground **Run/Cancel** showing saved alias and exact command, then a fresh SSH terminal. Never reuse an execution session. |
| Run Script on Host | Same confirmation, showing the original script; encode as base64 for `sh`, `bash` or `python3` on the remote host. Host needs `base64 --decode`. |

URLs reject `run`, `cmd`, `script`, `key`, unknown/duplicate query items, fragments, userinfo, ports, unsafe/overlong aliases and invalid session names. No URL execution key or key-bypass settings exist. Use Shortcuts parameters for commands; do not put credentials in commands/scripts or links. No request/URL contents are logged by this integration. Alias/name identifiers themselves can disclose context when shared.

Actions always open Blink; completion means the terminal was opened, **not** remote success. They return no output or remote exit status to Shortcuts and provide no unattended/background promise. Output stays in Blink's normal terminal. Session names are in memory, per window, until sessions/app close; they are not persistent recovery identifiers. Closed-session mappings are pruned. Other windows are not searched.

SSH goes through the existing terminal client, original keys/agent and known-host verification with explicit `StrictHostKeyChecking=yes`; there is no automatic acceptance override. Unknown/changed hosts still require Blink's existing visible trust prompt. Cancel the connection and verify fingerprints independently before enrolling an unknown or changed key. Saved-host existence is checked before and after confirmation. Local shell metacharacters are quoted into one remote-command argument. The shared existing `runShellSessionIntent` also avoids synchronously dispatching to the main queue when already on it.

## Verification and device gate

Local checks: exact input hashes and new-path collision guards; Swift parsing of UI/Intents files; compiled pure Swift navigation/action validation; malformed/command-bearing URLs; session reuse policy; script round trip; seven actual shell/fake-SSH boundary fixtures. These establish logic and POSIX quoting, not ios_system runtime parsing or UIKit confirmation behavior. CI must compile the actual Apple code; device tests must verify action discovery, cold/warm launch, cancellation, SSH trust and execution boundaries. Combined build/artifact results are recorded in [the candidate receipt](m0-bookmark-recovery.json).

Combined iPhone checklist, after a separately approved data-safe install route using existing identities:

1. Record installed/candidate identity and SHA; protect current keys, hosts, files and migration state. Do not infer install safety from CI. No app replacement is authorized by this record.
2. Bookmark a disposable folder; relaunch. Make its provider temporarily unavailable by an agreed reversible method: alias stays **Unavailable** through retry/relaunch, healthy neighbors work. Restore and retry; cancel reselection once, then reselect if required. Relaunch again. Already-erased entries require **+** and folder selection again, using an unused alias if a leftover link occupies the old name.
3. Delete only a disposable bookmark; relaunch. Its target/sentinel and unrelated alias conflicts remain intact.
4. Open a saved-host link and cancel: no session/connection starts. Accept a harmless connection; focus the named session repeatedly. Try closed/unknown names and a command/key-bearing URL: no execution. Check both cold and warm app launch.
5. Find all three actions in Shortcuts. Open/focus a session; cancel a command and script, then run harmless `printf` fixtures on a known host. Check quotes, literal `$()`/semicolons and multiline script behavior. Output must appear only on the intended remote host's terminal. Verify unknown/changed SSH keys still prompt; never accept a mismatch as part of this test.
6. Original SSH/Mosh, SFTP/SCP and iOS Files **browse, download, upload, reopen** remain separate checks. Record refresh/persistence later in a separately approved refresh session. Do not merge or advance the baseline until device acceptance.

## October 25 device feedback and follow-up (historical blocker)

User reports bookmarks are persisting well. Status: **In Progress**, with positive device evidence; temporary-provider failure/recovery and refresh have not been established. Exact installed candidate identity remains **Unknown** because the older and newer IPAs share a filename/version.

Shortcuts discovery at this checkpoint: **Blocked** (superseded by October 26 success below). The user reports no actions after opening Blink and restarting the iPhone. Packaged metadata has all three actions with `isDiscoverable: true` and the AppShortcutsProvider. Source inspection found no `BlinkSessionShortcuts.updateAppShortcutParameters()` call. This is a repair hypothesis, not a demonstrated root cause; SideStore rewriting/signing and installed-build identity also need checking. Apple's [WWDC23 guidance](https://developer.apple.com/videos/play/wwdc2023/10102/) demonstrates parameter refresh; it does not establish that omitting it explains this device failure. SideStore issue #1199 supplies no verified matching repair.

Associated tasks under [issue #2](https://github.com/raskal-labs/blink-rsk/issues/2):

- [x] **Verified:** inspect the candidate IPA for all three discoverable action declarations and provider metadata.
- [x] **Verified:** capture user report that launch/restart did not restore discovery.
- [ ] **Unknown:** reconcile the installed IPA with the October 24 download/artifact.
- [x] **Verified (user report, October 26):** the discovery blocker cleared; no registration/signing repair was demonstrated or applied.
- **Proposed repair deferred:** no lifecycle registration change is justified by the current successful result; revisit only if a failure recurs on an identified build.
- [x] **Verified (user report, October 26):** all three actions appear and run. Cancellation, negative inputs and SSH trust checks still need their own observations.
- [ ] **In Progress:** retain positive bookmark feedback and finish failure/recovery and refresh acceptance.
- [ ] **Unknown:** independently establish current Files.app browse/download/upload/reopen behavior.

This documentation update does not dispatch another build, change app identity or install anything. PR #7 remains unmerged.

## October 26 host-link feedback (initial unsuccessful attempt)

**Host/session link acceptance at this earlier attempt: Blocked; cause: Unknown.** The user reports that the suggested host link opened Blink to the existing activity without connecting or establishing the requested session. After initially selecting an error-message answer, the user clarified that **no error message appeared**; retain the later clarification. The user is not sure whether the installed IPA came from October 24 run `40128366917`. Do not attribute this result to the built candidate as an established fact.

The October 24 source handles both cold-launch URL contexts and running-app URL contexts. A handled host link should either request connection confirmation or show a generic error. A saved alias must match the GUI Hosts entry exactly (case-sensitive `BKHosts.withHost` lookup); a working SSH-config alias alone does not establish that entry. These are source observations, not a device diagnosis. The `id` parameter is an in-memory return-to-session mapping, **not a visible session/tab rename**; earlier chat wording was imprecise.

Proposed diagnostic at that checkpoint (no longer needed after the later success report): with Blink already showing the terminal and no modal dialog open, use Shortcuts **Open URLs** with `blinkshell://focus?id=rsk-probe-20261026`. No session with that probe ID has been requested. If the candidate handler receives it, it should show **Could not open session…**, without starting SSH or creating a session. Record the observed result before proposing a code fix. Silent app resumption would leave installed-build/app routing or URL delivery/presentation unresolved; it would not establish a particular cause. No additional build, app installation, identity change or phone-data operation is authorized or performed by this investigation.

## October 26 links and Shortcuts success

**Verified (user report):** host/session links and basic discovery/execution of all three Blink Shortcuts actions on the user's current iPhone installation. After saying they might have been using an older version and receiving the October 24 candidate download link, the user reported “they work.” When explicitly asked whether all three Shortcuts actions also appear and run, rather than only the links, the user confirmed “yep!”

This supersedes the earlier link/discovery blocker for current use. It does not establish that a registration/lifecycle defect caused the earlier symptoms; installed-build confusion remains a possible explanation, not a proven cause. No source fix, second build or agent installation was performed. The exact installed IPA SHA has not been independently checked, and the success report alone is not an install/signing receipt.

Remaining acceptance: detailed cancellation/invalid-link and SSH trust behavior; bookmark temporary-unavailability/reselection/deletion and post-refresh recovery; original connection regressions and independent Files.app browse/download/upload/reopen. Preserve the positive bookmark-persistence report. M0 and issue #2 stay In Progress, and PR #7 stays unmerged pending the remaining acceptance. The `id` remains an internal focus mapping, not a visible tab rename.

## Final candidate receipt

**Build/structure: Verified; iPhone links/basic Shortcuts: Verified (October 26 user report); remaining device acceptance: In Progress.** The one authorized [CI run 40128366917](https://github.com/raskal-labs/blink-rsk/actions/runs/40128366917) passed Xcode 26.6 native tests and complete iOS Release compilation at `38bd29221485c5306813c3916048bc77772d642b`. All three actions are present in packaged App Intents metadata. No diagnostics were emitted against the new Intents/model or bookmark files. Signing and packaging checks passed with the original IDs and both extensions. [Draft PR #7](https://github.com/raskal-labs/blink-rsk/pull/7) remains unmerged; later receipt-only documentation commits do not change the built source.

The IPA, SHA-256, harness source, source/patch manifests, logs and build/run receipts are archived under `/lab/blink-rsk-release/bookmark-session-20261024-run-40128366917/`. IPA SHA-256: `f28f1cc76f862bb4e3241c081b78dbd5cffa289b3a1bd96d6e89508209dbf151`. See [the machine-readable receipt](m0-bookmark-recovery.json) for its exact path and verification scope. Both rollback IPAs remain intact. No phone install/replacement, refresh, backup, data migration, identity change or merge was performed.
