#!/usr/bin/env python3
"""Verify exact upstream parity and patch guards in isolated copies.

Does not modify the supplied source or run the provider. Apple FileProvider
type checking requires the complete iOS build; this is not a sync-recovery test.
"""
import importlib.util
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("fp_patch", ROOT / "scripts/patch-fileprovider-startup-cleanup.py")
patcher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(patcher)
original = (Path(sys.argv[1]) / patcher.SOURCE_PATH).read_bytes()

with tempfile.TemporaryDirectory(prefix="blink-fp-startup-") as temp:
    tree = Path(temp)
    target = tree / patcher.SOURCE_PATH
    target.parent.mkdir(parents=True)
    target.write_bytes(original)
    sentinel = tree / "unrelated.txt"
    sentinel.write_bytes(b"preserve intervening work\n")
    patcher.apply(tree)
    assert patcher.blob(target.read_bytes()) == patcher.OUTPUT_BLOB
    assert {p.relative_to(tree).as_posix() for p in tree.rglob("*") if p.is_file()} == {
        patcher.SOURCE_PATH, "unrelated.txt"}
    assert sentinel.read_bytes() == b"preserve intervening work\n"
    print("PASS: one provider file matches the exact upstream output blob; unrelated file preserved", flush=True)

    compiler = shutil.which("swiftc")
    if compiler:
        subprocess.run([compiler, "-frontend", "-parse", str(target)], check=True)
        print("PASS: Swift syntax (Apple FileProvider type checking not performed)", flush=True)
    else:
        print("NOT RUN: Swift syntax; swiftc unavailable", flush=True)

    for label, data in [("double application", target.read_bytes()),
                        ("intervening edit", original + b"\n// intervening work\n")]:
        target.write_bytes(data)
        try:
            patcher.apply(tree)
        except SystemExit:
            pass
        else:
            raise AssertionError("accepted " + label)
        assert target.read_bytes() == data
        assert sentinel.read_bytes() == b"preserve intervening work\n"
        print("PASS: " + label + " rejected without edits", flush=True)
