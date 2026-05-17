#!/usr/bin/env python3
"""
MCP Server Launcher
Uruchamia skonfigurowane serwery MCP
"""
import subprocess
import json
import os
import sys

MCP_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(MCP_DIR, "servers.json")

def load_config():
    with open(CONFIG_FILE) as f:
        return json.load(f)

def start_filesystem_server(config):
    """Uruchom serwer filesystem"""
    server = config['mcp_servers']['filesystem_project']
    if not server.get('enabled', False):
        print("ℹ️  filesystem_project jest wyłączony")
        return None
    
    path = server['args'][-1]
    print(f"🚀 Uruchamiam filesystem server dla: {path}")
    
    cmd = [server['command']] + server['args']
    print(f"   {' '.join(cmd)}")
    
    try:
        proc = subprocess.Popen(cmd)
        print(f"   PID: {proc.pid}")
        return proc
    except Exception as e:
        print(f"❌ Błąd: {e}")
        return None

def start_apple_events_server(config):
    """Uruchom serwer Apple Events"""
    server = config['mcp_servers'].get('apple_events', {})
    if not server.get('enabled', False):
        print("ℹ️  apple_events jest wyłączony")
        return None
    
    print(f"🚀 Uruchamiam apple_events server")
    
    cmd = [server['command']] + server['args']
    print(f"   {' '.join(cmd)}")
    
    try:
        proc = subprocess.Popen(cmd)
        print(f"   PID: {proc.pid}")
        return proc
    except Exception as e:
        print(f"❌ Błąd: {e}")
        return None

def start_apple_notes_server(config):
    """Uruchom serwer Apple Notes"""
    server = config['mcp_servers'].get('apple_notes', {})
    if not server.get('enabled', False):
        print("ℹ️  apple_notes jest wyłączony")
        return None
    
    print(f"🚀 Uruchamiam apple_notes server")
    
    cmd = [server['command']] + server['args']
    print(f"   {' '.join(cmd)}")
    
    try:
        proc = subprocess.Popen(cmd)
        print(f"   PID: {proc.pid}")
        return proc
    except Exception as e:
        print(f"❌ Błąd: {e}")
        return None

def main():
    print("📂 MCP Server Launcher")
    print("=" * 40)
    
    if not os.path.exists(CONFIG_FILE):
        print(f"❌ Brak konfiguracji: {CONFIG_FILE}")
        sys.exit(1)
    
    config = load_config()
    
    print(f"\n📋 Skonfigurowane serwery:")
    for name, server in config['mcp_servers'].items():
        status = "✅ włączony" if server.get('enabled') else "⏸️  wyłączony"
        print(f"   - {name}: {status}")
    
    print("\n" + "=" * 40)
    
    # Uruchom serwery
    processes = []
    
    fs_proc = start_filesystem_server(config)
    if fs_proc:
        processes.append(fs_proc)
    
    apple_proc = start_apple_events_server(config)
    if apple_proc:
        processes.append(apple_proc)
    
    notes_proc = start_apple_notes_server(config)
    if notes_proc:
        processes.append(notes_proc)
    
    if processes:
        print(f"\n✅ {len(processes)} serwer(y) działa(ą)")
        print("   Naciśnij Ctrl+C aby zatrzymać")
        try:
            # Czekaj na wszystkie procesy
            for proc in processes:
                proc.wait()
        except KeyboardInterrupt:
            for proc in processes:
                proc.terminate()
            print("\n⏹️  Zatrzymano")
    else:
        print("\n❌ Nie udało się uruchomić żadnego serwera")

if __name__ == "__main__":
    main()
