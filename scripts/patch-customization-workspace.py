#!/usr/bin/env python3
"""Guarded combined-customization patch; apply after the six accepted repairs.
Offline only. Reject changed inputs/new-path collisions atomically.
"""
import hashlib
from pathlib import Path
import subprocess
import sys
PATCH = Path(__file__).resolve().parents[1] / "patches/customization-workspace.patch"
EXPECTED_BLOBS = {'Blink/SpaceController.swift': '1294e3c7daae861c10c69453968c8eec39206f28', 'Blink.xcodeproj/project.pbxproj': 'ac4bf2e5b69dcd77bc09a1b3709762c6ed35497a', 'Settings/SettingsView.swift': 'd6c846f7c9fb0788562fc0565c409536f6f33cc9', 'Blink/Terminal/LayoutConstraintManager.h': '777fbe8fd87ca9461235bb19959efb747980fbfb', 'Blink/Terminal/LayoutConstraintManager.m': '323dcb179de08e5d8e02432736f7204a30e74500'}
OUTPUT_BLOBS = {'Blink/SpaceController.swift': '119ca88e5e7df58d922652ca3a4fc97805247c8f', 'Blink.xcodeproj/project.pbxproj': 'b0ab334e1841316999c76b5ef1c0b32346c39986', 'Settings/SettingsView.swift': '27e7e29b99c4d2c80ca9d3048979d1a73868158a', 'Blink/Terminal/LayoutConstraintManager.h': '27146f260441e740bfe4907430e4bb8f21bfb681', 'Blink/Terminal/LayoutConstraintManager.m': '9c23c91d00e09efa5d6e86ba88ed51eb0c412c34', 'Blink/WorkbenchUI.swift': '171b917f4055d208b51ccc6885c505818573a4d7', 'Blink/WorkbenchDock.swift': 'fbd703d92197f5b20580661b156d7de38f17d7d3', 'Blink/WorkbenchDPadView.swift': '5bd24eada42986767e6bc608a8cc1e4380201de3'}
NEW_PATHS = ['Blink/WorkbenchUI.swift', 'Blink/WorkbenchDock.swift', 'Blink/WorkbenchDPadView.swift']

def blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
def apply(source):
    source = Path(source).resolve()
    for name, expected in EXPECTED_BLOBS.items():
        if blob((source / name).read_bytes()) != expected:
            raise SystemExit(f"{name} changed; refusing unverified customization-workspace patch")
    for name in NEW_PATHS:
        target = source / name
        if target.exists() or target.is_symlink():
            raise SystemExit(f"{name} exists; refusing to replace intervening work")
    command = ["git", "apply", "--whitespace=error", str(PATCH)]
    subprocess.run(command[:2] + ["--check"] + command[2:], cwd=source, check=True)
    subprocess.run(command, cwd=source, check=True)
if __name__ == "__main__": apply(sys.argv[1])
