# Blink-RSK

Reproducible, auditable sideload builds of [Blink Shell](https://github.com/blinksh/blink), with Raskal Labs extensions planned on top of the upstream `ios_system` command environment.

## Status

**Phase 0: bootstrap.** The first milestone intentionally builds an unmodified GPL Blink baseline as an unsigned IPA on a GitHub-hosted macOS runner. Once that succeeds, additional commands will be introduced atomically so build failures can be attributed to a specific change.

### Planned command work

Initial candidates: `find`, `sort`, `uniq`, `head`, `tail`, `cut`, `tr`, `tee`, and SHA-256 tooling. Later candidates include `jq`, `sqlite3`, `file`/libmagic, BLAKE3, and a deterministic `rsk-scan` command. Pipeline syntax is a separate investigation.

## Build

Run **Actions → Build Blink-RSK → Run workflow**. The workflow currently defaults to the builder's known-good Blink `v18.4.2` baseline; the Blink version is an input so newer upstream revisions can be tested without rewriting CI.

The artifact contains the unsigned IPA plus provenance files. SideStore performs device-side signing/install.

## Provenance

The bootstrap uses the open-source [Blink-Shell-GPL-Builder](https://github.com/NewsGuyTor/Blink-Shell-GPL-Builder) at a pinned commit. CI records the Blink version, builder revision, Blink-RSK revision, macOS/Xcode information, and SHA-256 hashes of produced IPA files.

## Licensing

Blink Shell is GPL-3.0. Blink-RSK modifications to Blink-derived code must remain compatible with Blink's license. Build/automation material original to this repository will be licensed explicitly as it is added.
