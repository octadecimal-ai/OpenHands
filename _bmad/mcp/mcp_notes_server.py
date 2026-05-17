#!/usr/bin/env python3
"""
MCP Server - Apple Notes Integration
Integracja z aplikacją Notes w macOS przez AppleScript
"""
import json
import subprocess
import sys
import re

def run_applescript(script):
    """Uruchom AppleScript i zwróć wynik"""
    cmd = ["osascript", "-e", script]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            return {"error": result.stderr.strip()}
        return {"result": result.stdout.strip()}
    except subprocess.TimeoutExpired:
        return {"error": "Timeout"}
    except Exception as e:
        return {"error": str(e)}

def get_notes_list():
    """Pobierz listę notatek"""
    script = '''tell application "Notes"
        set noteNames to {}
        repeat with n in notes
            set end of noteNames to name of n
        end repeat
        return noteNames
    end tell'''
    return run_applescript(script)

def get_note_by_name(name):
    """Pobierz treść notatki po nazwie"""
    escaped_name = name.replace('"', '\\"')
    script = f'''tell application "Notes"
        set theNote to first note whose name = "{escaped_name}"
        return body of theNote
    end tell'''
    return run_applescript(script)

def search_notes(query):
    """Szukaj notatek po fragmencie nazwy"""
    script = f'''tell application "Notes"
        set matchingNotes to {{}}
        repeat with n in notes
            if name of n contains "{query}" then
                set end of matchingNotes to name of n
            end if
        end repeat
        return matchingNotes
    end tell'''
    return run_applescript(script)

def create_note(title, body):
    """Utwórz nową notatkę"""
    escaped_body = body.replace('"', '\\"').replace('\n', '\\n')
    script = f'''tell application "Notes"
        make new note at folder "Notes" with properties {{name:"{title}", body:"{escaped_body}"}}
    end tell'''
    return run_applescript(script)

def handle_request(request):
    """Obsługa żądań MCP"""
    method = request.get("method", "")
    params = request.get("params", {})
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "mcp-server-apple-notes", "version": "1.0.0"}
            }
        }
    
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "result": {
                "tools": [
                    {"name": "notes_list", "description": "Lista wszystkich notatek", "inputSchema": {"type": "object"}},
                    {"name": "notes_get", "description": "Pobierz treść notatki", "inputSchema": {"type": "object", "properties": {"name": {"type": "string"}}}},
                    {"name": "notes_search", "description": "Szukaj notatek", "inputSchema": {"type": "object", "properties": {"query": {"type": "string"}}}},
                    {"name": "notes_create", "description": "Utwórz notatkę", "inputSchema": {"type": "object", "properties": {"title": {"type": "string"}, "body": {"type": "string"}}}}
                ]
            }
        }
    
    elif method == "tools/call":
        tool = params.get("name", "")
        args = params.get("arguments", {})
        
        if tool == "notes_list":
            result = get_notes_list()
        elif tool == "notes_get":
            result = get_note_by_name(args.get("name", ""))
        elif tool == "notes_search":
            result = search_notes(args.get("query", ""))
        elif tool == "notes_create":
            result = create_note(args.get("title", ""), args.get("body", ""))
        else:
            result = {"error": f"Unknown tool: {tool}"}
        
        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "result": {"content": [{"type": "text", "text": json.dumps(result)}]}
        }
    
    return {"error": "Method not found"}

def main():
    """Main loop - czytaj JSON-RPC ze stdin, pisz do stdout"""
    print("Apple Notes MCP Server running on stdio", file=sys.stderr)
    sys.stderr.flush()
    
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
            response = handle_request(request)
            print(json.dumps(response), flush=True)
        except json.JSONDecodeError:
            continue

if __name__ == "__main__":
    main()