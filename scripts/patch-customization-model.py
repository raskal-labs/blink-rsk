#!/usr/bin/env python3
"""Guarded combined-customization patch; apply after the six accepted repairs.
Offline only. Reject changed inputs/new-path collisions atomically.
"""
import hashlib
from pathlib import Path
import subprocess
import sys
PATCH = Path(__file__).resolve().parents[1] / "patches/customization-model.patch"
EXPECTED_BLOBS = {'Resources/term.js': 'bd2208ed2e5ad0e12e2057686d94be8b05f08168'}
OUTPUT_BLOBS = {'Resources/term.js': '4310f707da1c3589f8fa308e8714f0e8bb7abde2', 'Blink/WorkbenchModel.swift': '711dc215dee8a7db0e677478c3628c00101e6d29'}
NEW_PATHS = ['Blink/WorkbenchModel.swift']

def blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
def apply(source):
    source = Path(source).resolve()
    for name, expected in EXPECTED_BLOBS.items():
        if blob((source / name).read_bytes()) != expected:
            raise SystemExit(f"{name} changed; refusing unverified customization-model patch")
    for name in NEW_PATHS:
        target = source / name
        if target.exists() or target.is_symlink():
            raise SystemExit(f"{name} exists; refusing to replace intervening work")
    command = ["git", "apply", "--whitespace=error", str(PATCH)]
    subprocess.run(command[:2] + ["--check"] + command[2:], cwd=source, check=True)
    subprocess.run(command, cwd=source, check=True)
if __name__ == "__main__": apply(sys.argv[1])
