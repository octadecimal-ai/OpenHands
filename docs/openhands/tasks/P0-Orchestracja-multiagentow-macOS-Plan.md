# Plan AGILE: P0 - Orchestracja Multiagentów z Wykorzystaniem macOS

**Projekt:** Octadecimal Multi-Agent System  
**Zadanie:** P0 | Orchestracja multiagentów z wykorzystaniem macOS  
**Data utworzenia:** 2026-05-16  
**Status:** Do zatwierdzenia  
**Źródło:** `/Users/admin/Documents/Developer/Raports/Multi-agents systems/Gemini Deep Research/Integracja frameworków agentowych z macOS/`

---

## 1. CEL BIZNESOWY (Business Goal)

Stworzenie systemu orkiestracji multiagentowej, który wykorzystuje natywny ekosystem macOS (Finder Tags, Reminders, Notes) jako warstwę zarządzania kontekstem i zadaniami. System ma umożliwić agentom (OpenHands + BMAD) płynną współpracę z systemem operacyjnym bez barier kontenerowych.

---

## 2. ZAKRES (Scope)

### W zakresie (In Scope)
- [ ] Integracja agentów z Apple Reminders (kolejka zadań / Message Bus)
- [ ] Integracja agentów z Apple Notes (wspólna baza wiedzy)
- [ ] Integracja z Finder Tags (xattr / Spotlight) - stan zasobów i filtry RAG
- [ ] Konfiguracja protokołu MCP dla macOS
- [ ] Serwer MCP dla macOS (natywne API / AppleScript)
- [ ] Bezpieczna komunikacja agent ↔ macOS (TCC uprawnienia)
- [ ] Rozwiązanie wyścigów (Race Conditions) przy jednoczesnej modyfikacji zasobów
- [ ] Mapowanie faz BMAD na ekosystem macOS

### Poza zakresem (Out of Scope)
- Uruchamianie modeli LLM lokalnie (Ollama/MLX)
- Automatyzacja GUI trzecich aplikacji (OSWorld/Vision)
- Migracja istniejącej infrastruktury produkcyjnej
- Wdrożenie produkcyjne (etap Proof of Concept)

---

## 3. EPIKI (Epics)

### Epic 1: Architektura MCP dla macOS
**Cel:** Zbudowanie niezawodnej warstwy komunikacyjnej między agentami a systemem macOS

**Historyjki:**
- E1-US1: Wybór i instalacja oficjalnych serwerów MCP (filesystem, apple-events)
- E1-US2: Weryfikacja bezpieczeństwa przez MCP Inspector
- E1-US3: Konfiguracja TCC uprawnień dla Terminal/OpenHands
- E1-US4: Test komunikacji stdio między OpenHands a MCP Server

### Epic 2: Integracja Apple Reminders
**Cel:** Wykorzystanie Reminders jako zdecentralizowanej kolejki zadań dla agentów

