# Blink-RSK

Reproducible, auditable SideStore builds of [Blink Shell](https://github.com/blinksh/blink), with Raskal Labs command extensions planned on top of Blink's `ios_system` environment.

## Upstream baseline

The App Store currently ships Blink **18.7.1**. As of this repository update, the corresponding 18.7.x source revision is not exposed by a public branch, tag, or GitHub release in `blinksh/blink`, so Blink-RSK does not pretend that it can reproduce that binary.

The newest stable source revision that can currently be pinned and verified from the public upstream repository is:

- Blink **18.6.3**
- build **2009**
- upstream branch `v18.6.0`
- commit `c1b07ea97ac94f2ada190f7d6554f81502774a77`

CI verifies both the commit and the version/build values in the Xcode project before compiling. When upstream publishes the 18.7.1 source, updating this pin is a separate reviewed change.

## Current milestone

**Phase 0: verified upstream sideload baseline.** Build the pinned Blink source on GitHub's macOS runner without an Apple signing identity, package it as an IPA, and let SideStore perform the final signing on-device.

The build intentionally uses:

- `macos-15`
- explicitly selected Xcode **16.4** rather than the runner's moving default
- Blink's documented `get_frameworks.sh` and `get_resources.sh` preparation path
- Blink's documented removal of stale `project.xcworkspace/xcshareddata` before Xcode package resolution
- Release optimization with Blink's `BLINK_PUBLISHING_OPTION_DEVELOPER` feature set
- bundle identifier `io.raskal.blink-rsk`
- no regex or scripted mutation of `project.pbxproj`

### SideStore / App-ID policy

Blink normally embeds File Provider app extensions. SideStore signs each app extension as another App ID, which is undesirable on a free Apple account with a limited weekly App-ID budget. The Phase-0 IPA therefore strips only `.appex` bundles after the unsigned build and keeps the main Blink app and non-extension bundles intact.

Expected result: **one SideStore App ID** for Blink-RSK.

File Provider integration can be restored later as an explicit build variant if it is worth spending the additional App IDs.

## Build

Run **Actions → Build Blink-RSK → Run workflow**.

A successful run uploads:

- `Blink-RSK-18.6.3-2009-unsigned.ipa`
- `SHA256SUMS`
- `build-manifest.json`
- version/build/bundle-ID receipts

A failed run uploads the dependency, package-resolution, build-settings, and `xcodebuild` diagnostics needed to diagnose the actual failing layer.

## Planned command work

Only after the vanilla baseline builds and installs cleanly will command changes begin. Initial candidates are `find`, `sort`, `uniq`, `head`, `tail`, `cut`, `tr`, `tee`, and SHA-256 tooling. Later candidates include `jq`, `sqlite3`, `file`/libmagic, BLAKE3, and a deterministic `rsk-scan` command. Pipeline syntax remains a separate investigation.

## Provenance

The build manifest records the exact Blink commit/version/build, Blink-RSK commit, bundle identifier, Xcode version, iPhoneOS SDK, runner architecture, whether app extensions were stripped, and the expected SideStore App-ID count. The IPA is hashed with SHA-256.

## Licensing

Blink Shell is GPL-3.0. Blink-RSK modifications to Blink-derived code must remain compatible with Blink's license.
