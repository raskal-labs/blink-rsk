// Regression harness for the actual patched manager. All files and bookmark
// bytes are synthetic; no device storage, profiles or keys are accessed.
import Foundation
import Dispatch

enum TestFailure: Error { case injected }
let fm = FileManager.default
var testsRun = 0

func check(_ condition: Bool, _ message: String = "", file: StaticString = #file, line: UInt = #line) {
  precondition(condition, message, file: file, line: line)
}

final class Fixture {
  let root = fm.temporaryDirectory.appendingPathComponent(UUID().uuidString)
  var config: URL { root.appendingPathComponent("config") }
  var home: URL { root.appendingPathComponent("home") }
  var target: URL { root.appendingPathComponent("target") }
  var json: URL { config.appendingPathComponent(".locations.json") }
  var link: URL { home.appendingPathComponent("phone") }
  var resolutionFails = false
  var denied = false
  var unreadable = false
  var stale = false
  var refreshFails = false
  var starts = 0
  var stops = 0
  var balance = 0
  var onBookmark: (() throws -> Void)?

  init() throws {
    for url in [config, home, target] {
      try fm.createDirectory(at: url, withIntermediateDirectories: true)
    }
  }

  deinit {
    check(balance == 0, "unbalanced security scope at manager destruction")
    try? fm.removeItem(at: root)
  }

  func seed(_ names: [String] = ["phone"]) throws {
    let records = names.map { ["name": $0, "bookmarkData": Data(target.path.utf8).base64EncodedString()] }
    try JSONSerialization.data(withJSONObject: records, options: [.sortedKeys]).write(to: json)
  }

  func manager() -> BookmarkedLocationsManager {
    let access = BookmarkedLocationsManager.Access(
      resolve: { [self] data in
        if resolutionFails { throw TestFailure.injected }
        let value = String(decoding: data, as: UTF8.self)
        let path = value.hasPrefix("fresh:") ? String(value.dropFirst(6)) : value
        return (URL(fileURLWithPath: path), stale && !value.hasPrefix("fresh:"))
      },
      bookmark: { [self] url in
        try onBookmark?()
        if refreshFails { throw TestFailure.injected }
        return Data(("fresh:" + url.path).utf8)
      },
      start: { [self] _ in
        starts += 1
        if denied { return false }
        balance += 1
        return true
      },
      stop: { [self] _ in
        stops += 1
        balance -= 1
        check(balance >= 0, "stopped an unacquired scope")
      },
      isReadable: { [self] url in !unreadable && fm.isReadableFile(atPath: url.path) }
    )
    return BookmarkedLocationsManager(storedLocationsDirectory: config, symlinkBaseDirectory: home, access: access)
  }

  func destination() -> String? { try? fm.destinationOfSymbolicLink(atPath: link.path) }

  func failNextWrite() {
    onBookmark = { [self] in
      onBookmark = nil
      try fm.moveItem(at: json, to: config.appendingPathComponent("saved.json"))
      try fm.createDirectory(at: json, withIntermediateDirectories: false)
    }
  }

  func restoreJSON() throws {
    try fm.removeItem(at: json)
    try fm.moveItem(at: config.appendingPathComponent("saved.json"), to: json)
  }
}

func expectFailure(_ body: () throws -> Void) {
  do { try body() } catch { return }
  preconditionFailure("expected operation to fail")
}

func test(_ name: String, _ body: (Fixture) throws -> Void) throws {
  let fixture = try Fixture()
  try body(fixture)
  check(fixture.balance == 0, "scope retained after test: \(name)")
  testsRun += 1
  print("PASS: \(name)")
}

try test("legacy JSON round trip, readable-only exports and repeated reads reuse one scope") { f in
  try f.seed()
  let before = try Data(contentsOf: f.json)
  var m: BookmarkedLocationsManager? = f.manager()
  check(try m!.getLocations().first!.isAvailable)
  check(m!.getLocationURLs() == [f.target])
  check(m!.getLocationPaths() == [f.target.path])
  check(f.starts == 1 && f.balance == 1)
  check(try Data(contentsOf: f.json) == before)
  m = nil
  check(f.stops == 1)
}