**Historyjki:**
- E2-US1: Narzędzie do odczytu zadań z tagami (#AgentTodo, #ToExecute)
- E2-US2: Narzędzie do tworzenia i aktualizacji zadań z poziomu agenta
- E2-US3: Mechanizm heartbeat (selektywne sprawdzanie co X sekund)
- E2-US4: Synchronizacja statusu między agentami przez Reminders

### Epic 3: Integracja Apple Notes
**Cel:** Wykorzystanie Notes jako persistent knowledge graph dla agentów

**Historyjki:**
- E3-US1: Odczyt notatek z tagami kategoryzacyjnymi (#SprintContext)
- E3-US2: Zapis wniosków i artefaktów do Notatek
- E3-US3: Przeszukiwanie struktury folderów notatek
- E3-US4: Dostarczanie kontekstu historycznego nowo powołanym agentom

### Epic 4: Integracja Finder Tags (xattr/Spotlight)
**Cel:** Dynamiczne zarządzanie kontekstem przez tagowanie plików

**Historyjki:**
- E4-US1: Narzędzie do wyszukiwania plików po tagach (mdfind)
- E4-US2: Narzędzie do automatycznego tagowania plików (xattr)
- E4-US3: Implementacja file-level locking dla zapobiegania wyścigom
- E4-US4: Mapowanie tagów na filtry RAG dla agentów

### Epic 5: Mapowanie BMAD na macOS
**Cel:** Użycie 4 faz BMAD jako ramy dla workflow agentów

**Historyjki:**
- E5-US1: Analysis → Notatki z tagiem #bmad-prd
- E5-US2: Planning → Reminders z tagiem #bmad-tasks
- E5-US3: Solutioning → Pliki architektury z tagiem #bmad-arch
- E5-US4: Implementation → Workspace + aktualizacja Reminders

### Epic 6: Bezpieczeństwo i Izolacja
**Cel:** Zapewnienie bezpiecznej komunikacji przy zachowaniu funkcjonalności

**Historyjki:**
- E6-US1: Audyt kodu serwerów MCP (5-minutowy przegląd)
- E6-US2: Konfiguracja sandbox dla agentów (TCC)
- E6-US3: Ochrona przed nieautoryzowanym dostępem do AppleScript
- E6-US4: Testowanie scenariuszy odmowy dostępu

---

## 4. HISTORYJKI UŻYTKOWNIKA (User Stories)

### E1-US1: Wybór i instalacja oficjalnych serwerów MCP
```
JAKO: Administrator systemu
CHCĘ: Zainstalować sprawdzone serwery MCP dla macOS
ABY: Zapewnić bezpieczną i stabilną komunikację agentów z systemem

Kryteria akceptacji:
- [ ] Zainstalowany @modelcontextprotocol/server-filesystem z ograniczeniem do katalogu projektu
- [ ] Zainstalowany mcp-server-apple-events (FradSer) dla Reminders
- [ ] Dostępne narzędzia: macos_search_tags, macos_create_reminder, macos_read_note
- [ ] Konfiguracja widoczna w dokumentacji projektu
```

### E2-US2: Narzędzie do tworzenia zadań z poziomu agenta
```
JAKO: Agent orkiestrator
CHCĘ: Tworzyć zadania w Apple Reminders z odpowiednimi tagami
ABY: Delegować pracę do wyspecjalizowanych agentów

Kryteria akceptacji:
- [ ] Agent może utworzyć reminder: "Zrecenzuj kod w pliku X" z tagiem #DevAgent
- [ ] Reminder pojawia się natychmiast w systemie
- [ ] Agent może ustawić własny tag na reminderze
- [ ] Błąd uprawnień TCC zwraca czytelny komunikat
```

### E3-US2: Zapis wniosków do Notatek
```
JAKO: Agent analityczny
CHCĘ: Zapisywać wnioski i decyzje do Apple Notes
ABY: Budować wspólną bazę wiedzy zespołu

Kryteria akceptacji:
- [ ] Agent może utworzyć notatkę z tagiem #bmad-prd
- [ ] Notatki są dostępne z poziomu użytkownika w aplikacji Notes
- [ ] Kolejny agent może odczytać notatki i uzyskać kontekst historyczny
- [ ] Struktura folderów jest zgodna z konwencją BMAD
```

### E4-US3: File-level locking
```
JAKO: System orkiestracji
CHCĘ: Zapobiegać jednoczesnej modyfikacji tagów tego samego pliku
ABY: Unikać nadpisywania stanów i utraty danych

Kryteria akceptacji:
- [ ] Gdy Agent-A modyfikuje tagi pliku X, Agent-B czeka
- [ ] Lock jest zwalniany po zakończeniu operacji
- [ ] Timeout lock zwalnia po 30 sekundach bez odpowiedzi
- [ ] Logi pokazują historię lock/unlock dla debugowania
```

---

## 5. ZADANIA TECHNICZNE (Technical Tasks)

### Faza 1: Setup Środowiska
| ID | Zadanie | Estymata | Priorytet |
|----|---------|----------|-----------|
| T1.1 | Instalacja Node.js (jeśli brak) | 15 min | P0 |
| T1.2 | Instalacja npx i sprawdzenie wersji | 5 min | P0 |
| T1.3 | Konfiguracja PATH dla globalnych pakietów | 10 min | P1 |
| T1.4 | Utworzenie katalogu dla serwerów MCP | 5 min | P0 |
| T1.5 | Backup obecnej konfiguracji OpenHands | 10 min | P1 |

### Faza 2: Instalacja i Konfiguracja MCP Servers
| ID | Zadanie | Estymata | Priorytet |
|----|---------|----------|-----------|
| T2.1 | Instalacja @modelcontextprotocol/server-filesystem | 10 min | P0 |
| T2.2 | Konfiguracja filesystem server z ścieżką projektu | 15 min | P0 |
| T2.3 | Instalacja mcp-server-apple-events | 15 min | P0 |
| T2.4 | Test MCP Inspector dla obu serwerów | 30 min | P0 |
| T2.5 | Dokumentacja konfiguracji w projekcie | 20 min | P1 |

### Faza 3: Konfiguracja TCC i Uprawnień
| ID | Zadanie | Estymata | Priorytet |
|----|---------|----------|-----------|
| T3.1 | Uruchomienie testowego AppleScript | 10 min | P0 |
| T3.2 | Przyznanie uprawnień w System Preferences | 15 min | P0 |
| T3.3 | Test komunikacji Reminders z Terminal | 15 min | P0 |
| T3.4 | Dokumentacja kroków TCC | 20 min | P1 |
| T3.5 | Scenariusz odtworzenia uprawnień | 15 min | P2 |

### Faza 4: Narzędzia CLI dla Agentów
| ID | Zadanie | Estymata | Priorytet |
|----|---------|----------|-----------|
| T4.1 | Wrapper mdfind dla tagów | 30 min | P0 |
| T4.2 | Wrapper xattr dla zapisu tagów | 30 min | P0 |
| T4.3 | Wrapper osascript dla Reminders | 45 min | P0 |
| T4.4 | Wrapper osascript dla Notes | 45 min | P1 |
| T4.5 | Implementacja file-level locking | 60 min | P1 |

### Faza 5: Konfiguracja OpenHands z MCP
| ID | Zadanie | Estymata | Priorytet |
|----|---------|----------|-----------|
| T5.1 | Aktualizacja config OpenHands (mcp_tools) | 20 min | P0 | ✅ 2026-05-17 |
| T5.2 | Test połączenia z macOS MCP Server | 30 min | P0 | ✅ 2026-05-17 |
| T5.3 | Walidacja wszystkich narzędzi | 45 min | P0 | ✅ 2026-05-17 |
| T5.4 | Dokumentacja integracji | 30 min | P1 | ✅ 2026-05-17 |

### Faza 6: Testy Integracyjne
| ID | Zadanie | Estymata | Priorytet |
|----|---------|----------|-----------|
| T6.1 | Test: Agent tworzy reminder | 15 min | P0 |
| T6.2 | Test: Agent odczytuje notatki | 15 min | P0 |
| T6.3 | Test: Agent taguje plik | 15 min | P0 |
| T6.4 | Test: wielu agentów jednocześnie | 30 min | P1 |
| T6.5 | Test: obsługa błędu TCC | 15 min | P0 |

### Faza 7: Optymalizacja Apple Silicon
| ID | Zadanie | Estymata | Priorytet |
|----|---------|----------|-----------|
| T7.1 | Konfiguracja heartbeat interval | 15 min | P1 |
| T7.2 | Monitorowanie Unified Memory | 20 min | P2 |
| T7.3 | Optymalizacja pod Apple Silicon | 30 min | P2 |

---

## 6. KRYTERIA AKCEPTACJI (Acceptance Criteria)

### AC1: Serwery MCP działają
```
GIVEN: Fresh install OpenHands
WHEN: Agent wywołuje narzędzie MCP (np. macos_search_tags)
THEN: Otrzymuje poprawny wynik z macOS
AND: Czas odpowiedzi < 2 sekundy
```

### AC2: Bezpieczeństwo TCC
```
GIVEN: Nowa instalacja
WHEN: Agent próbuje uzyskać dostęp do Reminders
THEN: System wyświetla monit TCC
AND: Po akceptacji, dostęp działa
AND: Po odrzuceniu,返回 błąd uprawnień
```

### AC3: Kolejka zadań przez Reminders
```
GIVEN: Agent orkiestrator
WHEN: Tworzy reminder z tagiem #ToExecute
THEN: Dedykowany agent widzi zadanie
AND: Po wykonaniu, może oznaczyć jako ukończone
AND: Powiadamia orkiestratora
```

### AC4: Wiedza w Notatkach
```
GIVEN: Agent kończy pracę
WHEN: Zapisuje wnioski do Apple Notes
THEN: Notatki są widoczne w aplikacji
AND: Kolejny agent może je odczytać
AND: Kontekst jest zachowany między sesjami
```

### AC5: Tagowanie plików
```
GIVEN: Agent generuje artefakt
WHEN: Taguje plik jako #ReadyForQA
THEN: mdfind znajduje plik po tagu
AND: Inny agent może wyszukać po tym samym tagu
AND: Race condition jest obsługiwany
```

---

## 7. MAPOWANIE NA BMAD (BMAD Phases)

| Faza BMAD | Artefakt | Lokalizacja macOS | Narzędzia |
|-----------|----------|-------------------|-----------|
| **Analysis** | PRD / Project Brief | Apple Notes (#bmad-prd) | mcp_read_note |
| **Planning** | User Stories | Apple Reminders (#bmad-tasks) | mcp_create_reminder |
| **Solutioning** | Architecture | System plików + Tags (#bmad-arch) | mdfind, xattr |
| **Implementation** | Kod źródłowy | Workspace + Reminders (#in-progress) | mcp_update_reminder |

---

## 8. RYZYKA I MITIGACJE (Risks)

| ID | Ryzyko | Prawdopodobieństwo | Wpływ | Mitigacja |
|----|--------|-------------------|-------|-----------|
| R1 | TCC blokuje AppleScript | Wysokie | Wysoki | Szkolenie użytkownika + dokumentacja |
| R2 | Wyścigi przy jednoczesnych tagach | Średnie | Średni | File-level locking |
| R3 | Nadmierne obciążenie pamięci | Niskie | Średni | Heartbeat zamiast ciągłego polling |
| R4 | Niestabilność community MCP | Niskie | Wysoki | Fallback na czysty AppleScript |
| R5 | Inkompatybilność z Docker | Średnie | Wysoki | Test na macOS Tahoe / host-native |

---

## 9. DEFINICJA GOTOWOŚCI (Definition of Ready)

Zadanie jest GOTOWE do pracy gdy:
- [ ] Istnieje clear User Story z kryteriami akceptacji
- [ ] Zależności od innych zadań są zidentyfikowane
- [ ] Estymata jest przypisana
- [ ] Definition of Done jest zdefiniowana

---

## 10. DEFINICJA UKOŃCZENIA (Definition of Done)

Zadanie jest UKOŃCZONE gdy:
- [ ] Kod/narzędzie zostały napisane
- [ ] Testy manualne przeszły (według AC)
- [ ] Dokumentacja została zaktualizowana
- [ ] Commit został wykonany (jeśli wymagane)
- [ ] Kryteria akceptacji są spełnione

---

## 11. BACKLOG MVP (Prioritized)

| Priorytet | ID | Opis |
|-----------|----|------|
| P0 | T1.1-T1.4 | Setup środowiska MCP |
| P0 | T2.1-T2.4 | Instalacja i weryfikacja serwerów MCP |
| P0 | T3.1-T3.3 | Konfiguracja TCC |
| P0 | T4.1-T4.3 | Podstawowe wrappery CLI |
| P0 | T5.1-T5.3 | Konfiguracja OpenHands z MCP |
| P0 | T6.1-T6.3 | Podstawowe testy integracyjne |
| P1 | T4.4-T4.5 | Wrapper Notes + file locking |
| P1 | E4-E6 | Testy wielu agentów |
| P2 | T7.1-T7.3 | Optymalizacja Apple Silicon |

---

## 12. NASTĘPNE KROKI

1. ✅ Analiza zadania i research
2. ⬜ Prezentacja planu użytkownikowi
3. ⬜ Zatwierdzenie / modyfikacja zakresu
4. ⬜ Przystąpienie do Fazy 1 (Setup środowiska)
5. ⬜ Sprint 1: MCP Servers setup

---

## Źródła

- `Integracja macOS i frameworków agentowych.docx`
- `BMAD i MCP.docx`
- `Bezpieczenstwo MCP na macOS.docx`
- `Kontenery w macOS, pytanie o warstwę pośrednią.docx`
- `OpenHands + BMAD, czy jest dobrym wyborem w macOS.docx`
- `Przykład flow agenta w macOS.xlsx`