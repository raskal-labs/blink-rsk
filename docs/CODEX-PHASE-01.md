# Blink-rsk — Phase 01 Codex execution roadmap

Status: **Proposed** · updated 2026-10-12
Owner: Codex (implementation), user (iPhone-only verification)
Branch: `phase/01-upstream-parity`
Tracker: [issue #2](https://github.com/raskal-labs/blink-rsk/issues/2)
Background: [PHASE-01.md](PHASE-01.md)

## Outcome

Produce the **smallest maintainable Blink 18.7.0-based SideStore IPA** that preserves upstream functionality, runs on iPhone 16 / iOS 27, and lets iOS Files browse and transfer files over SFTP. Do not mistake successful CI, installation, normal SSH/SFTP, or Blink's Files.app **Validate Connection** for successful Files.app directory enumeration.

**Minimal-interaction contract:** Codex completes read-only inspections, source patches, tests, documentation and at most **one justified CI IPA build** autonomously. Batch results. Ask the user only when an installed app, signing account, existing data, or iPhone interaction must change; then provide one short decision with implications. Never claim to have installed or verified the app on-device without user results. No continuous polling or background action unless explicitly supported by the execution environment.

## Efficiency, SideStore limits, and external-first debugging (mandatory)

- **Conserve usage:** Reuse the archived IPAs, previous reports, source diffs, logs, and CI results before any new download, query, test, or build. Prefer targeted searches, bounded logs, small source reads, local static checks and batched tool calls. Never repeatedly fetch, scan, build or poll the same unchanged result. Spend CI/macOS minutes only on a candidate that passed the safety/signing preflight. Keep evidence concise rather than accumulating long duplicate reports.
- **SideStore ID/slot budget:** Free-account registrations are limited (typically **10 App IDs per rolling 7-day period**) separately from the **3 active-app limit** and 7-day certificate/provisioning validity. App extensions can consume separate IDs. The device last showed **4 App IDs remaining** and **3 active native apps**; its registered list included the FP Test main app plus two extension IDs. These numbers are a **time-stamped snapshot**, not perpetual capacity. Re-check the live SideStore counters before installing, refreshing, or registering anything; don't infer free native slots from remaining IDs or vice versa.
- **Keep existing identities:** Prefer updating the existing FP Test's main + two extension identities with the same signing account only **after** an explicit data-safety decision. Avoid renaming, randomizing, installing side-by-side test apps, consuming fresh IDs, or deactivating installed apps merely for convenience. An in-place update still needs backup/rollback approval. If no safe slot or compatible provisioned App Group/keychain is available, **stop and report the narrow blocker**; do not burn IDs by trial and error.
- **Research before diagnostics:** If stuck or after **one or two unsuccessful attempts** at a hypothesis, **search the web for comparable successes and failures before building a bespoke diagnostic suite**: first exact Blink and SideStore versions, then SideSign/AltStore, File Provider and iOS signing cases, then Apple Developer Forums and upstream code/issue threads. Look for actual resolved reports, reproduction conditions, and what fixed them; separate confirmed outcomes from speculation. Report 2–4 relevant links and a compact applicability verdict, not a sprawling literature review.
- **Smallest next test:** Prefer a known workaround, a read-only entitlement/profile inspection, or a one-line targeted log/error check before instrumentation. A custom diagnostic utility or test harness is a **last resort**, justified only when external fixes and existing evidence cannot distinguish plausible causes. Never weaken protections or spoof entitlement grants to make a build appear successful.

## Baselines (already Verified)

- Public upstream source `blinksh/blink@a90b4423c8b7a86770c24a7eaa6c13b0a5904b18`, Blink 18.7.0 (1097). Do not treat App Store 18.7.1 as the same source.
- Clean, unmodified upstream IPA: `/lab/blink-rsk-release/upstream-control-20261002/Blink-upstream-18.7.0-1097-unsigned.ipa`; SHA-256 `98b4a1f074fb922c4633a0df59f7a4f98ed8b435a9998d4b6158c4363d1c0521`. Original Actions run [36983463594](https://github.com/raskal-labs/blink-rsk/actions/runs/36983463594).
- Known installable *but Files.app-broken* FP Test: `/lab/blink-rsk-release/fp-test-20261008/Blink-NewsGuyTor-18.7.0-1097-fileprovider.ipa`; SHA-256 `d3e2f5afc124576d86014bf6c38803e66ddc41009e26bc98c2c80b4f3a44ba1e`. [Pre-release](https://github.com/raskal-labs/blink-rsk/releases/tag/v18.7.0-rsk.0-fp-test). Preserve this rollback artifact.
- FP Test on iPhone: `ssh gamecube`, SFTP upload and Files.app *Validate Connection* succeed. iOS Files stays on **Loading**. Extension logs show `itemFor NSFileProviderRootContainerItemIdentifier : Requested`; contemporaneous GameCube sshd sessions close at `[preauth]` (not proof of bad key). No successful root-item stat/enumeration captured.
- Both IPAs contain main app, File Provider and File Provider UI, with identical 3 bundle IDs and literal `NSExtensionFileProviderDocumentGroup=group.sh.blink`. Clean IPA has no embedded signatures/profiles; FP Test has ad-hoc requested-entitlement signatures; FP Test's recorded FP and main requested entitlements omit upstream's explicit shared `keychain-access-groups`.
- SideStore already registered IDs for main + 2 extensions; native active app slots were full when last checked. In-app registered IDs or original bundle IDs are **not proof** of actual provisioned App Group/keychain grants. SideStore version observed: 0.7.0-20260918.492+12a496ca.
- Upstream `Migrator.swift` checks `.migrator` version in shared storage; its 1400/1810/1860/1870 steps respectively handle config migration, old File Provider storage cleanup, style settings conversion, and suspended-session registry cleanup. Existing installed migration state **Unknown**. FP Test disables migration; don't restore blindly.

## Roadmap and task list

### 0. Freeze & quick inventory — no rebuild
- [x] Preserve and hash both already-built IPAs.
- [x] Record actual iPhone symptom, logs and GameCube-side SSH evidence (above; full evidence in issue #2).
- [ ] Confirm the working branch is clean, latest repo state and current build-workflow inputs; don't force-push or rewrite history.
- [ ] Identify which capabilities must be granted to the main app, FP extension and FP UI, and how the installed SideStore version signs each. Use its actual release/source, not just a newer SideSign implementation. Check SideStore's current App ID and active-slot budget before proposing an install.
- [ ] Write one **compact matrix** of bundle ID, requested entitlements, provisioned/effective entitlements (mark **Unknown** where not measurable), App Group, keychain group, FP document group. No elaborate signing framework.
- [ ] Compare upstream vs FP Test source patches; identify confirmed necessary, harmful and irrelevant changes. Only inspect files that affect current blocker.

**Gate:** A plausible, precisely stated blocker and smallest candidate change. If free provisioning cannot supply a required capability, stop and document it rather than fake it.

### 1. Prepare a safe candidate
- [ ] Check what important data is accessible for backup: `.ssh` private identities, host config, Files locations, local files and `.migrator`. Preserve privately and verify checksums/restore feasibility. **Never put credentials or private keys into Git, issues, build logs or public artifacts.**
- [ ] Document anything on the iPhone that cannot be backed up from available tools. If an in-place install may destroy inaccessible data, **Blocked pending user decision**; do not assume a rollback IPA also restores data.
- [ ] Derive candidate from pinned upstream, preserving both app extensions and upstream File Provider logic. Change only necessary signing preparation and migration safety controls; do not blanket-remove entire subsystems.
- [ ] Ensure consistent, legitimately provisioned App Group and keychain access between main app and FP; reconcile extension document-group value with reality. Source configuration and requested entitlements are not evidence of effective installed entitlements.
- [ ] Before writing new diagnostics, check comparable **resolved** external reports and try the cheapest discriminating check. Add only small static assertions or targeted logs where existing tests cannot discriminate; no generalized diagnostic suite or product refactor.

**Gate:** Reviewable source diff, explicit migration policy, safety/backup receipt, extension+entitlement matrix and clear hypothesis. If no safe test path, report **Blocked** with one specific decision for user.

### 2. Build once, package and hand off
- [ ] Reuse existing CI workflow where possible. Run its fast validation/build-setting checks before any IPA build; fail early on missing extensions, wrong IDs, FP document-group mismatch, unexpected patches, or requested-entitlement differences.
- [ ] Trigger **one** documented, pinned GitHub Actions IPA build once gate 1 is satisfied. Do not start speculative build loops.
- [ ] Inspect artifact ZIP, extension presence, signatures/entitlements as far as possible, version/IDs and SHA-256. Preserve a release candidate on GameCube separately from existing artifacts; attach manifest and concise limitations.
- [ ] Produce an install handoff: artifact URL, hash, app IDs expected, whether SideStore will update FP Test in place, data risk, and a *short* 2-minute test procedure. **Do not uninstall, deactivate, overwrite an existing native app, consume new IDs, or change the signing account without specific user authorization.**

**Gate:** Candidate verified structurally and approved for the selected on-device installation route. CI success != functional success.

### 3. One user test, one evidence-based follow-up
- [ ] User installs/signs natively in SideStore and supplies short results (not required to troubleshoot via LiveContainer).
- [ ] Test in order: launch/restart → saved SSH key & host → SFTP → Files.app Validate Connection → Files.app **actual listing** of `/tmp` → download/open → upload/rename/delete *disposable* file → relaunch Files.app and re-check.
- [ ] If Files.app fails, correlate one FP log excerpt and GameCube sshd timestamps; identify which of shared storage, keychain/SSH, root stat, or enumeration failed. Don't repeatedly ask for logs already supplied.
- [ ] If stuck or after one/two failed attempts, **search resolved external cases before making diagnostic tooling**. Pick **one** smallest correction or known workaround; record result before another build. A second build requires new evidence and a fresh justification.
- [ ] If it passes, verify data persistence and refresh/restart, tag a new verified release, and record artifact/hash. Keep UX enhancements from [issue #3](https://github.com/raskal-labs/blink-rsk/issues/3) deferred.

## Decision points / stop rules

- **Codex may proceed without asking:** read files, diff source, inspect IPAs and CI, create isolated changes/tests, write docs/issue updates, build one justified IPA, and save non-secret artifacts. Keep changes on the Phase 01 branch (or a short-lived child branch); do not force-push or merge to `main` before iPhone acceptance.
- **Ask user once, only when needed:** required access or backup is unavailable; replacing/deactivating an installed app or changing identifiers is necessary; in-place upgrade could lose unsaved keys/data; ready for iPhone install/test.
- **Stop:** no legitimate provisioning solution, unresolved data-loss risk, CI artifact missing required extension, or a test failure with no discriminating evidence. Do not silently fall back to stripped File Provider or private storage.
- **No scope creep / no wasted usage:** no shell UX improvements, RSK commands, Mosh overhaul, UI changes, new automation, migration framework, speculative diagnostic suite, unnecessary CI runs or fresh App IDs until Files.app is verified.

## Codex deliverable format

Post one concise checkpoint in issue #2 containing: **status** (Proposed / In Progress / Verified / Blocked / Unknown), hypothesis, changed files, checks executed and results, artifact URL/hash if built, unresolved limitations, exactly one next action. Label untested hypotheses as such. If ready for device testing, provide only the minimal action for the user and the criteria for reporting pass/fail.

**Success is not “it built” or “Files.app showed Blink”. Success is a native, maintainable SideStore build with working Files.app browse and transfers plus preserved user configuration.**
