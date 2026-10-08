#!/usr/bin/env python3
"""Compile and exercise the actual patched XCConfig resolver on macOS."""
from pathlib import Path
import plistlib
import subprocess
import sys
import tempfile

source = Path(sys.argv[1]).resolve()
with tempfile.TemporaryDirectory(prefix="blink-app-groups-") as temp:
    root = Path(temp)
    bundle = root / "Resolver.app"
    resources = bundle / "Contents/Resources"
    executable_dir = bundle / "Contents/MacOS"
    resources.mkdir(parents=True)
    executable_dir.mkdir(parents=True)
    info = {"CFBundleIdentifier": "io.raskal.group-resolver-test",
            "CFBundleExecutable": "Resolver", "CFBundlePackageType": "APPL",
            "BLINK_GROUP_ID": "sh.blink"}
    (bundle / "Contents/Info.plist").write_bytes(plistlib.dumps(info))
    main = root / "main.m"
    main.write_text(r'''
#import <Foundation/Foundation.h>
#import "XCConfig.h"
int main(void) {
  @autoreleasepool {
    @try {
      puts([XCConfig.infoPlistFullGroupID UTF8String]);
      return 0;
    } @catch (NSException *exception) {
      fprintf(stderr, "%s: %s\n", exception.name.UTF8String, exception.reason.UTF8String);
      return 2;
    }
  }
}
''')
    executable = executable_dir / "Resolver"
    subprocess.run(["xcrun", "clang", "-fobjc-arc", "-fblocks",
                    "-framework", "Foundation", "-I", str(source / "BlinkConfig"),
                    str(source / "BlinkConfig/XCConfig.m"), str(main),
                    "-o", str(executable)], check=True)
    profile = resources / "embedded.mobileprovision"

    def check(label, groups=None, expected=None, error=None, raw=None, absent=False):
        if absent:
            profile.unlink(missing_ok=True)
        else:
            entitlements = {} if groups is None else {"com.apple.security.application-groups": groups}
            payload = plistlib.dumps({"Entitlements": entitlements})
            # Opaque CMS-like wrapper: tests XML extraction, not CMS authentication.
            profile.write_bytes(raw if raw is not None else b"\x30\x82\xff\x00" + payload + b"\x00\xff")
        result = subprocess.run([str(executable)], capture_output=True, text=True)
        if error:
            assert result.returncode == 2 and error in result.stderr, (label, result)
        else:
            assert result.returncode == 0 and result.stdout.strip() == expected, (label, result)
        print("PASS:", label)

    check("upstream exact group", ["group.sh.blink"], expected="group.sh.blink")
    for role in ("main app", "File Provider", "File Provider UI"):
        check(role + " resolves the same signed group",
              ["group.unrelated", "group.sh.blink.73F2VG4BAJ"],
              expected="group.sh.blink.73F2VG4BAJ")
    check("no embedded profile preserves upstream behavior", absent=True, expected="group.sh.blink")
    check("missing group capability", error="BlinkAppGroupError")
    check("wrong group capability type", "group.sh.blink", error="BlinkAppGroupError")
    check("unrelated group rejected", ["group.other"], error="BlinkAppGroupError")
    check("ambiguous groups rejected", ["group.sh.blink.ONE", "group.sh.blink.TWO"], error="BlinkAppGroupError")
    check("malformed profile rejected", raw=b"<plist>broken</plist>", error="BlinkProvisioningProfileError")
    check("missing XML rejected", raw=b"not a profile", error="BlinkProvisioningProfileError")
    check("incomplete XML rejected", raw=b"<plist>", error="BlinkProvisioningProfileError")
