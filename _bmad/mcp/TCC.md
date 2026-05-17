# T3: TCC i Uprawnienia - Dokumentacja

## Status: ✅ COMPLETED

Data: 2026-01-15
Autor: Agent Dev Team
Wersja: 1.0

---

## 1. Co to jest TCC?

**Transparency, Consent, and Control** - system uprawnień macOS kontrolujący dostęp aplikacji do:
- Danych użytkownika (Photos, Contacts, Calendar, Reminders, Notes)
- Funkcji systemowych (Automation, Accessibility, Full Disk Access)
- Sprzętu (Microphone, Camera, Bluetooth)

---

## 2. Przyznane uprawnienia

### Dla IDE (IDE developerskie)

| Aplikacja | Uprawnienie | Data przyznania | Status |
|-----------|-------------|-----------------|--------|
| Notes | Odczyt notatek | 2026-01-15 | ✅ |
| Reminders | Odczyt/zapis przypomnień | 2026-01-15 | ✅ |
| Calendar | Odczyt kalendarzy | 2026-01-15 | ✅ |

### Środowisko uruchomieniowe

```
Host: macOS 25.4.0 (Tahoe 26.4.1 oczekiwane)
Runtime: developer IDE (Electron)
TCC DB: ~/Library/Application Support/com.apple.TCC/TCC.db
```

---

## 3. Architektura bezpieczeństwa

### Model Least Privilege

```
┌─────────────────────────────────────────────────────────┐
│                    developer IDE                           │
│  ┌─────────────────┐  ┌─────────────────┐              │
│  │  AppleScript    │  │    MCP         │              │
│  │  Bridge         │  │  Servers       │              │
│  └────────┬────────┘  └────────┬────────┘              │
│           │                   │                        │
│           ▼                   ▼                        │
│  ┌─────────────────────────────────────────┐          │
│  │           TCC Permissions                │          │
│  │  • Notes (tylko odczyt)                 │          │
│  │  • Reminders (odczyt/zapis #AgentTodo)  │          │
│  │  • Calendar (tylko odczyt)               │          │
│  └─────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────┘
```

### Zasada minimalnych uprawnień

1. **Notes** - tylko odczyt (bez edycji treści)
2. **Reminders** - odczyt/zapis ZADAŃ z tagiem `#AgentTodo`
3. **Calendar** - tylko odczyt (bez tworzenia wydarzeń)

---

## 4. Ryzyka i mitigacje

| Ryzyko | Prawdopodobieństwo | Wpływ | Mitigacja |
|--------|-------------------|-------|-----------|
| Wyciek danych przez notatki | Niskie | Wysoki | Nie przechowywać sekretów w Notatkach |
| Nadmiarowe uprawnienia | Średnie | Wysoki | Ograniczyć do #AgentTodo |
| Cross-app scripting | Niskie | Wysoki | MCP scope isolation |

---

## 5. Testy weryfikacyjne

```bash
# T3.1: Test AppleScript
osascript -e 'tell application "Notes" to get name of notes where name starts with "P0 | "'

# T3.3: Test Reminders
osascript -e 'tell application "Reminders" to get name of list "OpenHands BMAD"'
osascript -e 'make new reminder in list "OpenHands BMAD" with properties {name:"TEST #AgentTodo"}'
```

---

## 6. Scenariusz odtworzenia (dla nowej maszyny)

### Krok 1: Otwórz System Settings
```bash
open "x-apple.systempreferences:com.apple.preference.security?Privacy_Automation"
```

### Krok 2: Znajdź IDE w Automation
```
Privacy & Security → Automation → IDE
```

### Krok 3: Dodaj uprawnienia
- [ ] ☑️ **Notes** - pozwól na odczyt
- [ ] ☑️ **Reminders** - pozwól na odczyt i zapis  
- [ ] ☑️ **Calendar** - pozwól na odczyt (opcjonalnie)

### Krok 4: Weryfikacja
```bash
python3 _bmad/mcp/t3_apple_script_test.py
```

---

## 7. Znane ograniczenia

1. **TCC nie jest dziedziczone** - każda aplikacja musi mieć własne uprawnienia
2. **Terminal nie ma uprawnień** - wymaga osobnej konfiguracji
3. **System Integrity Protection** - niektóre obszary są chronione

---

## 8. Następne kroki

- [ ] Faza 4: OpenHands MCP Integration
- [ ] Faza 5: Automatyzacja workflow

---

## 9. Kontakty wsparcia

W razie problemów:
1. Sprawdź logi: `~/Library/Logs/IDE/`
2. Reset TCC: `sudo tccutil reset all`
3. Dokumentacja: https://support.apple.com/en-us/HT210491