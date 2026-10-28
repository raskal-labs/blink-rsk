#!/usr/bin/env python3
"""Inspect the packaged IPA; no signing, install or device acceptance inference."""
import hashlib
import json
from pathlib import Path
import plistlib
import sys
import zipfile
EXPECTED = {
    'OpenTerminalSessionIntent', 'RunCommandOnHostIntent', 'RunScriptOnHostIntent',
    'FocusSessionIntent', 'ListRemoteDirectoryIntent', 'DownloadFileIntent',
    'UploadFileIntent', 'OpenSavedFolderIntent',
}
ipa = Path(sys.argv[1])
with zipfile.ZipFile(ipa) as z:
    assert z.testzip() is None
    main = 'Payload/Blink.app/'
    data = json.loads(z.read(main+'Metadata.appintents/extract.actionsdata'))
    actions = data['actions']
    assert set(actions) == EXPECTED, set(actions)
    for name, action in actions.items():
        assert action['isDiscoverable'] and action['openAppWhenRun'], name
        assert 'resultValueType' in action, (name, sorted(action))
    parameters = {p['name'] for p in actions['OpenTerminalSessionIntent']['parameters']}
    assert parameters == {'host', 'sessionName', 'connection', 'startingCommand', 'reuse'}, parameters
    assert any(p['name'] == 'file' for p in actions['UploadFileIntent']['parameters'])
    identifiers = {}
    for suffix, expected in [('', 'sh.blink.blinkshell'),
                            ('PlugIns/BlinkFileProviderExtension.appex/', 'sh.blink.blinkshell.BlinkFileProviderExtension'),
                            ('PlugIns/BlinkFileProviderExtensionUI.appex/', 'sh.blink.blinkshell.BlinkFileProviderExtensionUI')]:
        info = plistlib.loads(z.read(main+suffix+'Info.plist'))
        assert info['CFBundleIdentifier'] == expected
        identifiers[suffix or 'main'] = expected
    appex = {n.split('/')[3] for n in z.namelist() if n.startswith(main+'PlugIns/') and '.appex/' in n}
    assert appex == {'BlinkFileProviderExtension.appex','BlinkFileProviderExtensionUI.appex'}, appex
    assert not any(n.endswith('embedded.mobileprovision') for n in z.namelist())
    receipt = {'schema': 1, 'sha256': hashlib.sha256(ipa.read_bytes()).hexdigest(),
               'actions': {name: {'resultValueType': action['resultValueType'],
                                  'parameters': [p['name'] for p in action['parameters']]} for name, action in actions.items()},
               'bundle_ids': identifiers, 'zip_crc': 'passed', 'device_acceptance': 'Unknown'}
    Path(sys.argv[2]).write_text(json.dumps(receipt, indent=2)+'\n')
print('PASS: packaged CRC, eight discoverable foreground actions with returned values, parameter contract, original bundle IDs and exactly two provider extensions')
