#!/usr/bin/env python3
"""Only blinksh 9e8767b75 Snips resign + madjinn a31aa977 gesture detach.
Apply AFTER session-actions. No rendering/scroll queue or keyboard-lock import.
"""
import hashlib
from pathlib import Path
import subprocess
import sys
PATCH = Path(__file__).resolve().parents[1] / "patches/terminal-input-gestures.patch"
EXPECTED_BLOBS = {'Blink/SpaceController.swift': '7c001a1e69622367bea4c1f20cac9ba225036d47', 'Blink/WebKit/WKWebView.swift': 'a04ca8ab70dd97639a91f130ca89e166b67b2269'}
OUTPUT_BLOBS = {'Blink/SpaceController.swift': '5415b30d4cb27f04e9f65c1641978ba04d0a8612', 'Blink/WebKit/WKWebView.swift': 'd4674be632ab0b66e0f85002514d7de8fd886776'}
def blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
def apply(source):
    source = Path(source).resolve()
    for name, expected in EXPECTED_BLOBS.items():
        if blob((source / name).read_bytes()) != expected:
            raise SystemExit(f"{name} changed; refusing unverified terminal corrections")
    command = ["git", "apply", "--whitespace=error", str(PATCH)]
    subprocess.run(command[:2] + ["--check"] + command[2:], cwd=source, check=True)
    subprocess.run(command, cwd=source, check=True)
if __name__ == "__main__": apply(sys.argv[1])
