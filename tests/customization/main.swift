import Foundation
func check(_ yes: @autoclosure () throws -> Bool, line: UInt = #line) { precondition(try! yes(), "line \(line)") }
func rejects(_ operation: () throws -> Void) {
  do { try operation() } catch { return }; preconditionFailure("accepted invalid customization")
}
let original = WorkbenchPreferences()
let bytes = try JSONEncoder().encode(original)
check(try WorkbenchPreferences.decode(bytes) == original)
var value = original
var second = value.profile; second.id = UUID(); second.name = "Editing"; second.actions = [.copyAll, .selectAll, .copyScreen, .paste]; second.dpad = true
value.profiles.append(second); value.selectedProfile = second.id
check(value.profile == second)
second.actions.reverse(); value.updateProfile(second)
check(value.profile.actions == [.paste, .copyScreen, .selectAll, .copyAll])
for n in 0..<20 { value.visitHost("host-\(n)") }
check(value.recentHosts.count == 12 && value.recentHosts.first == "host-19")
value.visitHost("host-17"); check(value.recentHosts.first == "host-17" && Set(value.recentHosts).count == 12)
value.labels[UUID().uuidString] = "Production console"
value.favoriteHosts = ["server-one", "server-two"]
check(try WorkbenchPreferences.decode(JSONEncoder().encode(value)) == value)
for mutation: (inout WorkbenchPreferences) -> Void in [
  { $0.version = 2 }, { $0.profiles = [] }, { $0.profiles.append($0.profiles[0]) },
  { $0.selectedProfile = UUID() }, { $0.profiles[0].name = " " },
  { $0.profiles[0].actions = [.copy, .copy] }, { $0.profiles[0].controlSize = 0 },
  { $0.appearance = "unknown" }, { $0.accent = "unknown" },
  { $0.labels["../bad"] = "label" }, { $0.labels[UUID().uuidString] = String(repeating: "a", count: 65) },
  { $0.favoriteHosts = ["a", "a"] }, { $0.recentHosts = (0..<13).map(String.init) }
] {
  var invalid = original; mutation(&invalid)
  let data = try JSONEncoder().encode(invalid)
  rejects { _ = try WorkbenchPreferences.decode(data) }
}
rejects { _ = try WorkbenchPreferences.decode(Data(repeating: 32, count: 1048577)) }
rejects { _ = try WorkbenchPreferences.decode(Data("{}".utf8)) }
var mode = WorkbenchInteraction()
check(!mode.suppressSoftwareKeyboard)
mode.keyboardLocked = true; check(mode.suppressSoftwareKeyboard)
mode.selecting = true; mode.showKeyboard(); check(!mode.selecting && !mode.keyboardLocked && !mode.suppressSoftwareKeyboard)
mode.keyboardHidden = true; check(mode.suppressSoftwareKeyboard)
mode.showKeyboard(); mode.selecting = true; check(mode.suppressSoftwareKeyboard && !mode.keyboardLocked)
print("PASS: preferences/profile round trip, ordering, recent dedup/bounds, version/corruption/unsafe data rejection and explicit input-mode transitions")
let dangerous = "printf '👩🏽‍💻'\n\u{1b}[31m\u{0}"
check(WorkbenchPastePolicy.needsReview(dangerous, enabled: true))
check(!WorkbenchPastePolicy.needsReview(dangerous, enabled: false))
check(!WorkbenchPastePolicy.needsReview("single command", enabled: true))
check(WorkbenchPastePolicy.needsReview(String(repeating: "é", count: 2049), enabled: true))
check(WorkbenchPastePolicy.preview(dangerous).contains("\\u{001B}"))
check(!WorkbenchPastePolicy.preview(dangerous).contains("\u{1b}"))
check(dangerous.hasSuffix("\u{0}"))
print("PASS: paste review UTF-8 threshold, multiline/control detection and visible preview escaping preserve original input")
