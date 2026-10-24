import Foundation

func check(_ condition: @autoclosure () throws -> Bool, _ message: String = "assertion") {
  precondition(try! condition(), message)
}
func rejects(_ body: () throws -> Void) {
  do { try body() } catch { return }
  preconditionFailure("unexpectedly accepted input")
}
func parse(_ value: String) throws -> SessionLink { try SessionLink.parse(URL(string: value)!) }

let host = try parse("blinkshell://host/gamecube?id=logs")
check(host.host == "gamecube" && host.id == "logs" && host.remoteCommand == nil)
check(host.terminalCommand == "ssh -o StrictHostKeyChecking=yes gamecube")
check(try parse("BLINKSHELL://focus?id=logs").kind == .focus)
check(try SessionLink.navigation(host: nil, id: nil).kind == .terminal)
for bad in [
  "blinkshell://run?cmd=id", "blinkshell://host/gamecube?cmd=id",
  "blinkshell://host/gamecube?key=secret", "blinkshell://host/gamecube?script=id",
  "blinkshell://host/gamecube?mosh=1", "blinkshell://host/gamecube?id=a&id=b",
  "blinkshell://host/gamecube?id=", "blinkshell://host/gamecube?id",
  "blinkshell://host/gamecube?id=a&unknown=b", "blinkshell://host/gamecube#cmd=id",
  "blinkshell://user:pass@host/gamecube", "blinkshell://host:22/gamecube",
  "blinkshell://host/-oProxyCommand=x", "blinkshell://host/.hidden", "blinkshell://host/a/b",
  "blinkshell://host/a%20b", "blinkshell://host/a%0Ab", "blinkshell://host/a%3Bid",
  "blinkshell://host/a%2520b", "blinkshell://host/a@b", "blinkshell://host/",
  "blinkshell://focus", "blinkshell://focus/path?id=a", "blinkshell://focus?id=../a",
  "ssh://host/gamecube", "blinkshell://x-callback-url/run?cmd=id"
] { rejects { _ = try parse(bad) } }
rejects { _ = try SessionLink.navigation(host: "a", id: String(repeating: "a", count: 65)) }
rejects { _ = try SessionLink.navigation(host: String(repeating: "a", count: 254), id: nil) }
for bad in ["", " ", "id\nwhoami", "id\r", "id\0", "id\u{1b}", String(repeating: "x", count: 8001)] {
  rejects { _ = try SessionLink.execution(host: "gamecube", command: bad) }
}
for bad in ["-oFoo=x", "a b", "user@host"] {
  rejects { _ = try SessionLink.execution(host: bad, command: "id") }
}
rejects { _ = try SessionLink.execution(host: "gamecube", command: "id", interpreter: "sh; id") }
rejects { _ = try SessionLink.execution(host: "gamecube", command: "id\0", interpreter: "sh") }
let script = "printf '%s\\n' \"hello\"\nprintf '%s' '$(id); literal'\n"
let request = try SessionLink.execution(host: "gamecube", command: script, interpreter: "sh")
check(request.id == nil && request.preview == script)
let b64 = String(request.remoteCommand!.split(separator: "'")[1])
check(String(data: Data(base64Encoded: b64)!, encoding: .utf8) == script)
check(host.canReuseSession(true) && !host.canReuseSession(false))
check(!request.canReuseSession(true))
let samples = ["printf '%s' 'hello'", "echo $(touch LOCAL_EXECUTION_BUG)", "id; touch LOCAL_EXECUTION_BUG", "echo `touch LOCAL_EXECUTION_BUG`", "printf '%s' \"double\"", "echo \\backslash"]
var fixtures: [[String: String]] = []
for sample in samples {
  let action = try SessionLink.execution(host: "gamecube", command: sample)
  fixtures.append(["line": action.terminalCommand, "remote": sample])
}
fixtures.append(["line": request.terminalCommand, "remote": request.remoteCommand!])
let output = URL(fileURLWithPath: CommandLine.arguments[1])
try JSONSerialization.data(withJSONObject: fixtures).write(to: output)
print("PASS: navigation-only URLs, strict host tokens, invalid action parameters, script round trip and session reuse policy")
