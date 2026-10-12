# Phase 01 — Upstream parity and SideStore reliability

**Current Codex execution roadmap/task checklist:** [CODEX-PHASE-01.md](CODEX-PHASE-01.md) · [GitHub issue #2](https://github.com/raskal-labs/blink-rsk/issues/2). The older exploratory notes below are historical context; use the newer runbook for task order and current verified device evidence.

Started: 2026-10-11
Working branch: `phase/01-upstream-parity`
Base: `main` at `facc9a166df7e5db88840c3bb634172084ba16cf`
Baseline release: [v18.7.0-rsk.0-fp-test](https://github.com/raskal-labs/blink-rsk/releases/tag/v18.7.0-rsk.0-fp-test)
Baseline CI run: [37819898107](https://github.com/raskal-labs/blink-rsk/actions/runs/37819898107)
Baseline source: `ef0ed16770912d6e5ca5510449dfc34fb798e9c8`
Baseline IPA SHA-256: `d3e2f5afc124576d86014bf6c38803e66ddc41009e26bc98c2c80b4f3a44ba1e`
Local preserved copy: `/lab/blink-rsk-release/fp-test-20261008/` on GameCube

## Verified / unverified
- CI built the baseline successfully; the IPA was downloaded and hash-checked.
- User observed `Blink FP Test` appearing as a location in Files.app on iPhone 16 / iOS 27.
- Files.app displayed `LOADING`; successful enumeration, transfer, shared storage, SSH/Mosh, clipboard, key persistence and restart are **not yet verified**.
- The baseline predates the App Group resolver fix merged in `8c43219d1` / `8fd4248d6`; do not attribute that fix to the released IPA.
- Release is intentionally a pre-release, not a stable release.

## Branch reconciliation
- `main`: authoritative integration branch.
- `phase/01-upstream-parity`: active investigation and fixes, branched from main.
- `archive/third-party-builder`: historical reference, behind main with zero unique commits.
- `baseline/vanilla-18.6.3`: historical reference, behind main with zero unique commits.
- `build/direct-upstream`: historical reference, behind main with zero unique commits.
- No merge or force-push needed; do not delete historical references.

## First investigation — identify effective signing/storage constraints
1. **Device evidence**: Capture whether Files.app exits LOADING, the Blink terminal launches, restart behaviour, SideStore version, SSH/Mosh, copy/paste, key persistence, and any install/crash logs.
2. **Entitlement map**: Build a per-target table for main app, File Provider and File Provider UI: bundle ID, provisioning profile, requested entitlements, effective entitlements, keychain groups, shared App Groups, `NSExtensionFileProviderDocumentGroup`.
3. **Static issue to investigate**: The IPA packaging checks that the extension plist document group is `group.sh.blink` *before* SideStore signing; the runtime `XCConfig.infoPlistFullGroupID` patch can resolve a different provisioned group. Determine whether SideStore also rewrites the extension plist; otherwise these can diverge.
4. **Static issue to investigate**: `BlinkPaths.groupContainerPath` and `UserDefaults.suite` rely on the App Group. Test what happens when `containerURLForSecurityApplicationGroupIdentifier` returns nil or the suite cannot initialize; avoid silently creating isolated substitute storage.
5. **Static issue to investigate**: Compare the upstream File Provider keychain-access-group entitlements with the experimental signing manifest, which does not explicitly request them for the extension.
6. **Static issue to investigate**: NewsGuyTor disables the migration entry point; inventory every migration and identify any upgrade/data-loss implications before selectively re-enabling.
7. **Reproduction harness**: Prefer a minimal diagnostic app/extension and deterministic tests before a full Xcode rebuild. No entitlement spoofing; use actual Apple provisioning grants.
8. **External evidence**: Search confirmed successes and failures in SideStore, AltStore, Blink, iOS File Provider and Apple Developer Forums. Repeat targeted research after one or two failed attempts.

## Experiment policy
- One hypothesis and one variable per experiment.
- Prioritize low-cost, high-information tests, then reversible repairs, then alternate signing, then feature alternatives.
- Record exact commands, error signatures, input conditions, artifacts, results and external references.
- Preserve a working IPA and known-good data before attempting a migration or bundle identity change.
- No automatic CI build until device evidence or a clear static defect justifies it.

## Acceptance gate
- On-device install, launch and restart stable.
- SSH/Mosh, local and OSC 52 clipboard, key creation/restart and Files.app enumeration tested.
- File Provider read/write verified **or** limitation specifically characterized with a documented fallback.
- Data persistence and migration behaviour verified.
- Reproducible build manifest and rollback release retained.
