#!/usr/bin/env python3
"""Guarded combined-customization patch; apply after the six accepted repairs.
Offline only. Reject changed inputs/new-path collisions atomically.
"""
import hashlib
from pathlib import Path
import subprocess
import sys
PATCH = Path(__file__).resolve().parents[1] / "patches/customization-input.patch"
EXPECTED_BLOBS = {'Blink/Terminal/TermDevice.h': '3cb56a448a258660454aa297fecf77515d3daf19', 'Blink/Terminal/TermDevice.m': '30626cd2eaf37b024ea7d429fe27b6f9b2a934fb', 'Blink/Terminal/TermView.h': '0124d532ccf2679c38e7109ff0d5ab6ed0759e40', 'Blink/Terminal/TermView.m': '7ffa417558872490c018540cfa23e469546f84f2', 'Blink/Terminal/TermController.swift': 'cef620e715d4228b2c6f30cedfcfccdeda3472d5', 'Blink/SmarterKeys/SmarterTermInput.swift': '23591db454596e90c6d45017bc3070d467aa2c79', 'Blink/SmarterKeys/KBView.swift': 'd909149b506274317aa0e23d2d1df7ae049b8dc4'}
OUTPUT_BLOBS = {'Blink/Terminal/TermDevice.h': '289aded5348288ca229fcacd8bd1b8d1bdec70c2', 'Blink/Terminal/TermDevice.m': '6d741b9b28ca735ac0d21b40cdef0856228c4b39', 'Blink/Terminal/TermView.h': '3974002337bcfb9359c927200d2de7824ada9a4e', 'Blink/Terminal/TermView.m': 'e81e456a347cca7e1ef3dc79fe1cf524f3d950b8', 'Blink/Terminal/TermController.swift': 'd3836f0f6cce4f4c342abeaca1a472c7cf3c9bc3', 'Blink/SmarterKeys/SmarterTermInput.swift': '93cc19fdfae2d27072d8763cbc35fe873969348d', 'Blink/SmarterKeys/KBView.swift': '9e6763b87c032aa8c6319f22ff7a24b8180f89d0', 'Blink/Terminal/WorkbenchInputDelivery.h': '84cade5960a92de827b8d10dc28e694ec02f8e4d', 'Blink/Terminal/WorkbenchInputDelivery.m': '0d408bc90d73cf4c0b042304a7ca53751b57ebb5', 'Blink/Terminal/WorkbenchWriteStep.h': 'afc7c0402e2f7c1b4e9d6b274599706da2dee0a1'}
NEW_PATHS = ['Blink/Terminal/WorkbenchInputDelivery.h', 'Blink/Terminal/WorkbenchInputDelivery.m', 'Blink/Terminal/WorkbenchWriteStep.h']

def blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
def apply(source):
    source = Path(source).resolve()
    for name, expected in EXPECTED_BLOBS.items():
        if blob((source / name).read_bytes()) != expected:
            raise SystemExit(f"{name} changed; refusing unverified customization-input patch")
    for name in NEW_PATHS:
        target = source / name
        if target.exists() or target.is_symlink():
            raise SystemExit(f"{name} exists; refusing to replace intervening work")
    command = ["git", "apply", "--whitespace=error", str(PATCH)]
    subprocess.run(command[:2] + ["--check"] + command[2:], cwd=source, check=True)
    subprocess.run(command, cwd=source, check=True)
if __name__ == "__main__": apply(sys.argv[1])
