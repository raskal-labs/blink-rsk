#!/usr/bin/env python3
"""Backport blinksh/blink@7e28d172's exact startup-cleanup disable, offline.

Fail closed on intervening source edits. No domain reset, data operations,
build, signing or installation is performed.
"""
import hashlib
from pathlib import Path
import subprocess
import sys

PATCH = Path(__file__).resolve().parents[1] / "patches/fileprovider-startup-cleanup.patch"
SOURCE_PATH = "BlinkFileProvider/FileProviderReplicatedExtension.swift"
INPUT_BLOB = "5a2e68107f52bd95f6c64c3b852ba6bed667c7bc"
OUTPUT_BLOB = "9381403608eb952db0c399b65a4e0e02004514c2"
UPSTREAM_COMMIT = "7e28d1721ecb6614951040477036ef31d5a0964e"


def blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def apply(source):
    source = Path(source).resolve()
    if blob((source / SOURCE_PATH).read_bytes()) != INPUT_BLOB:
        raise SystemExit(f"{SOURCE_PATH} changed; refusing an unverified File Provider patch")
    command = ["git", "apply", "--whitespace=error", str(PATCH)]
    subprocess.run(command[:2] + ["--check"] + command[2:], cwd=source, check=True)
    subprocess.run(command, cwd=source, check=True)


if __name__ == "__main__":
    apply(sys.argv[1])