try test("resolution failure preserves bytes and names across reload, then recovers") { f in
  try f.seed()
  let before = try Data(contentsOf: f.json)
  f.resolutionFails = true
  for _ in 0..<2 {
    let m = f.manager()
    let locations = try m.getLocations()
    check(locations.count == 1 && locations[0].name == "phone" && !locations[0].isAvailable)
    check(m.getLocationPaths().isEmpty && m.getLocationURLs().isEmpty)
    check(try Data(contentsOf: f.json) == before)
  }
  check(f.starts == 0 && f.stops == 0)
  f.resolutionFails = false
  let m = f.manager()
  check(try m.getLocations()[0].isAvailable)
  check(f.destination() == f.target.path)
}

try test("scope denial and unreadability retain saved data and balance successful starts") { f in
  try f.seed()
  let before = try Data(contentsOf: f.json)
  let m = f.manager()
  f.denied = true
  check(try !m.getLocations()[0].isAvailable)
  check(f.balance == 0 && f.stops == 0)
  f.denied = false
  f.unreadable = true
  check(try !m.getLocations()[0].isAvailable)
  check(f.balance == 0 && f.stops == 1)
  check(try Data(contentsOf: f.json) == before)
  f.unreadable = false
  check(try m.getLocations()[0].isAvailable)
}

try test("stale refresh failure retains original bytes; retry persists refreshed legacy schema") { f in
  try f.seed()
  let before = try Data(contentsOf: f.json)
  f.stale = true
  f.refreshFails = true
  let m = f.manager()
  check(try !m.getLocations()[0].isAvailable)
  check(try Data(contentsOf: f.json) == before)
  check(f.balance == 0)
  f.refreshFails = false
  check(try m.getLocations()[0].isAvailable)
  let objects = try JSONSerialization.jsonObject(with: Data(contentsOf: f.json)) as! [[String: Any]]
  check(Set(objects[0].keys) == Set(["name", "bookmarkData"]))
  check(try Data(contentsOf: f.json) != before)
  let reloaded = f.manager()
  check(try reloaded.getLocations()[0].isAvailable)
}

try test("read collision with regular file or directory never removes data") { f in
  try f.seed()
  let before = try Data(contentsOf: f.json)
  let m = f.manager()
  try Data("unrelated".utf8).write(to: f.link)
  check(try !m.getLocations()[0].isAvailable)
  check(try String(contentsOf: f.link, encoding: .utf8) == "unrelated")
  try fm.removeItem(at: f.link)
  try fm.createDirectory(at: f.link, withIntermediateDirectories: false)
  let sentinel = f.link.appendingPathComponent("keep.txt")
  try Data("keep".utf8).write(to: sentinel)
  check(try !m.getLocations()[0].isAvailable)
  check(fm.fileExists(atPath: sentinel.path))
  check(try Data(contentsOf: f.json) == before)
  check(f.balance == 0)
}

try test("read collision with unrelated symlink preserves alias and excludes shell path") { f in
  try f.seed()
  try fm.createSymbolicLink(at: f.link, withDestinationURL: f.config)
  let m = f.manager()
  check(try !m.getLocations()[0].isAvailable)
  check(m.getLocationPaths().isEmpty)
  check(f.destination() == f.config.path)
  try fm.removeItem(at: f.link)
  check(try m.getLocations()[0].isAvailable)
}

try test("dangling bookmark alias survives target outage and recovers when target returns") { f in
  try f.seed()
  try fm.createSymbolicLink(at: f.link, withDestinationURL: f.target)
  try fm.removeItem(at: f.target)
  let m = f.manager()
  check(try !m.getLocations()[0].isAvailable)
  check(f.destination() == f.target.path)
  try fm.createDirectory(at: f.target, withIntermediateDirectories: false)
  check(try m.getLocations()[0].isAvailable)
  check(f.balance == 1)
}

try test("add rejects unavailable duplicate names, dangling conflicts and unsafe names") { f in
  try f.seed()
  let m = f.manager()
  f.resolutionFails = true
  expectFailure { _ = try m.addLocation(name: "phone", location: f.target) }
  try fm.createSymbolicLink(atPath: f.home.appendingPathComponent("dangling").path, withDestinationPath: "/missing-blink-test-target")
  for name in ["dangling", "", ".", "..", "../outside", "a/b", "a\0b"] {
    expectFailure { _ = try m.addLocation(name: name, location: f.target) }
  }
  check(f.starts == 0)
}

