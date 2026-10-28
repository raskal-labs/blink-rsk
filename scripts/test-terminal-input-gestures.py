#!/usr/bin/env python3
"""Exact narrow parity, atomic guard rejection, Snips restoration + attach contracts."""
import importlib.util
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('terminal_patch', ROOT/'scripts/patch-terminal-input-gestures.py')
p = importlib.util.module_from_spec(spec); spec.loader.exec_module(p)
source = Path(sys.argv[1])
inputs = {name: (source/name).read_bytes() for name in p.EXPECTED_BLOBS}
with tempfile.TemporaryDirectory(prefix='blink-terminal-') as tmp:
    tree = Path(tmp)
    for name, data in inputs.items():
        target = tree/name; target.parent.mkdir(parents=True, exist_ok=True); target.write_bytes(data)
    p.apply(tree)
    for name, expected in p.OUTPUT_BLOBS.items():
        assert p.blob((tree/name).read_bytes()) == expected
        subprocess.run([shutil.which('swiftc'), '-frontend', '-parse', str(tree/name)], check=True)
    sc = (tree/'Blink/SpaceController.swift').read_text()
    assert sc.count('self.currentTerm()?.resignInput()') == inputs['Blink/SpaceController.swift'].decode().count('self.currentTerm()?.resignInput()') + 2
    for method, call in [('showSnippetsAction', 'presentSnippetsController()'), ('showSnippetsWithScratchAction', 'presentSnippetsControllerWithScratch()')]:
        # Upstream method naming is independent of this narrow check.
        index = sc.index('    self.'+call)
        assert sc[index-50:index].endswith('    self.currentTerm()?.resignInput()\n\n')
    dismiss = sc.split('  func dismissSnippetsController() {')[1].split('\n  }')[0]
    assert '_dismissSnippetsController' in dismiss and 'self.focusOnShellAction()' in dismiss
    assert 'ctrl._isSnipsInputModeActive = false' in sc
    wk = (tree/'Blink/WebKit/WKWebView.swift').read_text()
    assert 'webView.addGestureRecognizer(r)' in wk
    assert '_wkWebView?.removeGestureRecognizer(r)' in wk
    assert '_wkWebView?.addGestureRecognizer(r)' not in wk
    assert '_enqueueScroll' not in wk and '_pendingWheelDeltaY' not in wk
    for changed in inputs:
        for name, data in inputs.items(): (tree/name).write_bytes(data)
        (tree/changed).write_bytes(inputs[changed]+b'\n// changed\n')
        before = {name: (tree/name).read_bytes() for name in inputs}
        try: p.apply(tree)
        except SystemExit: pass
        else: raise AssertionError('accepted intervening work')
        assert before == {name: (tree/name).read_bytes() for name in inputs}
    print('PASS: exact three-line correction parity; atomic file guards; attachment retained; Snips dismiss/refocus path retained; Swift syntax')
