# Blink-RSK

Reproducible, auditable SideStore builds of [Blink Shell](https://github.com/blinksh/blink), with Raskal Labs command extensions planned on top of Blink's `ios_system` environment.

## Upstream source target

The App Store currently ships Blink **18.7.1**, but that exact release source is not exposed by a public upstream branch/tag that can be pinned reproducibly.

The newest public **18.7** source currently exposed by `blinksh/blink` is the upstream default branch `raw` at:

- source version: **18.7.0**
- branch at selection: `raw`
- commit: `a90b4423c8b7a86770c24a7eaa6c13b0a5904b18`

The workflow pins that commit rather than following the moving branch. It verifies that the source declares Blink 18.7.0 before compiling. This is not claimed to reproduce the App Store 18.7.1 binary.

## Current milestone

**Phase 0: complete upstream sideload control.** Before making Blink-RSK source changes, build the complete upstream application as faithfully as possible and determine whether SideStore can install and launch it.

The control build intentionally uses:

- `macos-26`
- explicitly selected Xcode **26.6**
- the exact pinned upstream commit above
- recursive upstream submodules
- upstream `get_frameworks.sh` and `get_resources.sh`
- upstream's documented removal of `Blink.xcodeproj/project.xcworkspace/xcshareddata/`
- an unchanged copy of `template_setup.xcconfig` as `developer_setup.xcconfig`
- Release configuration with upstream's own Release publishing condition
- upstream bundle identifiers before SideStore re-signing
- no Blink-RSK xcconfig overrides
- no Blink source patches
- no scripted mutation of `project.pbxproj`

### Complete application policy

The IPA preserves Blink's embedded File Provider app extensions. It removes only stale code-signature directories and embedded provisioning profiles from the unsigned build product before packaging.

This is deliberate: the first test is whether a complete upstream Blink application can be re-signed by current SideStore. App-ID/capability optimization comes later, after a working control has been demonstrated.

The workflow records the main bundle identifier and every embedded `.appex` bundle identifier so the exact package presented to SideStore is auditable.

## Build

Run **Actions → Build upstream Blink baseline → Run workflow**.

A successful run uploads:

- `Blink-upstream-18.7.0-<build>-unsigned.ipa`
- `SHA256SUMS`
- `build-manifest.json`
- main bundle-ID receipt
- version/build receipts
- extension count
- embedded bundle-ID inventory

A failed run uploads dependency, package-resolution, build-settings, and `xcodebuild` diagnostics.

## Blink-RSK modifications

`config/blink-rsk.xcconfig` is retained for future RSK work but is **not applied by the Phase-0 control workflow**.

Only after the complete upstream control installs and launches cleanly do RSK changes begin. Initial command candidates include `find`, `sort`, `uniq`, `head`, `tail`, `cut`, `tr`, `tee`, and SHA-256 tooling. Later candidates include `jq`, `sqlite3`, `file`/libmagic, BLAKE3, and a deterministic `rsk-scan` command.

## Provenance

The build manifest records the exact upstream commit/version/build, Blink-RSK harness commit, original upstream bundle ID, Xcode version, iPhoneOS SDK, runner architecture, extension count, and packaging policy. The IPA is hashed with SHA-256.

A CI-successful artifact is not considered the known-good baseline until the packaged IPA has also been installed and launched successfully through SideStore.

## Licensing

Blink Shell is GPL-3.0. Blink-RSK modifications to Blink-derived code must remain compatible with Blink's license.
