# Combined Shortcuts candidate — October 27, 2026

**In Progress.** Supersedes the October 26 build deferral: the user authorizes one additional candidate CI dispatch after implementation/preflight. No install, replacement, provider reset, signing change or merge is authorized. PR #7 stays draft. The October 24 artifact/receipts remain historical, unchanged and available for rollback.

Current device evidence: existing host/session links and all three original Shortcuts actions work by user report. Bookmark persistence has positive feedback; broader failure/recovery and refresh acceptance remains In Progress. The user withdrew the October 26 Files sync failure as mistaken. That report is superseded, is not an active blocker, and supplies no successful transfer test.

## Reconciliation and provenance

Inspected AGENTS.md, all local/remote branches and worktrees, live PR #7/issue #2, the canonical roadmap/product direction, pinned source and archived October 24 receipts. Continued the existing `fix/bookmarks-session-actions` branch; no competing implementation branch was found. Preserved the existing uncommitted UX research and bookmark checkpoint edits. Retained the pin `a90b4423c8b7a86770c24a7eaa6c13b0a5904b18`, original bookmark repair, App Group resolver, navigation-only links and queued exact `7e28d172` provider startup-cleanup backport.

Read upstream `7a427f3db37ec25869b24226905d89103a8ad99d`'s `Blink/Fleet/HeadlessSSHRunner.swift`, `FleetIntents.swift`, general Intents and FleetCore ExitTrailer before adaptation. Reuse SSHClient dial/exec and dedicated run-loop architecture, saved/default signers and linked agent. Reject upstream's default unknown-key acceptance, unlimited read accumulation and background/Fleet promises. Strict known-host verification precedes authentication for result/transfer actions. Existing InputPrompter, stored password and foreground interactive challenges remain supported. ProxyJump/ProxyCommand profiles still use the existing SSH framework; profiles needing a terminal-specific proxy helper may fail visibly and need the terminal instead.

Separately guarded `terminal-input-gestures.patch` contains only the two Snips resign lines from upstream `9e8767b75` and the detach replacement from madjinn `a31aa977`. `shortcuts-expansion.patch` then extends five existing files and adds two main-app Swift sources. Combined six-patch allowlist: 13 source paths. No new extension, identity, entitlement or migration change.

## Delivered source behavior

| Action | Result and boundary |
| --- | --- |
| Open Terminal Session | SSH/Mosh, optional starting command and explicit reuse toggle. Returns a navigation receipt. Names without commands reuse by default in the current window; name alone focuses. A starting command always creates a new session and remaps the name, without injecting into the old session. Command requires a host; local shell opening remains available. |
| Focus Session | Explicitly focus an existing named session in the current window; missing/closed names fail. Returns a receipt. Names are in memory until app/session closure. |
| Run Command / Run Script on Host | Foreground confirmation, then no-PTY SSH result capture. Return JSON `host`, `stdout`, `stderr`, `exitCode`; use **Get Dictionary from Input** and **Get Dictionary Value → stdout** next. Nonzero status throws with status and up to 4,096 characters of diagnostic output. Unknown/missing status fails. Scripts use the existing base64/interpreter approach with decode-error propagation; host needs `base64 --decode` and the chosen interpreter. |
| Upload File | One IntentFile from a shortcut/share-sheet shortcut; optional filename, explicit remote directory. Returns JSON host/directory/filename/bytes/status. Existing file/symlink destinations fail atomically through `O_EXCL`; no silent replacement. Zero-byte input is valid. |
| Download File | One regular remote file returns an IntentFile with its filename; next use Save File or Share. No local destination is chosen or overwritten by Blink. Size checked before and during transfer. |
| List Remote Directory | JSON host/path/entries with name/type/size; sorted names and bounded enumeration. No shell parsing of remote filenames. |
| Open Saved Folder | Saved bookmark entity picker includes unavailable entries. Revalidate through the existing bookmark manager; unavailable entries fail with Retry/reselection guidance and remain saved. Open an available URL with quoted `cd` in a fresh local terminal, retaining the manager's balanced access scope. |

All eight actions open Blink and require the foreground app. Execution/transfer actions confirm the saved target and operation. Result/SFTP connections reject unknown or changed keys; establish trust independently through Blink's existing interactive terminal first. External links stay navigation-only and reject all command, script, key and new transport parameters. Cold/warm routing and per-window naming reuse the existing scene path. Shortcuts do not promise unattended/background completion on iOS.

