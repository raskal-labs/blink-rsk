#!/usr/bin/env python3
"""Apply the M0 bookmark repair to the exact pinned Blink source, offline.

Like the App Group patcher, fail closed if the expected input has changed.
No builds, signing, installations or dependency downloads are performed.
"""
import hashlib
from pathlib import Path
import subprocess
import sys

PATCH = Path(__file__).resolve().parents[1] / "patches/bookmark-recovery.patch"
EXPECTED_BLOBS = {
    "Settings/Model/BookmarkedLocationsManager.swift": "baf1ab7111ab9422de6b29f82c570860a2ee8fe7",
    "Settings/ViewControllers/BookmarkedLocations/BookmarkedLocationsView.swift": "55a38b6cf1df21b722121f19b35beb062943d3b4",
}


def apply(source):
    source = Path(source).resolve()
    for name, expected in EXPECTED_BLOBS.items():
        data = (source / name).read_bytes()
        blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        if blob != expected:
            raise SystemExit(f"{name} changed; refusing an unverified bookmark patch")
    # Check every hunk before changing either file. git apply also works in an
    # isolated directory without a .git checkout; no index or refs are changed.
    command = ["git", "apply", "--whitespace=error", str(PATCH)]
    subprocess.run(command[:2] + ["--check"] + command[2:], cwd=source, check=True)
    subprocess.run(command, cwd=source, check=True)


if __name__ == "__main__":
    apply(sys.argv[1])
