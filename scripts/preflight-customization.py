#!/usr/bin/env python3
"""Offline integration preflight from exact pristine pinned source; no CI dispatch.
Use macOS for native Foundation/resolver coverage; Linux records those exclusions.
"""
from pathlib import Path
import ast
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import yaml
ROOT=Path(__file__).resolve().parents[1]
source=Path(sys.argv[1]).resolve()
pin='a90b4423c8b7a86770c24a7eaa6c13b0a5904b18'
custom=json.loads((ROOT/'scripts/customization-paths.json').read_text())
combined=json.loads((ROOT/'scripts/customization-combined-paths.json').read_text())
original=set(combined)-set(custom['new'])-{'Blink/SessionLink.swift','Blink/BlinkIntents.swift','Blink/ShortcutsRunner.swift','Blink/ShortcutsFiles.swift'}
with tempfile.TemporaryDirectory(prefix='blink-complete-customization-') as temp:
    tree=Path(temp);inputs={}
    for name in sorted(original):
        data=subprocess.check_output(['git','-C',str(source),'show',pin+':'+name])
        target=tree/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data);inputs[name]=data
    for repair in ['sidestore-app-groups','bookmark-recovery','session-actions','fileprovider-startup-cleanup','terminal-input-gestures','shortcuts-expansion']:
        if repair!='sidestore-app-groups':subprocess.run([sys.executable,str(ROOT/'scripts'/('test-'+repair+'.py')),str(tree)],check=True)
        subprocess.run([sys.executable,str(ROOT/'scripts'/('patch-'+repair+'.py')),str(tree)],check=True)
    subprocess.run([sys.executable,str(ROOT/'scripts/test-customization.py'),str(tree)],check=True)
    for repair in custom['order']:subprocess.run([sys.executable,str(ROOT/'scripts'/('patch-'+repair+'.py')),str(tree)],check=True)
    changed={p.relative_to(tree).as_posix() for p in tree.rglob('*') if p.is_file() and (p.relative_to(tree).as_posix() not in inputs or p.read_bytes()!=inputs[p.relative_to(tree).as_posix()])}
    assert changed==set(combined),(changed,set(combined))
    # Existing WK gesture teardown correction remains untouched by customization.
    assert '_wkWebView?.removeGestureRecognizer(r)' in (tree/'Blink/WebKit/WKWebView.swift').read_text()
    provider=(tree/'BlinkFileProvider/FileProviderReplicatedExtension.swift').read_bytes()
    assert hashlib.sha1(b"blob "+str(len(provider)).encode()+b"\0"+provider).hexdigest()=='9381403608eb952db0c399b65a4e0e02004514c2'
    print('PASS: all nine guarded patches compose on exact pin; exactly 31 source paths; existing provider polling/startup and gesture teardown repairs retained',flush=True)
for path in (ROOT/'scripts').glob('*.py'):ast.parse(path.read_text(),filename=str(path))
workflow=yaml.safe_load((ROOT/'.github/workflows/build-newsguytor-fileprovider.yml').read_text())
assert workflow.get('on',workflow.get(True))=={'workflow_dispatch':None}
for step in workflow['jobs']['build']['steps']:
    if 'run' not in step:continue
    subprocess.run(['bash','-n'],input=step['run'],text=True,check=True)
    for block in re.findall(r"python3 - <<'PY'\n(.*?)\nPY",step['run'],re.S):compile(block,'workflow-python','exec')
subprocess.run(['git','diff','--check'],cwd=ROOT,check=True)
print('PASS: manual-only workflow, embedded shell/Python, harness Python and whitespace checks',flush=True)
if sys.platform!='darwin':print('NOT RUN locally: Apple UI type checking, native input delivery/resolver integration, full iOS compilation, codesigning, App Intents extraction and IPA packaging',flush=True)