try test("add failures do not leave aliases or leaked scopes") { f in
  try f.seed([])
  let before = try Data(contentsOf: f.json)
  let m = f.manager()
  f.refreshFails = true
  expectFailure { _ = try m.addLocation(name: "phone", location: f.target) }
  check(f.destination() == nil && f.balance == 0)
  f.refreshFails = false
  f.failNextWrite()
  expectFailure { _ = try m.addLocation(name: "phone", location: f.target) }
  check(f.destination() == nil && f.balance == 0)
  try f.restoreJSON()
  check(try Data(contentsOf: f.json) == before)
  _ = try m.addLocation(name: "phone", location: f.target)
  check(m.getLocationPaths() == [f.target.path])
}

try test("reselection replaces only chosen record and alias, preserving target contents") { f in
  try f.seed(["phone", "other"])
  let sentinel = f.target.appendingPathComponent("keep.txt")
  try Data("keep".utf8).write(to: sentinel)
  try fm.createSymbolicLink(atPath: f.link.path, withDestinationPath: "/unavailable-blink-test-target")
  let m = f.manager()
  f.resolutionFails = true
  check(try !m.getLocations()[0].isAvailable)
  f.resolutionFails = false
  _ = try m.reselectLocation(name: "phone", location: f.config)
  check(f.destination() == f.config.path)
  check(fm.fileExists(atPath: sentinel.path))
  let all = try m.getLocations()
  check(all.map { $0.name } == ["phone", "other"])
  check(all[0].url == f.config && all[1].url == f.target)
}

try test("reselection refuses regular-file collision and preserves saved bytes") { f in
  try f.seed()
  try Data("keep".utf8).write(to: f.link)
  let before = try Data(contentsOf: f.json)
  let m = f.manager()
  expectFailure { _ = try m.reselectLocation(name: "phone", location: f.target) }
  check(try String(contentsOf: f.link, encoding: .utf8) == "keep")
  check(try Data(contentsOf: f.json) == before)
  check(f.balance == 0)
}

try test("reselection write failure restores alias and retains original active scope") { f in
  try f.seed()
  let before = try Data(contentsOf: f.json)
  let m = f.manager()
  check(try m.getLocations()[0].isAvailable)
  f.failNextWrite()
  expectFailure { _ = try m.reselectLocation(name: "phone", location: f.config) }
  check(f.destination() == f.target.path && f.balance == 1)
  try f.restoreJSON()
  check(try Data(contentsOf: f.json) == before)
  check(m.getLocationPaths() == [f.target.path])
}

try test("explicit unavailable deletion removes saved entry and dangling alias, never target") { f in
  try f.seed()
  try fm.createSymbolicLink(at: f.link, withDestinationURL: f.target)
  let sentinel = f.target.appendingPathComponent("keep.txt")
  try Data("keep".utf8).write(to: sentinel)
  f.resolutionFails = true
  let m = f.manager()
  try m.removeLocation(name: "phone")
  check(try m.getLocations().isEmpty)
  check(try f.manager().getLocations().isEmpty)
  check(f.destination() == nil && fm.fileExists(atPath: sentinel.path))
  // A name without a saved record must not authorize removal of any link.
  try fm.createSymbolicLink(at: f.link, withDestinationURL: f.target)
  try m.removeLocation(name: "phone")
  check(f.destination() == f.target.path)
}

try test("explicit deletion preserves conflicting ordinary files") { f in
  try f.seed()
  try Data("keep".utf8).write(to: f.link)
  let m = f.manager()
  try m.removeLocation(name: "phone")
  check(try String(contentsOf: f.link, encoding: .utf8) == "keep")
  check(try m.getLocations().isEmpty)
}

try test("unreadable store and malformed JSON never get overwritten or retain allowed paths") { f in
  try f.seed()
  let m = f.manager()
  check(!m.getLocationPaths().isEmpty && f.balance == 1)
  let bad = Data("{invalid json".utf8)
  try bad.write(to: f.json)
  expectFailure { _ = try m.getLocations() }
  check(m.getLocationPaths().isEmpty && f.balance == 0)
  check(try Data(contentsOf: f.json) == bad)
  try fm.removeItem(at: f.json)
  try fm.createDirectory(at: f.json, withIntermediateDirectories: false)
  expectFailure { _ = try m.getLocations() }
}

try test("missing store reads do not create an empty file") { f in
  let m = f.manager()
  check(try m.getLocations().isEmpty)
  check(!fm.fileExists(atPath: f.json.path))
}

