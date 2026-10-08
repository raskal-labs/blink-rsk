#!/usr/bin/env python3
"""Patch pinned Blink to resolve SideStore's provisioned shared App Group.

Applies to BlinkConfig, used by both the app and its File Provider extensions.
Never substitutes per-process private storage for an unavailable shared group.
"""
from pathlib import Path
import sys

ORIGINAL = "+ (NSString *) infoPlistFullGroupID {\n  return [NSString stringWithFormat:@\"group.%@\", [self infoPlistGroupID]];\n}"
REPLACEMENT = "+ (NSDictionary *)_installedProfileEntitlements {\n  static NSDictionary *entitlements;\n  static dispatch_once_t once;\n  dispatch_once(&once, ^{\n    NSString *path = [NSBundle.mainBundle pathForResource:@\"embedded\" ofType:@\"mobileprovision\"];\n    NSData *profile = path ? [NSData dataWithContentsOfFile:path] : nil;\n    if (!profile) { return; }\n\n    // iOS has already validated the installed profile. Read its XML payload\n    // for capability names; this parser does not authenticate profiles.\n    NSData *startTag = [@\"<plist\" dataUsingEncoding:NSUTF8StringEncoding];\n    NSData *endTag = [@\"</plist>\" dataUsingEncoding:NSUTF8StringEncoding];\n    NSRange start = [profile rangeOfData:startTag options:0 range:NSMakeRange(0, profile.length)];\n    if (start.location == NSNotFound) {\n      [NSException raise:@\"BlinkProvisioningProfileError\" format:@\"Installed profile has no XML plist payload\"];\n    }\n    NSRange tail = NSMakeRange(start.location, profile.length - start.location);\n    NSRange end = [profile rangeOfData:endTag options:0 range:tail];\n    if (end.location == NSNotFound) {\n      [NSException raise:@\"BlinkProvisioningProfileError\" format:@\"Installed profile has an incomplete XML plist payload\"];\n    }\n    NSData *xml = [profile subdataWithRange:NSMakeRange(start.location, NSMaxRange(end) - start.location)];\n    NSError *error = nil;\n    id plist = [NSPropertyListSerialization propertyListWithData:xml options:NSPropertyListImmutable format:nil error:&error];\n    id values = [plist isKindOfClass:NSDictionary.class] ? plist[@\"Entitlements\"] : nil;\n    if (![values isKindOfClass:NSDictionary.class]) {\n      [NSException raise:@\"BlinkProvisioningProfileError\" format:@\"Installed profile has no valid entitlements dictionary: %@\", error];\n    }\n    entitlements = values;\n  });\n  return entitlements;\n}\n\n+ (NSString *) infoPlistFullGroupID {\n  NSString *configured = [NSString stringWithFormat:@\"group.%@\", [self infoPlistGroupID]];\n  NSDictionary *entitlements = [self _installedProfileEntitlements];\n  if (!entitlements) {\n    // Preserve upstream behavior for builds without an embedded profile.\n    return configured;\n  }\n  id groups = entitlements[@\"com.apple.security.application-groups\"];\n  if (![groups isKindOfClass:NSArray.class]) {\n    [NSException raise:@\"BlinkAppGroupError\" format:@\"Installed profile grants no App Groups for %@\", configured];\n  }\n  if ([groups containsObject:configured]) {\n    return configured;\n  }\n  NSMutableArray<NSString *> *matches = [NSMutableArray array];\n  NSString *prefix = [configured stringByAppendingString:@\".\"];\n  for (id group in groups) {\n    if ([group isKindOfClass:NSString.class] && [group hasPrefix:prefix]) {\n      [matches addObject:group];\n    }\n  }\n  if (matches.count != 1) {\n    [NSException raise:@\"BlinkAppGroupError\" format:@\"Expected one provisioned match for %@; found %lu\", configured, (unsigned long)matches.count];\n  }\n  NSLog(@\"[Blink SideStore] Resolved shared App Group: %@\", matches.firstObject);\n  return matches.firstObject;\n}"

def apply(source):
    path = Path(source) / "BlinkConfig/XCConfig.m"
    content = path.read_text()
    if content.count(ORIGINAL) != 1:
        raise SystemExit("XCConfig App Group resolver changed; refusing an unverified patch")
    path.write_text(content.replace(ORIGINAL, REPLACEMENT))

if __name__ == "__main__":
    apply(sys.argv[1])
