#!/usr/bin/env python3
"""Apply Shortcuts expansion AFTER session-actions and terminal-input-gestures, offline.

Like the App Group patcher, fail closed if the expected input has changed.
No builds, signing, installations or dependency downloads are performed.
"""
import hashlib
from pathlib import Path
import subprocess
import sys

PATCH = Path(__file__).resolve().parents[1] / "patches/shortcuts-expansion.patch"
EXPECTED_BLOBS = {'Blink.xcodeproj/project.pbxproj': '985d53915aa875b7d28c6ee0e89f698499df7720', 'Blink/SpaceController.swift': '5415b30d4cb27f04e9f65c1641978ba04d0a8612', 'Blink/SessionLink.swift': 'aeb400b355f4ca984ad7094a677db44e708475d1', 'Blink/BlinkIntents.swift': '4859f911680d30663f0d306060af6af4e6a5ff6d', 'SSH/SFTP.swift': 'dd4b03835502f89b0ac8358eb2bbded099bd6fb0'}
NEW_PATHS = ['Blink/ShortcutsRunner.swift', 'Blink/ShortcutsFiles.swift']


def apply(source):
    source = Path(source).resolve()
    for name, expected in EXPECTED_BLOBS.items():
        data = (source / name).read_bytes()
        blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        if blob != expected:
            raise SystemExit(f"{name} changed; refusing an unverified shortcuts-expansion patch")
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