try test("one failed location does not remove a healthy neighbor") { f in
  try f.seed(["phone", "other"])
  try Data("collision".utf8).write(to: f.link)
  let before = try Data(contentsOf: f.json)
  let m = f.manager()
  let all = try m.getLocations()
  check(all.count == 2 && !all[0].isAvailable && all[1].isAvailable)
  check(m.getLocationPaths() == [f.target.path])
  check(try Data(contentsOf: f.json) == before)
}

try test("access loss after a successful read releases its scope and permits later reacquisition") { f in
  try f.seed()
  let before = try Data(contentsOf: f.json)
  let m = f.manager()
  check(m.getLocationPaths() == [f.target.path] && f.balance == 1)
  f.resolutionFails = true
  check(m.getLocationPaths().isEmpty && f.balance == 0 && f.stops == 1)
  f.resolutionFails = false
  check(m.getLocationPaths() == [f.target.path] && f.balance == 1)
  f.unreadable = true
  check(m.getLocationPaths().isEmpty && f.balance == 0 && f.stops == 2)
  check(try Data(contentsOf: f.json) == before)
  f.unreadable = false
  check(m.getLocationPaths() == [f.target.path] && f.balance == 1)
}

try test("missing alias directory causes a recoverable link creation failure") { f in
  try f.seed()
  let before = try Data(contentsOf: f.json)
  try fm.removeItem(at: f.home)
  let m = f.manager()
  check(try !m.getLocations()[0].isAvailable)
  check(f.balance == 0 && f.stops == 1)
  check(try Data(contentsOf: f.json) == before)
  try fm.createDirectory(at: f.home, withIntermediateDirectories: false)
  check(try m.getLocations()[0].isAvailable)
}

try test("unavailable legacy unsafe names remain saved and can be explicitly removed without path operations") { f in
  try f.seed(["../outside"])
  let outside = f.root.appendingPathComponent("outside")
  try Data("keep".utf8).write(to: outside)
  let before = try Data(contentsOf: f.json)
  let m = f.manager()
  check(try !m.getLocations()[0].isAvailable)
  check(m.getLocationPaths().isEmpty && f.starts == 0)
  check(try Data(contentsOf: f.json) == before)
  try m.removeLocation(name: "../outside")
  check(try m.getLocations().isEmpty)
  check(try String(contentsOf: outside, encoding: .utf8) == "keep")
}

try test("relative alias for the correct target is accepted without rewriting it") { f in
  try f.seed()
  try fm.createSymbolicLink(atPath: f.link.path, withDestinationPath: "../target")
  let m = f.manager()
  check(m.getLocationPaths() == [f.target.path])
  check(f.destination() == "../target")
}

try test("concurrent shell reads retain one scope and do not rewrite saved bytes") { f in
  try f.seed()
  let before = try Data(contentsOf: f.json)
  let m = f.manager()
  DispatchQueue.concurrentPerform(iterations: 32) { _ in
    check(m.getLocationPaths() == [f.target.path])
  }
  check(f.starts == 1 && f.balance == 1)
  check(try Data(contentsOf: f.json) == before)
}

try test("reselection grant and alias survive manager reload") { f in
  try f.seed()
  var m: BookmarkedLocationsManager? = f.manager()
  _ = try m!.reselectLocation(name: "phone", location: f.config)
  m = nil
  let reloaded = f.manager()
  check(try reloaded.getLocations()[0].name == "phone")
  check(reloaded.getLocationURLs() == [f.config])
  check(f.destination() == f.config.path)
}

try test("deletion with an unreadable store preserves entry, alias and acquired scope") { f in
  try f.seed()
  let m = f.manager()
  check(try m.getLocations()[0].isAvailable)
  try fm.moveItem(at: f.json, to: f.config.appendingPathComponent("saved.json"))
  try fm.createDirectory(at: f.json, withIntermediateDirectories: false)
  expectFailure { try m.removeLocation(name: "phone") }
  check(f.destination() == f.target.path && f.balance == 1)
  try f.restoreJSON()
  check(try m.getLocations().count == 1)
  try m.removeLocation(name: "phone")
  check(try f.manager().getLocations().isEmpty)
  check(f.balance == 0)
}

print("\(testsRun) bookmark runtime regressions passed")
