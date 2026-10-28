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

let mosh = try SessionLink.opening(host: "gamecube", id: "logs", transport: .mosh, command: nil, reuse: true)
check(mosh.canReuseSession(true) && mosh.terminalCommand == "mosh gamecube")
let fresh = try SessionLink.opening(host: "gamecube", id: "logs", transport: .ssh, command: nil, reuse: false)
check(!fresh.canReuseSession(true))
for transport: SessionLink.Transport in [.ssh, .mosh] {
  let start = try SessionLink.opening(host: "gamecube", id: "logs", transport: transport, command: "printf '%s' '$(literal)'", reuse: true)
  check(!start.canReuseSession(true) && start.id == "logs")
}
rejects { _ = try SessionLink.opening(host: nil, id: nil, transport: .mosh, command: nil, reuse: true) }
rejects { _ = try SessionLink.opening(host: nil, id: nil, transport: .ssh, command: "id", reuse: true) }
for value in ["", ".", "..", "a/b", "a\\b", "a\n", "a\0", String(repeating: "x", count: 256)] {
  rejects { _ = try ShortcutPolicy.filename(value) }
}
for value in ["a b.txt", "-flag", "é.txt", "quote's.txt"] { check(try ShortcutPolicy.filename(value) == value) }
check(try ShortcutPolicy.path("a b/é") == "~/a b/é")
check(try ShortcutPolicy.path("~/a") == "~/a")
check(try ShortcutPolicy.path("/tmp/a") == "/tmp/a")
for value in ["", "\0", "a\n", "~user/path", "path/~", String(repeating: "x", count: 4097)] {
  rejects { _ = try ShortcutPolicy.path(value) }
}
let nonce = "BLINK_TEST_123"
for raw in ["hello", "hello\n", "", "\n__BLINK_EXIT_0__\n", "quotes ' \\"] {
  for code: Int32 in [0, 1, 127, 255] {
    let parsed = try ShortcutPolicy.parse(Data((raw + "\n" + nonce + ":\(code)\n").utf8), nonce: nonce)
    check(parsed.0 == raw && parsed.1 == code)
  }
}
for raw in ["", "\nOTHER:0\n", "\n\(nonce):0\nextra", "\n\(nonce):-1\n", "\n\(nonce):256\n", "\n\(nonce):0"] {
  rejects { _ = try ShortcutPolicy.parse(Data(raw.utf8), nonce: nonce) }
}
var executionFixtures: [[String: Any]] = []
for (command, stdout, stderr, status) in [
  ("printf hi", "hi", "", 0), ("printf 'hi\\n'", "hi\n", "", 0),
  ("printf err >&2; exit 17", "", "err", 17), ("exit 23", "", "", 23),
  ("printf ok # a trailing comment", "ok", "", 0), ("exec printf done", "done", "", 0),
  ("printf '%s' '$(touch LOCAL_EXECUTION_BUG)'", "$(touch LOCAL_EXECUTION_BUG)", "", 0),
  ("if", "", "", 2)
] {
  executionFixtures.append(["line": ShortcutPolicy.wrapped(command, nonce: nonce), "stdout": stdout, "stderr": stderr, "status": status, "nonce": nonce])
}
let moshStart = try SessionLink.opening(host: "gamecube", id: "x", transport: .mosh, command: "printf '%s' '$(touch LOCAL_EXECUTION_BUG)'", reuse: true)
executionFixtures.append(["mosh": moshStart.terminalCommand])
try JSONSerialization.data(withJSONObject: executionFixtures).write(to: URL(fileURLWithPath: CommandLine.arguments[1]+".execution"))
// Simultaneous timeout/cancellation/completion resolve exactly once, including
// cancellation before continuation installation. Runs the production bridge.
for before in [false, true] {
  for _ in 0..<40 {
    let gate = ShortcutCompletion<Int>()
    let done = DispatchSemaphore(value: 0)
    if before { gate.finish(.success(9)) }
    Task.detached {
      let value = try! await withCheckedThrowingContinuation { gate.install($0) }
      check([9, 10, 11].contains(value))
      done.signal()
    }
    DispatchQueue.global().async { gate.finish(.success(10)) }
    DispatchQueue.global().async { gate.finish(.success(11)) }
    check(done.wait(timeout: .now()+3) == .success)
    check(gate.isFinished)
  }
}
print("PASS: Mosh/fresh-start policy, filenames/paths, exact exit trailer, 80 continuation races")