Bounds: 60-second action deadline, 256 KiB per command output channel, 16 MiB per file and 2,000 directory entries/256 KiB listing JSON. Relative remote paths start at account home; `~` and `~/` are supported. Reject control characters and invalid/overlong filenames/paths. Upload input is read under coordinated/security-scoped access following [Apple's IntentFile contract](https://developer.apple.com/documentation/appintents/intentfile/fileurl); only acquired scopes are released. File input is never removed. Cancellation/deadline resolves once even before worker setup; Combine cleanup runs on the SSH owning thread. Existing synchronous libssh SFTP calls can delay resource cleanup. Cancellation, timeout, overflow or a transport failure can leave remote work or a partial upload: inspect the destination and choose an unused name before retrying. No remote rollback/delete is attempted.

**Concrete platform limitation:** no supported standalone Files-app bookmark navigation exists in the inspected source. This batch exposes terminal opening only, rather than claim an arbitrary saved security-scoped URL can navigate Files. Native Files provider browse/transfer tests and downloaded-file Save/Share remain separate supported workflows.

Provider backport disables only automatic startup temporary-file cleanup; polling, replica state and existing domains remain intact. Abandoned temporary files may remain. It is not described as repairing the withdrawn sync report.

## Validation and candidate receipts

Local preflight: all six patches compose on pristine pinned inputs with exactly 13 reviewed source paths; all 24 bookmark manager regressions, existing link/action and seven SSH shell-boundary fixtures, exact provider parity/guards/syntax, terminal correction parity/guards/attachment/dismiss contracts, expansion atomic guards, eight real exit/stdio fixtures, Mosh shell boundary, path/name validation and 80 continuation races pass. Workflow YAML, shell blocks, embedded Python, harness Python and applied-source whitespace pass. Linux checks do not type-check Apple frameworks or establish real transfers/authentication/UI behavior.

Native resolver checks, macOS Swift regressions, full iOS Release compilation, App Intents metadata and packaging are pending the single authorized CI dispatch. Machine-readable checkpoint: [shortcuts-expansion.json](shortcuts-expansion.json). Do not relabel old receipts as this build.

## One combined device checklist

Run only after a separately authorized, data-safe installation route. This checklist does not authorize replacement, resets or refresh.

1. Record the actual candidate source, IPA SHA, device/iOS and installed artifact identity; retain old IPA/rollback references. Verify original keys, hosts, local files, both provider extensions, normal SSH/Mosh and existing Files locations survive.
2. Recheck existing host/focus links and all three original actions on cold and warm launches. Reject links carrying command/script/key/Mosh parameters. Cancel confirmation; no connection/command starts. Retest missing host and closed session names.
3. Chain command JSON through Get Dictionary → stdout, including empty output, quotes/literal `$()`/semicolons, separate stderr and nonzero `exit 7`. Run multiline sh/bash/python3 fixtures; a missing interpreter/decoder must fail clearly. Verify timeout, >256 KiB output and cancellation. Independently check unknown/changed-key rejection without accepting a mismatch.
4. List a disposable SFTP directory including spaces/Unicode/quotes in names. Upload one small file from Shortcuts and a share-sheet shortcut; check bytes/content remotely. Retry the same name and a pre-existing symlink: neither target changes. Try an unavailable input/provider, invalid filename and >16 MiB file. Cancel a transfer; inspect any partial before retrying under another name.
5. Download a disposable file, inspect filename/content, then Save File or Share. Test zero-byte, missing, directory, permission-denied and oversize input. Record actual native Files browse/upload/download/reopen separately; the withdrawn banner report is not a required failure reproduction or reset task.
6. Open SSH and existing Mosh on a known host, with/without a starting command. A named no-command request reuses; reuse off creates new. A starting command with a name already used by an unrelated session creates a fresh session; old session receives no input. Focus named sessions; test closed names, another window, cold and warm launches. No complete Mosh scrollback/history or mouse behavior is claimed.
7. Open an available saved folder in a fresh local terminal; verify cwd and disposable contents. Check persistence across relaunch. An unavailable bookmark stays listed and stored; Retry/reselection/cancel behave correctly without removing neighbors. Positive persistence feedback remains valid; broader recovery/refresh acceptance still requires results.
8. In local, SSH and Mosh sessions, open both Snips paths (normal and Scratch) with modifiers active; close/cancel/use a Snip and confirm terminal input/modifiers restore. Switch sessions and reattach views repeatedly; normal gestures still attach, detached views do not retain recognizers. Check keyboard-hidden and hardware/software keyboard cases. These checks do not prove a fix for historical scrolling freezes.

Next agreed milestone: combined customization across touch controls, terminal usability, workspace UI and appearance. Retain existing research. Select All/Copy All, optional D-pad, keyboard lock, large paste, renderer/backpressure and Mosh mouse/scrollback experiments are excluded here; local retained-buffer copying and remote multiplexer history remain distinct.
