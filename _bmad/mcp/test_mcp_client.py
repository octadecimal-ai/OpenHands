#!/usr/bin/env python3
"""
MCP Client - Test komunikacji z serwerami MCP
"""
import json
import subprocess
import sys

def send_mcp_request(server_cmd, request):
    """Wyślij request JSON do serwera MCP przez stdio"""
    proc = subprocess.Popen(
        server_cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    request_json = json.dumps(request) + "\n"
    stdout, stderr = proc.communicate(input=request_json, timeout=10)
    
    if stderr:
        print(f"   STDERR: {stderr[:200]}")
    
    return stdout

def test_filesystem_server():
    """Test filesystem server"""
    print("\n🧪 TEST: Filesystem Server")
    print("-" * 40)
    
    server_cmd = [
        "node",
        "/opt/homebrew/lib/node_modules/@modelcontextprotocol/server-filesystem/dist/index.js",
        "/Users/admin/Developer/multi-agent-systems/develop/openhands-bmad-agt"
    ]
    
    # Initialize
    print("1. Wysyłanie initialize...")
    response = send_mcp_request(server_cmd, {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "mcp-test-client", "version": "1.0.0"}
        }
    })
    print(f"   Odpowiedź: {response[:300]}")
    
    # List tools
    print("\n2. Wysyłanie tools/list...")
    response = send_mcp_request(server_cmd, {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    })
    print(f"   Odpowiedź: {response[:500]}")
    
    return True

def test_apple_events_server():
    """Test apple events server"""
    print("\n🧪 TEST: Apple Events Server")
    print("-" * 40)
    
    server_cmd = ["mcp-server-apple-events"]
    
    # Initialize
    print("1. Wysyłanie initialize...")
    try:
        response = send_mcp_request(server_cmd, {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "mcp-test-client", "version": "1.0.0"}
            }
        })
        print(f"   Odpowiedź: {response[:500]}")
        return True
    except Exception as e:
        print(f"   ❌ Błąd: {e}")
        return False

def main():
    print("=" * 50)
    print("🔍 MCP Client - Test Suite")
    print("=" * 50)
    
    results = []
    
    results.append(("Filesystem", test_filesystem_server()))
    results.append(("Apple Events", test_apple_events_server()))
    
    print("\n" + "=" * 50)
    print("📊 WYNIKI TESTÓW")
    print("=" * 50)
    
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {name}: {status}")
    
    all_passed = all(r[1] for r in results)
    print("\n" + ("🎉 WSZYSTKIE TESTY PRZESZŁY" if all_passed else "⚠️  NIEKTÓRE TESTY NIE PRZESZŁY"))
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())