#!/usr/bin/env python3
"""Apply the session links/Shortcuts adaptation to the exact pinned Blink source, offline.

Like the App Group patcher, fail closed if the expected input has changed.
No builds, signing, installations or dependency downloads are performed.
"""
import hashlib
from pathlib import Path
import subprocess
import sys

PATCH = Path(__file__).resolve().parents[1] / "patches/session-actions.patch"
EXPECTED_BLOBS = {'Blink.xcodeproj/project.pbxproj': '1d418119be3f1df3cec877df591763c4d2405a04', 'Blink/SceneDelegate.swift': '8a59f85fbadfaf8c4d7befb22b0995575fbdc09e', 'Blink/SpaceController.swift': '750cb04d82ceb85c2d80a6e1992e47ef3af21b5c'}
NEW_PATHS = ['Blink/SessionLink.swift', 'Blink/BlinkIntents.swift']


def apply(source):
    source = Path(source).resolve()
    for name, expected in EXPECTED_BLOBS.items():
        data = (source / name).read_bytes()
        blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        if blob != expected:
            raise SystemExit(f"{name} changed; refusing an unverified session-actions patch")
    for name in NEW_PATHS:
        path = source / name
        if path.exists() or path.is_symlink():
            raise SystemExit(f"{name} exists; refusing to replace intervening work")
    # Check every hunk before changing either file. git apply also works in an
    # isolated directory without a .git checkout; no index or refs are changed.
    command = ["git", "apply", "--whitespace=error", str(PATCH)]
    subprocess.run(command[:2] + ["--check"] + command[2:], cwd=source, check=True)
    subprocess.run(command, cwd=source, check=True)


if __name__ == "__main__":
    apply(sys.argv[1])
