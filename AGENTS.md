# Blink-RSK agent operating boundaries

Read `README.md`, root `ROADMAP.md`, and on `phase/01-upstream-parity` read `docs/PHASE-01.md` and `docs/CODEX-PHASE-01.md`. Product ideas are proposals unless actual iPhone acceptance supports them. Protect the currently installed, working app and its files, keys, SideStore slots and File Provider identity.

- Scoped source edits, documentation, reviews, static inspection and locally isolated tests are permitted by a corresponding work order. Commit only explicitly reviewed paths to the assigned branch; never force-push, implicitly merge, or silently replace a baseline.
- A successful macOS build or structurally valid IPA is not proof of iPhone installation, persistence, Files.app integration or signing/refresh reliability. Keep source, build, installation and device evidence separate.
- Do not initiate a CI signing/build operation, install/replace/deactivate an app, change bundle IDs/App Groups/keychain entitlements, migrate/delete user data, alter network/server configuration, run backups or hardware operations, or deploy production components unless the particular operation is explicitly authorized within a bounded work order. Stop before a consequential decision, even if a previous exploratory document discusses it.
- Never publish tokens, key material, mobile provisioning artifacts or private device data. Preserve untracked research until reviewed; do not use `git add -A` or `git clean`. Do not automatically advance from Phase 01 to product features.
