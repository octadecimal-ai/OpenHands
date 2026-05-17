# MCP Server Configuration

## Status: ✅ Faza 5 COMPLETED

OpenHands zintegrowany z MCP dla macOS (2026-05-17).

## OpenHands MCP Integration

```bash
# Lista skonfigurowanych serwerów
openhands mcp list

# Dodane serwery:
# • filesystem_project - npx @modelcontextprotocol/server-filesystem
# • apple_events - /opt/homebrew/bin/mcp-server-apple-events  
# • apple_notes - python3 mcp_notes_server.py
```

## Pliki konfiguracyjne

- `servers.json` - Konfiguracja serwerów MCP
- `launcher.py` - Launcher do uruchamiania serwerów
- `test_mcp_client.py` - Klient testowy MCP

## Zainstalowane serwery

### 1. Filesystem Server
- **Package**: `@modelcontextprotocol/server-filesystem@0.2.0`
- **Path**: `/opt/homebrew/lib/node_modules/@modelcontextprotocol/server-filesystem/dist/index.js`
- **Scope**: Katalog projektu
- **Status**: ✅ Skonfigurowany

### 2. Apple Events Server
- **Package**: `mcp-server-apple-events@1.4.0`
- **Path**: `/opt/homebrew/bin/mcp-server-apple-events`
- **Features**: Apple Reminders i Calendar
- **Status**: ✅ Skonfigurowany
- **Notes**: Wymaga TCC permissions

## Testowanie

```bash
# Test komunikacji
python3 _bmad/mcp/test_mcp_client.py

# Uruchomienie serwerów
python3 _bmad/mcp/launcher.py
```

## Protokół MCP

- **Version**: 2024-11-05
- **Transport**: stdio (JSON-RPC 2.0)
- **Tools available**: 
  - Filesystem: read_file, read_text_file, read_directory
  - Apple: reminders_list, reminders_add, calendar_events

## Następne kroki

1. ⚠️ MACOS APP NOTES - wymaga JavaScript OSA lub alternatywnego podejścia
2. Integracja z LLM Desktop
3. Test pełnej ścieżki agentowej