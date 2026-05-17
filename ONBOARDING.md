# Onboarding Guide - Octadecimal OpenHands + BMAD

## Cel dokumentu

Przywrócenie kontekstu i narzędzi dla nowego zespołu po klonowaniu repo.

---

## 1. Wymagania wstępne

### System
- macOS (Ventura/Sonoma/Sequoia)
- Python 3.11+
- Node.js 18+ (dla MCP servers)

### Zainstalowane narzędzia
```bash
# OpenHands
pip install openhands

# MCP servers
npm install -g @modelcontextprotocol/server-filesystem
brew install mcp-server-apple-events

# Git configured
git config --global user.name "Twoje Imie"
git config --global user.email "twoj@email.com"
```

---

## 2. Konfiguracja MCP (Faza 5 - ukończona)

### Zarejestrowane serwery MCP
```bash
openhands mcp list
# ✅ filesystem_project - npx @modelcontextprotocol/server-filesystem
# ✅ apple_events - /opt/homebrew/bin/mcp-server-apple-events  
# ✅ apple_notes - python3 mcp_notes_server.py
```

### Lokalizacja config
```
~/.local/share/uv/tools/openhands/config.toml
```

### Rejestracja nowego serwera
```bash
openhands mcp add <name> <command> [args...]
```

---

## 3. Uprawnienia TCC (Faza 3)

### Przyznane uprawnienia dla Terminal
- **Notes** - Pełny dostęp (318 notatek)
- **Calendar** - Pełny dostęp (19 kalendarzy)
- **Reminders** - Pełny dostęp

### Weryfikacja
```bash
# Test Reminders
osascript -e 'tell application "Reminders" to get name of lists'

# Test Notes
osascript -e 'tell application "Notes" to get name of folders'
```

---

## 4. Struktura projektu

```
openhands-bmad-agt/
├── _bmad/                    # Konfiguracja BMAD
│   ├── mcp/                   # MCP servers
│   │   ├── servers.json       # Definicje serwerów
│   │   ├── launcher.py        # Launcher
│   │   └── mcp_notes_server.py # Custom Notes server
│   └── output/                # Artifacts BMAD
├── .agents/                   # BMAD Skills (74 skilli)
│   └── skills/
│       ├── bmad-agent-dev/    # Developer Agent
│       ├── bmad-agent-architect/ # Architect Agent
│       ├── bmad-create-story/ # Story creation
│       ├── bmad-sprint-planning/ # Sprint planning
│       └── ... (70+ more)
├── docs/                      # Dokumentacja
│   ├── openhands/             # OpenHands specific
│   │   └── tasks/             # Task plans
│   │       └── P0-Orchestracja-multiagentow-macOS-Plan.md
│   └── ...
├── AGENTS.md                  # Agent memory
└── README.md                  # (tworzony)
```

---

## 5. Aktualny stan projektu P0

### Ukończone fazy
| Faza | Status | Opis |
|------|--------|------|
| Faza 3 | ✅ | TCC & Uprawnienia macOS |
| Faza 5 | ✅ | OpenHands MCP Integration |

### Task tracker (T5.x - ostatni)
```
T5.1: Aktualizacja config OpenHands (mcp_tools) - ✅ 2026-05-17
T5.2: Test połączenia z macOS MCP Server - ✅ 2026-05-17
T5.3: Walidacja wszystkich narzędzi MCP - ✅ 2026-05-17
T5.4: Dokumentacja integracji - ✅ 2026-05-17
```

### Następne zadania (Faza 6)
| ID | Zadanie | Priorytet |
|----|---------|-----------|
| T6.1 | Test: Agent tworzy reminder | P0 |
| T6.2 | Test: Agent odczytuje notatki | P0 |
| T6.3 | Test: Agent taguje plik | P0 |
| T6.4 | Test: wielu agentów jednocześnie | P1 |
| T6.5 | Test: obsługa błędu TCC | P0 |

---

## 6. Kluczowa wiedza

### MCP Server dla Apple Events
- Serwer: `mcp-server-apple-events`
- Narzędzia: calendar, reminders, notes, finder_tags
- Konfiguracja: `/opt/homebrew/bin/mcp-server-apple-events`

### Task tracking
- Plany zadań: `docs/openhands/tasks/`
- Task tracker: kontekst sesji

### Znane issues
- TCC wymaga manualnego przyznania w System Preferences
- GitHub token (`GITHUB_TOKEN`) wymaga aktualizacji jeśli wygasł

---

## 7. Szybki start

```bash
# 1. Sklonuj repo
git clone https://github.com/piotradamczyk78/openhands-bmad-agt.git
cd openhands-bmad-agt

# 2. Skonfiguruj MCP
openhands mcp add apple_events /opt/homebrew/bin/mcp-server-apple-events

# 3. Weryfikuj połączenie
openhands mcp list

# 4. Test TCC
osascript -e 'tell application "Reminders" to get name of lists'

# 5. Przeczytaj plan projektu
cat docs/openhands/tasks/P0-Orchestracja-multiagentow-macOS-Plan.md
```

---

## 8. Kontakt / Team Octadecimal

- Repozytorium: https://github.com/piotradamczyk78/openhands-bmad-agt
- Organizacja: Octadecimal
- Brancha główna: `main`
- Feature branch: `feature/initial-cleanup`