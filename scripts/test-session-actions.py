#!/usr/bin/env python3
"""Guarded patch, pure Swift validation, and shell-token boundary regressions.
Does not modify source or connect to hosts. UIKit/AppIntents compile in candidate CI.
"""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('session_patch', ROOT / 'scripts/patch-session-actions.py')
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)
source = Path(sys.argv[1])
inputs = {name: (source / name).read_bytes() for name in p.EXPECTED_BLOBS}
with tempfile.TemporaryDirectory(prefix='blink-session-tests-') as tmp:
    root = Path(tmp)
    def fresh(label):
        tree = root / label
        for name, data in inputs.items():
            target = tree / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        return tree
    tree = fresh('patched')
    p.apply(tree)
    assert {f.relative_to(tree).as_posix() for f in tree.rglob('*') if f.is_file()} == set(inputs) | set(p.NEW_PATHS)
    for idx, name in enumerate([*inputs, *p.NEW_PATHS]):
        other = fresh('guard'+str(idx))
        target = other / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(b'intervening work')
        before = {f.relative_to(other): f.read_bytes() for f in other.rglob('*') if f.is_file()}
        try: p.apply(other)
        except SystemExit: pass
        else: raise AssertionError('accepted changed input')
        assert before == {f.relative_to(other): f.read_bytes() for f in other.rglob('*') if f.is_file()}
    print('PASS: patch applies to exactly five paths; all modified/new path guards reject without partial edits', flush=True)
    compiler = shutil.which('swiftc')
    assert compiler, 'swiftc required'
    for name in ['Blink/SceneDelegate.swift', 'Blink/SpaceController.swift', 'Blink/BlinkIntents.swift']:
        subprocess.run([compiler, '-frontend', '-parse', str(tree / name)], check=True)
    shutil.copyfile(ROOT / 'tests/session-actions/main.swift', root / 'main.swift')
    subprocess.run([compiler, '-swift-version', '5', '-module-cache-path', str(root / 'cache'), str(tree / 'Blink/SessionLink.swift'), str(root / 'main.swift'), '-o', str(root / 'tests')], check=True)
    subprocess.run([str(root / 'tests'), str(root / 'fixtures.json')], check=True)
    # An actual shell launches a fake ssh executable. Metacharacters must arrive
    # as one remote argument, never run on the device. No network or real SSH.
    bindir = root / 'bin'
    bindir.mkdir()
    fake = bindir / 'ssh'
    fake.write_text('#!/usr/bin/env python3\nimport sys,json\nprint(json.dumps(sys.argv[1:]))\n')
    fake.chmod(0o755)
    for fixture in json.loads((root / 'fixtures.json').read_text()):
        result = subprocess.check_output(['/bin/sh', '-c', fixture['line']], cwd=root, env={**os.environ, 'PATH': str(bindir)+os.pathsep+os.environ['PATH']}, text=True)
        assert json.loads(result) == ['-o', 'StrictHostKeyChecking=yes', 'gamecube', '--', fixture['remote']]
        assert not (root / 'LOCAL_EXECUTION_BUG').exists()
    print('PASS: seven command/script fixtures preserve the remote shell boundary without local execution')
    # Wiring contracts complement model behavior; native UI must still be tested.
    ui = (tree / 'Blink/SpaceController.swift').read_text()
    assert 'guard accepted else' in ui and ui.count('BKHosts.withHost(host) != nil') == 2
    assert 'DispatchQueue.main.sync' in ui and 'if Thread.isMainThread' in ui
    intents = (tree / 'Blink/BlinkIntents.swift').read_text()
    assert intents.count('openAppWhenRun: Bool = true') == 3
    assert 'HeadlessSSHRunner' not in intents and 'acceptUnknownHostKeys' not in intents
    print('PASS: foreground confirmation, saved-host revalidation and existing main-thread entry-point guard are wired')
