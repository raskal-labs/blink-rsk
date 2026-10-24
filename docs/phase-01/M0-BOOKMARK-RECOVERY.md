# M0 bookmark preservation and recovery

**Status: In Progress.** Work order: [issue #2](https://github.com/raskal-labs/blink-rsk/issues/2), bookmark follow-up dated 2026-10-23. This is an implementation and acceptance record under the [root roadmap](../../ROADMAP.md), not a second roadmap. The October 24 work order now authorizes one candidate CI build after preflight; no iPhone acceptance is claimed.

## Preflight and implementation

Inspected on 2026-10-23 before editing:

- Local checkout was clean on `main` / `origin/main` at `02aad479dfadb710afc9e166d8cb107f93e808eb`, with no stash or other worktree. GitHub listed only `main`; PRs #1, #4, #5 and #6 were merged, with no intervening implementation PR. Historical Phase 01/baseline branch names in archived documents are not live remote branches in this inspection. Created local branch `fix/m0-bookmark-recovery` from that revision.
- Read the live issue body and chronological comments, including the newer bookmark work order. Its older body/runbook build permission does not override the present no-build/no-install instruction.
- Upstream `raw` still points to [`a90b4423`](https://github.com/blinksh/blink/tree/a90b4423c8b7a86770c24a7eaa6c13b0a5904b18), 18.7.0/1097. The manager blob is `baf1ab7111ab9422de6b29f82c570860a2ee8fe7`, identical at October commit [`7a427f3`](https://github.com/blinksh/blink/commit/7a427f3db37ec25869b24226905d89103a8ad99d). Available `main`, `app-store`, `development` and `next` refs did not expose this manager path. The default-branch manager history and bookmark issue search yielded no compatible later repair. This is a bounded search, not proof that no newer source exists anywhere.
- The July 12 entry in [upstream discussion #2247](https://github.com/blinksh/blink/discussions/2247) describes explicit unavailable state and startup retry work. The checked source does not contain that repair. We implement the narrow persistence/reselection fix without importing startup/session changes or upgrading the pin.

The patch keeps the existing `[ { "name", "bookmarkData" } ]` JSON format in `.blink/.locations.json`. Runtime availability and resolved URLs are not serialized. Resolution, scope denial, unreadability, failed stale refresh, and symlink conflicts preserve the saved records and original bookmark bytes. Reads do not create an empty store. Only successful stale refresh, explicit add/reselection, or explicit deletion writes the file, atomically.

Settings retains unavailable entries and offers **Retry** and **Select Folder Again**. Reselection preserves the saved alias name and replaces its bookmark data only after access and persistence succeed. Failed selection leaves the old record; cancellation does not delete it. Already-erased records cannot be recreated from missing bookmark bytes: select the folder through **+** if its saved entry is gone.

Shell URL/path exports include only available entries. The manager serializes its operations and holds one successful security-scope acquisition per available alias for shell use, releasing it on unavailability, deletion, replacement or manager destruction. Repeated reads do not acquire another scope. [Apple requires balancing successful acquisitions with releases](https://developer.apple.com/documentation/foundation/url/stopaccessingsecurityscopedresource()).

Reads create missing aliases but preserve conflicting files, directories and differently targeted symlinks, including dangling links. A mismatched alias is unavailable until the user explicitly reselects. Reselection can rebind a symlink at the saved alias; deletion can unlink it, including when its bookmark cannot resolve. Neither operation follows that symlink to remove folder contents. Regular files/directories at the alias are preserved. Failed add/reselection writes roll back the new link and attempt to restore the old symlink.

The existing manual candidate workflow is prepared to test/apply this patch after the unchanged App Group resolver. Its exact source-file allowlist and patch receipt now cover the resolver, bookmark manager and bookmark settings view. The source pin, signing requests, IDs, App Groups, keychain and migration behavior are unchanged. No workflow has been dispatched. Previously archived IPAs contain none of this bookmark patch.

## Focused checks

Use an isolated, unmodified source directory containing the pinned manager and settings view:

```sh
python3 scripts/test-bookmark-recovery.py /path/to/pinned/blink
```

The runner never edits that input. It checks exact upstream blob hashes, applies the patch to temporary copies and tests rejection of either changed input and of double application without partial edits. Then it compiles the actual patched manager and runs `tests/bookmarks/main.swift` with synthetic bookmark/scope operations and real temporary JSON/files/symlinks. Only BlinkConfig/Objective-C wiring is replaced for the standalone harness. On Linux, `platform.swift` supplies fail-if-used signatures for Apple's unavailable URL APIs; the injected adapter exercises the manager instead. On macOS, the real Foundation adapter compiles, but actual security grants still require an iPhone test.

For patch checks alone, explicitly use `--patch-only`; that mode reports runtime regressions as **NOT RUN**. Missing `swiftc` fails a full test run rather than silently skipping it. The prepared macOS workflow runs the full suite before an app build, if a build is separately approved later.

Regression coverage includes legacy JSON compatibility, repeated read scope balance, resolution failure/reload/recovery, denied and unreadable access, stale refresh success/failure, missing and conflicting aliases, dangling-link recovery, duplicate/unsafe names, failed adds/reselections, atomic-write rollback, explicit deletion with unavailable data, corrupt stores, and a healthy neighbor beside a failed entry. Tests use no private data or installed app storage.

**Local results:** 4 patch application/guard checks and 24 manager regressions passed using a temporary Swift 6.0.3 Linux toolchain in Swift 5 language mode. The patched settings view passed Swift syntax parsing. Workflow YAML, shell blocks and embedded Python parsed; manual trigger, source pin, build and signing steps match the starting workflow. See [the machine-readable receipt](m0-bookmark-recovery.json). Linux results establish manager logic and filesystem behavior; macOS/iOS compilation, SwiftUI type checking/interactions, Apple bookmark/scope semantics, installed entitlements, refresh and native Files.app behavior remain unverified.

## iPhone acceptance, with separate results

Run these as a bounded user device session. First record the actual installed app version/build, artifact/source revision and IPA SHA if known, iOS version, SideStore version and time. If the installed artifact is unestablished, record **Unknown** rather than assigning it an archived SHA. Preserve the earlier successful local file operations, initial bookmark persistence check and `hd-receipts.zip` transfer as historical evidence; later failures do not erase those observations.

Current-app Files.app checks can establish a baseline independently. Patched bookmark acceptance requires a separately approved build and data-safe install route using existing identities, with reviewed private restore capability and migration state. This document authorizes no build, backup, install, refresh, deactivation, reset, ID change or server/network change. Do not replace the working installation to run these instructions without that decision.

| Check | Procedure and pass condition | Result |
| --- | --- | --- |
| Local bookmark persistence | Bookmark a disposable Files folder with a harmless text sentinel. Record its alias and content. Open it through the local Blink shell. Leave/reopen Bookmarks and relaunch Blink from a disposable session: same saved alias and sentinel remain accessible. | Unknown |
| Temporary unavailability | Use an agreed reversible outage for a disposable provider folder. Retry Bookmarks and a local shell command. The entry remains visible as **Unavailable**, never disappears; unrelated entries still work. Relaunch during the outage and confirm the name remains. Do not reset the provider/domain or delete `.locations.json` to simulate an outage. | Unknown |
| Automatic recovery | Restore that folder's availability and tap **Retry**, then retry the shell command. Same alias resolves with original contents. Repeat relaunch. If iOS cannot resolve the old grant, continue with reselection. | Unknown |
| Folder reselection | On the unavailable row choose **Select Folder Again**. Cancel once: name remains saved. Reopen the picker and select the intended folder: same alias works. A regular file/directory occupying the alias must remain untouched and produce a recoverable error. Relaunch and confirm the new grant persists. | Unknown |
| Explicit deletion | Delete only a disposable bookmark, including an unavailable one. Its entry stays removed after relaunch; its symlink alias is removed when possible, and the actual folder/sentinel remains intact. | Unknown |
| Files.app remote browsing | In **iOS Files → Browse → Blink → existing remote location**, open the configured root and at least one child folder. Record actual item names/count or a redacted screenshot and elapsed time. A spinner, provider icon or **Validate Connection** is not a pass. | Unknown |
| Files.app download/read | Through that remote Files location, copy a small uniquely named text fixture to a disposable **On My iPhone** folder. Open it locally and compare exact content/size (hash if available) with the remote source. Record independently from browsing. | Unknown |
| Files.app upload/write | Through Files.app, copy a second unique harmless fixture to an already approved disposable remote folder. Verify content independently through an existing terminal/SFTP route. Rename/move only that fixture if those operations are being accepted; verify each separately. Avoid overwriting existing files. | Unknown |
| Files.app reopening | Close/reopen Files.app, reopen the same remote location and repeat listing plus an uncached fixture download/upload. Repeat after Blink relaunch; distinguish a cached file opening from a working remote connection. Record each result separately. | Unknown |
| Refresh and persistence | In a separately approved SideStore refresh session, capture before/after identity/build and bookmark/Files results. Confirm original host profiles and SSH key identity still work without exposing key material. Recheck both local bookmarks and Files browse/transfers/reopen. | Unknown |

For each row record timestamp, build identity, provider/connection category, expected/observed result and error. A local bookmark pass does not establish remote File Provider success; successful terminal SFTP and **Validate Connection** are separate evidence. If Files fails, retain one short redacted provider-log excerpt around the exact attempt and correlate it with existing server evidence; a `[preauth]` close alone is not proof of a rejected key. Keep raw URLs, bookmark data, keys, provisioning material and private paths out of public reports.

## Unresolved risks and next gate

- The actual trigger of the reported device loss is not established. Preserving records prevents this manager's destructive filtering; it does not restore already-erased data or fix all File Protection/startup races.
- Stale bookmarks whose resolved URL differs from the existing alias require explicit reselection; reads intentionally preserve a differently targeted symlink. A live Apple scope is tested for readability, which may temporarily fail while a provider hydrates its folder.
- Locking covers the singleton's operations within one process, not concurrent external edits to `.locations.json` or its aliases. Avoid manual alias/store edits during recovery. If rollback cannot recreate a symlink because the filesystem is unavailable, the saved record remains, and Retry/reselection can repair the alias later.
- Native SwiftUI compilation, picker cancellation/reselection, actual Apple grants and post-refresh persistence require their own evidence. No release/tag or known-good installed baseline is advanced by these changes.

**Next gate:** review the scoped diff and run the macOS native compile/tests before authorizing any candidate build. Independently reconcile the currently installed artifact and record the three Files.app results: browse, both transfer directions, reopen. M0 and issue #2 remain open until device evidence supports acceptance.

## October 24 combined candidate

Reused and reviewed this pending patch under the new work order. Added reload-after-reselection/deletion and unreadable-store deletion coverage (24 runtime cases total). See [session actions candidate](SESSION-ACTIONS-CANDIDATE.md) for the separate upstream review, foreground adaptation, combined device checklist and build gate. Earlier no-build statements above describe the October 23 session; the new work order authorizes one CI candidate build, never installation or merge. The source pin, App Group resolver, both File Provider extensions and signing identity remain unchanged.
