#!/usr/bin/env python3
"""Isolated guarded application, real Swift/pure logic and real shell boundaries.
No network, credentials, signing or installation. Native APIs compile in candidate CI.
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
spec = importlib.util.spec_from_file_location('expansion', ROOT/'scripts/patch-shortcuts-expansion.py')
p = importlib.util.module_from_spec(spec); spec.loader.exec_module(p)
inputs = {name: (Path(sys.argv[1])/name).read_bytes() for name in p.EXPECTED_BLOBS}
with tempfile.TemporaryDirectory(prefix='blink-shortcuts-') as tmp:
    temp = Path(tmp)
    def fresh(label):
        tree = temp/label
        for name, data in inputs.items():
            target = tree/name; target.parent.mkdir(parents=True, exist_ok=True); target.write_bytes(data)
        return tree
    tree = fresh('source'); p.apply(tree)
    assert {f.relative_to(tree).as_posix() for f in tree.rglob('*') if f.is_file()} == set(inputs)|set(p.NEW_PATHS)
    for i, name in enumerate([*inputs, *p.NEW_PATHS]):
        other = fresh('guard'+str(i)); target = other/name
        target.parent.mkdir(parents=True, exist_ok=True); target.write_bytes(b'preserve intervening work')
        before = {f.relative_to(other): f.read_bytes() for f in other.rglob('*') if f.is_file()}
        try: p.apply(other)
        except SystemExit: pass
        else: raise AssertionError('accepted changed/new path '+name)
        assert before == {f.relative_to(other): f.read_bytes() for f in other.rglob('*') if f.is_file()}
    compiler = shutil.which('swiftc'); assert compiler
    for name in [*inputs, *p.NEW_PATHS]:
        if name.endswith('.swift'):
            subprocess.run([compiler,'-frontend','-parse',str(tree/name)],check=True)
    shutil.copyfile(ROOT/'tests/shortcuts/main.swift',temp/'main.swift')
    subprocess.run([compiler,'-swift-version','5','-module-cache-path',str(temp/'cache'),str(tree/'Blink/SessionLink.swift'),str(temp/'main.swift'),'-o',str(temp/'tests')],check=True)
    fixtures = temp/'fixtures.json'
    subprocess.run([str(temp/'tests'),str(fixtures)],check=True)
    bindir = temp/'bin'; bindir.mkdir()
    fake = bindir/'ssh'; fake.write_text('#!/usr/bin/env python3\nimport sys,json\nprint(json.dumps(sys.argv[1:]))\n'); fake.chmod(0o755)
    shutil.copyfile(fake,bindir/'mosh'); (bindir/'mosh').chmod(0o755)
    env = {**os.environ,'PATH':str(bindir)+os.pathsep+os.environ['PATH']}
    for item in json.loads(fixtures.read_text()):
        result = subprocess.check_output(['/bin/sh','-c',item['line']],cwd=temp,env=env,text=True)
        assert json.loads(result) == ['-o','StrictHostKeyChecking=yes','gamecube','--',item['remote']]
    count = 0
    for item in json.loads(Path(str(fixtures)+'.execution').read_text()):
        if 'mosh' in item:
            args = json.loads(subprocess.check_output(['/bin/sh','-c',item['mosh']],cwd=temp,env=env,text=True))
            assert args[:2] == ['gamecube','--'] and len(args) == 3
            # Matches MoshClientParams + mosh-server startup argument concatenation.
            result = subprocess.run(['/bin/sh','-c',args[2]],cwd=temp,capture_output=True,text=True)
            assert result.stdout == '$(touch LOCAL_EXECUTION_BUG)' and result.returncode == 0
        else:
            result = subprocess.run(['/bin/sh','-c',item['line']],cwd=temp,capture_output=True,text=True)
            assert result.stdout == item['stdout']+'\n'+item['nonce']+':'+str(item['status'])+'\n', (item,result)
            if item['status'] != 2: assert result.stderr == item['stderr']
            count += 1
        assert not (temp/'LOCAL_EXECUTION_BUG').exists()
    sc = (tree/'Blink/SpaceController.swift').read_text()
    assert 'guard !isSnipsInputModeActive, !_spaceControllerAnimating' in sc
    assert sc.index('link.canReuseSession(true)') < sc.index('_newShellAction(command: link.terminalCommand)')
    assert sc.count('self.currentTerm()?.resignInput()') == inputs['Blink/SpaceController.swift'].decode().count('self.currentTerm()?.resignInput()')
    assert 'self.focusOnShellAction()' in sc.split('func dismissSnippetsController()')[1]
    runner = (tree/'Blink/ShortcutsRunner.swift').read_text()
    assert 'acceptUnknownHostKeys' not in runner and 'InteractiveResponse.affirmative' not in runner
    assert 'verifyHostCallback: verify' in runner and 'bk.defaultSigners()' in runner and 'AuthPasswordInteractive' in runner
    assert 'handleEvents(receiveCancel:' in runner and 'DispatchWorkItem' in runner
    intents = (tree/'Blink/BlinkIntents.swift').read_text()
    assert intents.count('openAppWhenRun: Bool = true') == 8
    assert 'ReturnsValue<IntentFile>' in intents and '@Parameter(title: "File") var file: IntentFile' in intents
    # Candidate CI diagnosed this initializer as iOS 18-only; keep iOS 16 actions compatible.
    assert 'supportedContentTypes:' not in intents
    assert 'location.isAvailable' in intents and 'removeLocation' not in intents
    files = (tree/'Blink/ShortcutsFiles.swift').read_text()
    assert 'NSFileCoordinator()' in files and 'if scoped { url.stopAccessingSecurityScopedResource() }' in files
    assert 'file.read(max:' in files and '.tryReduce(Data())' in files and 'data.count + block.count <= ShortcutPolicy.fileLimit' in files
    sftp = (tree/'SSH/SFTP.swift').read_text()
    exclusive = sftp.split('public func createExclusive')[1].split('public func remove')[0]
    assert 'O_EXCL' in exclusive and 'O_TRUNC' not in exclusive
    assert 'contents.count >= maxEntries' in sftp
    print(f'PASS: seven-path patch and atomic guards; Swift syntax; seven SSH boundaries; {count} actual exit/stdio wrappers; Mosh shell boundary; foreground/auth/bounds/scopes/exclusive-create integration contracts')
