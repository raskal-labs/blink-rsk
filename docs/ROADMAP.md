# Blink-RSK development roadmap

Status: proposed · 2026-10-10
Repository: raskal-labs/blink-rsk

## Product objective
Maintain a reproducible, SideStore-installable Blink Shell fork with maximum feasible upstream parity, an expanded local Unix command environment, RSK/homelab tooling, and an optional custom UI and contextual T9 command keyboard.

## Operating principles
- Work sequentially through four stages; allow independent research and prototypes without merging unfinished features.
- Preserve upstream behaviour before extending it. Avoid rebuilding features already implemented.
- GitHub Actions builds on macOS/Xcode; Codex develops/audits/tests; iPhone/SideStore is the runtime acceptance authority.
- No claim of compatibility based only on CI success. Preserve the last on-device verified IPA as rollback.
- Keep pinned source/toolchain/patch manifests, hashes, and test receipts.
- Do not require private credentials in CI. Never log secrets.
- For Apple capabilities, distinguish requested entitlements, actual provisioned entitlements, and runtime behaviour.
- Every change is reviewable, independently testable, and preferably reversible.

## Stage 1 — Upstream parity and SideStore reliability (ACTIVE)
### 1A. Establish source baseline
- Check exact source availability for the latest Blink release; request corresponding source from maintainers if necessary.
- Inventory differences from pinned 18.7.0 commit a90b4423c8b7a86770c24a7eaa6c13b0a5904b18 and current release.
- Compare NewsGuyTor modifications with upstream, separating essential sideload fixes from feature removal.
### 1B. Test existing build before rebuilding
- Existing stripped control: Actions 37675286620.
- Existing full File Provider test: Actions 37819898107, artifact Blink-NewsGuyTor-fileprovider-raw-2 (CI success, on-device UNVERIFIED).
- Test SideStore install, launch, restart, SSH, Mosh, local clipboard, OSC 52 remote clipboard, File Provider in Files.app, file access from another app, and key persistence.
- Record SideStore version, iOS version, install errors, actual entitlements and relevant .ips crash logs.
### 1C. Repair only confirmed failures
- Validate main app and both File Provider extensions, bundle IDs, profiles, shared App Group, keychain groups and File Provider document group.
- Reassess migration guards, SideloadFix, and removed capabilities; retain only necessary modifications.
- Test iCloud/CloudKit and other privileged features only where legitimately provisionable. Offer a clearly distinct sync alternative if unavailable.
- Preserve/restore release URL automation without inventing upstream behaviour.
### Stage 1 exit gate
On-device installation and restart stable; SSH/Mosh and copy/paste pass; File Provider tested and either works or is documented as a specific unresolved account/provisioning limitation; no silent data loss; CI provenance and rollback artifact retained.

## Stage 2 — Local Unix environment
- First: find, sort, uniq, head, tail, cut, tr, tee, SHA-256; predictable stdout/stderr and exit statuses.
- Then: jq, sqlite3, file/libmagic, filesystem metadata, BLAKE3 as justified.
- Investigate pipelines and redirection as separate ios_system architectural work; do not promise POSIX parity before testing.
- Add command availability matrix and iOS device-level fixture tests.
### Stage 2 exit gate
Commands work on-device with repeatable fixtures, Unicode paths, large-file limits, cancellation and error handling; no regression to Stage 1.

## Stage 3 — RSK and homelab integration
- Consume canonical host inventory, aliases, user/port/identity and SSH config; avoid hardcoded private addresses.
- Implement safe rsk host, ssh, mosh, ssh-key status/deploy (dry-run, dedupe, explicit target), and device status.
- Implement deterministic rsk scan --jsonl compatible with desktop rsk scan/catalog schema; preserve observation provenance.
- Add offline queue and explicit sync, conflicts/retries and idempotency.
- Add send/fetch, clipboard helpers, Wake-on-LAN where supported, and scoped Shortcuts/App Intents/deep links.
- Keep Polaris/Home Assistant integrations optional and permission-scoped.
### Stage 3 exit gate
A documented set of real homelab workflows succeeds from the iPhone; source of truth remains canonical; destructive or privileged actions require explicit confirmation.

## Stage 4 — RSK UI and contextual T9
- Define theme tokens, typography, restrained colour and compact density; preserve uncluttered terminal mode.
- Improve host/session switcher, connection indicators, command palette and touch controls.
- Prototype the August 2026 Linux Contextual T9 Terminal Engine as an optional in-app input mode, not an iOS-wide keyboard extension.
- Preserve 3x3 T9 grid, Momentum Rail, operator clutch, literal multi-tap, QWERTY escape hatch and ghost completion.
- Prediction sources: available commands, history frecency, flags/help, filesystem paths and canonical RSK host inventory.
- Guard against sending predictions as commands automatically; detect interactive contexts (Vim, TUIs, password prompts) conservatively.
- Benchmark usability against regular keyboard; provide accessibility and hardware-keyboard fallbacks.
### Stage 4 exit gate
Optional UI and T9 can be disabled independently; SSH/Mosh input and interactive apps remain correct; no regression to earlier stages.

## Codex execution pattern
1. Audit and propose smallest testable change.
2. Add tests and receipts before modifying packaging or app behaviour.
3. Implement on isolated branch/PR; no repeated CI builds without a specific hypothesis.
4. Run local/static checks; trigger one pinned GitHub Actions build when warranted.
5. Perform SideStore/iPhone acceptance and attach exact failure evidence.
6. Merge only after passing gate; tag a known-good milestone and retain rollback.

## Immediate next actions
1. Download and install the existing File Provider artifact from run 37819898107 via SideStore.
2. Record install/launch/Files/clipboard results and any .ips crash report.
3. Have Codex audit upstream-versus-IPA features and SideStore signing against those results.
4. Open targeted fixes only for confirmed blockers; avoid new feature work until Stage 1 acceptance.
