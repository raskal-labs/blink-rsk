#!/usr/bin/env python3
"""Combined guarded-patch, model, JS and real pipe regressions.
Apple UI type checking belongs to the complete candidate build; no network/device I/O.
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
manifest = json.loads((ROOT/'scripts/customization-paths.json').read_text())
source = Path(sys.argv[1])
modules = []
for name in manifest['order']:
    spec = importlib.util.spec_from_file_location(name.replace('-','_'), ROOT/'scripts'/('patch-'+name+'.py'))
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module); modules.append(module)
with tempfile.TemporaryDirectory(prefix='blink-customization-tests-') as temp:
    temp = Path(temp)
    inputs = {name: (source/name).read_bytes() for name in manifest['modified']}
    def fresh(label, names):
        tree=temp/label
        for name in names:
            p=tree/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(inputs[name])
        return tree
    for number,p in enumerate(modules):
        tree=fresh('patch-'+str(number),p.EXPECTED_BLOBS)
        p.apply(tree)
        assert {f.relative_to(tree).as_posix() for f in tree.rglob('*') if f.is_file()} == set(p.EXPECTED_BLOBS)|set(p.NEW_PATHS)
        for name,digest in p.OUTPUT_BLOBS.items():assert p.blob((tree/name).read_bytes())==digest,name
        for i,name in enumerate([*p.EXPECTED_BLOBS,*p.NEW_PATHS]):
            other=fresh('guard-'+str(number)+'-'+str(i),p.EXPECTED_BLOBS)
            path=other/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(b'preserve intervening work')
            before={f.relative_to(other):f.read_bytes() for f in other.rglob('*') if f.is_file()}
            try:p.apply(other)
            except SystemExit:pass
            else:raise AssertionError('accepted intervening path '+name)
            assert before=={f.relative_to(other):f.read_bytes() for f in other.rglob('*') if f.is_file()}
        before={f.relative_to(tree):f.read_bytes() for f in tree.rglob('*') if f.is_file()}
        try:p.apply(tree)
        except SystemExit:pass
        else:raise AssertionError('accepted double application')
        assert before=={f.relative_to(tree):f.read_bytes() for f in tree.rglob('*') if f.is_file()}
    tree=fresh('combined',manifest['modified'])
    for p in modules:p.apply(tree)
    expected=set(manifest['modified'])|set(manifest['new'])
    assert {f.relative_to(tree).as_posix() for f in tree.rglob('*') if f.is_file()}==expected
    print('PASS: three customization patches compose; exactly 20 reviewed source paths; all input/new-path/double-apply guards reject atomically',flush=True)
    swift=shutil.which('swiftc');assert swift
    for name in expected:
        if name.endswith('.swift'):subprocess.run([swift,'-frontend','-parse',str(tree/name)],check=True)
    shutil.copyfile(ROOT/'tests/customization/main.swift',temp/'main.swift')
    subprocess.run([swift,'-swift-version','5','-module-cache-path',str(temp/'cache'),str(tree/'Blink/WorkbenchModel.swift'),str(temp/'main.swift'),'-o',str(temp/'model-tests')],check=True)
    subprocess.run([str(temp/'model-tests')],check=True)
    cc=shutil.which('cc') or shutil.which('clang');assert cc
    subprocess.run([cc,'-std=c11','-Wall','-Wextra','-Werror','-I',str(tree/'Blink/Terminal'),str(ROOT/'tests/customization/write-step.c'),'-o',str(temp/'write-tests')],check=True)
    subprocess.run([str(temp/'write-tests')],check=True)
    subprocess.run(['node','--check',str(tree/'Resources/term.js')],check=True)
    subprocess.run(['node',str(ROOT/'tests/customization/terminal.js'),str(tree/'Resources/term.js')],check=True)
    if sys.platform=='darwin':
        subprocess.run(['xcrun','clang','-fobjc-arc','-fblocks','-framework','Foundation','-I',str(tree/'Blink/Terminal'),str(tree/'Blink/Terminal/WorkbenchInputDelivery.m'),str(ROOT/'tests/customization/input-delivery.m'),'-o',str(temp/'delivery-tests')],check=True)
        subprocess.run([str(temp/'delivery-tests')],check=True,timeout=45)
        print('PASS: native Foundation ordered-input integration',flush=True)
    else:print('NOT RUN on Linux: native Foundation input-queue integration and Apple UI type checking',flush=True)
    sc=(tree/'Blink/SpaceController.swift').read_text()
    assert 'guard !_spaceControllerAnimating, !_isSnipsInputModeActive else { throw SessionActionError.busy }' in sc
    assert sc.count('self.currentTerm()?.resignInput()')>=4
    assert 'self.focusOnShellAction()' in sc.split('func dismissSnippetsController()')[1].split('MARK: SceneIntent')[0]
    assert 'willTransitionTo pendingViewControllers' in sc and 'workbenchPad.stopRepeating()' in sc
    assert 'workbenchTargets[key]' in sc and '(launch target)' in sc
    assert 'terminal === self.currentTerm()' in sc and 'workbenchPasteConfirmed(text)' in sc
    assert 'FileManager.default.temporaryDirectory' in sc and '.completeFileProtection' in sc
    assert 'if let expected, expected != total' in sc and '4 * 1024 * 1024' in sc
    assert 'terminal.shouldBlockFirstResponder = _isSnipsInputModeActive' in sc
    assert 'workbenchPad.onClose' in sc and 'profile.dpad = false' in sc
    assert 'profile.controlSize * 3 + 16' in sc and 'profile.controlSize * 3 + 64' in sc
    assert 'term_workbenchSetInteraction' in sc and 'terminal === currentTerm()' in sc
    assert 'workbenchTerminalReady(self)' in (tree/'Blink/Terminal/TermController.swift').read_text()
    ui=(tree/'Blink/WorkbenchUI.swift').read_text()
    assert 'TerminalPreviewCell(style: style' in ui and 'editedStyle' in ui
    assert 'styles.updateStyle(next)' not in ui
    assert 'guard storageError == nil' in ui and 'resetExplicitly' in ui
    device=(tree/'Blink/Terminal/TermDevice.m').read_text()
    assert 'write(_pinput[1], input.UTF8String, len)' not in device
    assert '[_inputDelivery invalidate]' in device and 'postNotificationName:@"BlinkWorkbenchInputStatus"' in device
    delivery=(tree/'Blink/Terminal/WorkbenchInputDelivery.m').read_text()
    assert 'F_SETNOSIGPIPE' in delivery and '_framesEpoch != _epoch' in delivery
    assert '_reservations >= 2048' in delivery and '_pending + data.length > 4 * 1024 * 1024' in delivery
    assert 'turn < 16' in delivery and 'dispatch_suspend(_source)' in delivery
    project=(tree/'Blink.xcodeproj/project.pbxproj').read_text()
    for name in ['WorkbenchModel.swift','WorkbenchUI.swift','WorkbenchDock.swift','WorkbenchDPadView.swift','WorkbenchInputDelivery.m']:
        assert project.count('/* '+name+' in Sources */')==2,name
    print('PASS: final wiring preserves Snips/session guard, target identity, native style draft scope, bounded export/input, temporary-file protection and exactly five main-app source registrations',flush=True)
