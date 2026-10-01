# Blink-RSK

Reproducible, auditable sideload builds of [Blink Shell](https://github.com/blinksh/blink), with Raskal Labs extensions planned on top of the upstream `ios_system` command environment.

## Status

**Phase 0: verified upstream baseline.** The first milestone builds an unmodified GPL Blink baseline as an unsigned IPA on a GitHub-hosted macOS runner. Once that succeeds, additional commands will be introduced atomically so build failures can be attributed to a specific change.

The initial baseline is Blink **18.4.2 build 1051**, upstream commit `99660bf1b9f9c8b5580720b7b22a94c4daec4cb7`. Upstream exposes `v18.4.2` as a branch pointing to that commit; it is not treated as a Git tag by this repository.

### Planned command work

Initial candidates: `find`, `sort`, `uniq`, `head`, `tail`, `cut`, `tr`, `tee`, and SHA-256 tooling. Later candidates include `jq`, `sqlite3`, `file`/libmagic, BLAKE3, and a deterministic `rsk-scan` command. Pipeline syntax is a separate investigation.

## Build

Run **Actions → Build Blink-RSK baseline → Run workflow**. The default input is the verified upstream Blink 18.4.2 commit SHA. The workflow also accepts an explicit upstream branch name or full 40-character commit SHA.

The workflow follows Blink's upstream preparation path (`get_frameworks.sh`, `get_resources.sh`, `template_setup.xcconfig`) and performs an unsigned Release device build with `xcodebuild`. It does not regex-edit Blink's Xcode project. The resulting `.app` is packaged as an unsigned IPA for SideStore to re-sign/install on-device.

## Provenance

CI records the requested Blink ref, resolved Blink commit, Blink-RSK revision, macOS/Xcode/iPhoneOS SDK information, and SHA-256 hash of the produced IPA. The third-party GPL-builder experiment used during bootstrap is retained only in repository history/archive and is not part of the current baseline build path.

## Licensing

Blink Shell is GPL-3.0. Blink-RSK modifications to Blink-derived code must remain compatible with Blink's license. Build/automation material original to this repository will be licensed explicitly as it is added.
