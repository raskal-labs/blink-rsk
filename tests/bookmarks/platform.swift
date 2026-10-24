// Apple's bookmark and security-scope APIs do not exist in Linux Foundation.
// These signatures only let the unchanged Access.live adapter type-check. They
// fail if accidentally used; every runtime test injects its own Access adapter.
// On macOS this file is empty and the real Foundation API signatures compile.
#if os(Linux)
import Foundation

extension URL {
  struct BookmarkCreationOptions: OptionSet {
    let rawValue: Int
    static let minimalBookmark = Self(rawValue: 1)
  }
  struct BookmarkResolutionOptions: OptionSet {
    let rawValue: Int
    static let withoutUI = Self(rawValue: 1)
  }
  init(resolvingBookmarkData: Data, options: BookmarkResolutionOptions,
       relativeTo: URL?, bookmarkDataIsStale: inout Bool) throws {
    fatalError("Live Apple bookmark API must not be used by Linux tests")
  }
  func bookmarkData(options: BookmarkCreationOptions, includingResourceValuesForKeys: [URLResourceKey]?,
                    relativeTo: URL?) throws -> Data {
    fatalError("Live Apple bookmark API must not be used by Linux tests")
  }
  func startAccessingSecurityScopedResource() -> Bool {
    fatalError("Live Apple security scope API must not be used by Linux tests")
  }
  func stopAccessingSecurityScopedResource() {
    fatalError("Live Apple security scope API must not be used by Linux tests")
  }
}
#endif
