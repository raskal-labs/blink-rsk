#!/usr/bin/env python3
"""Test patch guards, then compile/exercise the patched manager in isolation.

Usage: python3 scripts/test-bookmark-recovery.py PINNED_SOURCE [--patch-only]
The source argument is never modified. Runtime tests require swiftc. Linux uses
test-only shims for Apple's unavailable URL APIs; the manager logic is unchanged.
"""
import argparse
import importlib.util
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("bookmark_patch", ROOT / "scripts/patch-bookmark-recovery.py")
patcher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(patcher)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--patch-only", action="store_true", help="explicitly omit the Swift runtime suite")
    args = parser.parse_args()
    inputs = {name: (args.source / name).read_bytes() for name in patcher.EXPECTED_BLOBS}

    with tempfile.TemporaryDirectory(prefix="blink-bookmark-tests-") as temp:
        root = Path(temp)

        def fresh(label):
            tree = root / label
            for name, data in inputs.items():
                path = tree / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
            (tree / "unrelated.txt").write_text("preserve this file\n")
            return tree

        tree = fresh("patched")
        patcher.apply(tree)
        assert (tree / "unrelated.txt").read_text() == "preserve this file\n"
        assert all((tree / name).read_bytes() != data for name, data in inputs.items())
        assert {p.relative_to(tree).as_posix() for p in tree.rglob("*") if p.is_file()} == set(inputs) | {"unrelated.txt"}
        print("PASS: pinned patch applies offline to exactly the two intended files", flush=True)

        for changed in inputs:
            other = fresh("guard-" + Path(changed).stem)
            (other / changed).write_bytes(inputs[changed] + b"\n// intervening work\n")
            before = {name: (other / name).read_bytes() for name in inputs}
            try:
                patcher.apply(other)
            except SystemExit:
                pass
            else:
                raise AssertionError("changed source was accepted")
            assert all((other / name).read_bytes() == data for name, data in before.items())
            print("PASS: changed input is rejected without partial edits: " + changed, flush=True)

        before = {name: (tree / name).read_bytes() for name in inputs}
        try:
            patcher.apply(tree)
        except SystemExit:
            pass
        else:
            raise AssertionError("double application was accepted")
        assert all((tree / name).read_bytes() == data for name, data in before.items())
        print("PASS: double application is rejected without edits", flush=True)

        if args.patch_only:
            print("NOT RUN: Swift runtime regressions (--patch-only selected)", flush=True)
            return
        compiler = shutil.which("swiftc")
        if compiler is None:
            raise SystemExit("Swift runtime regressions require swiftc; no runtime tests ran")

        subprocess.run([compiler, "-frontend", "-parse",
                        str(tree / "Settings/ViewControllers/BookmarkedLocations/BookmarkedLocationsView.swift")],
                       check=True)
        print("PASS: patched settings Swift syntax (not SwiftUI type checking)", flush=True)

        manager = (tree / "Settings/Model/BookmarkedLocationsManager.swift").read_text()
        # Only remove app-module/Objective-C wiring. The actual manager logic,
        # Foundation I/O and production URL adapter compile unchanged on macOS.
        manager = manager.replace("import BlinkConfig", """enum BlinkPaths {
  static func blinkURL() -> URL { URL(fileURLWithPath: NSTemporaryDirectory()) }
  static func homeURL() -> URL { blinkURL() }
}""").replace("@objc ", "")
        (root / "Manager.swift").write_text(manager)
        shutil.copyfile(ROOT / "tests/bookmarks/main.swift", root / "main.swift")
        shutil.copyfile(ROOT / "tests/bookmarks/platform.swift", root / "Platform.swift")
        if sys.platform == "linux":
            print("PLATFORM: Linux URL shims; actual Apple bookmark/scope behavior is not tested", flush=True)
        executable = root / "bookmark-tests"
        subprocess.run([compiler, "-swift-version", "5", "-module-cache-path", str(root / "module-cache"),
                        str(root / "Manager.swift"), str(root / "Platform.swift"), str(root / "main.swift"),
                        "-o", str(executable)], check=True)
        subprocess.run([str(executable)], check=True)


if __name__ == "__main__":
    main()
