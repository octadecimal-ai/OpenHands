# Decision Register

Ten plik jest skróconym rejestrem decyzji projektowych dla systemu multiagentów Octadecimal. Szczegółowy przebieg rozmów znajduje się w `docs/openhands/conversation-log.md`, a obowiązujące zasady pracy w `docs/openhands/working-rules.md`.

## D001 - Proces iteracyjnego doprecyzowania systemu

**Data:** 2026-05-14

**Status:** Accepted

**Decyzja:** Projekt będzie doprecyzowywany w krótkich epizodach: kontekst, pytania, analiza użytkownika, ustalenia, decyzje i następny krok. Wyniki rozmów będą zapisywane w `docs/openhands/conversation-log.md`, a decyzje w `docs/openhands/decision-register.md`.

**Rationale:** Repo jest obecnie przede wszystkim dokumentacyjne, a decyzje architektoniczne wymagają stopniowego odsiewania wcześniejszego researchu od realnych ustaleń wdrożeniowych.

**Konsekwencje:** Każda runda pracy powinna kończyć się jasnym zapisem ustaleń. Decyzje nie powinny pozostawać wyłącznie w czacie.

**Źródła:** `README.md`, `CONTRIBUTING-to-analize-and-improve.md`, `docs/current-infrastructure.md`, `docs/governance-gemini-research.md`, `docs/scrum-perplexity-research.md`

**Powiązane pytania:** Q001

## D002 - Lokalne Git repo jako rejestr zmian w plikach

**Data:** 2026-05-14

**Status:** Accepted

**Decyzja:** Katalog projektu ma być lokalnym repozytorium Git, używanym do śledzenia zmian w dokumentach i przyszłych plikach projektowych.

**Rationale:** Użytkownik wskazał potrzebę repozytorium zmian w plikach. Git pasuje do przyjętego modelu `docs-as-code` i zasad atomowości, odwracalności oraz transparentności z `CONTRIBUTING-to-analize-and-improve.md`.

**Konsekwencje:** Przed i po istotnych zmianach należy sprawdzać status Git. Commit powinien być wykonywany tylko na wyraźne polecenie użytkownika lub zgodnie z później przyjętą zasadą.

**Źródła:** `CONTRIBUTING-to-analize-and-improve.md`

**Powiązane pytania:** Q002

## D003 - Working Rules jako obowiązkowy kontekst startowy

**Data:** 2026-05-14

**Status:** Accepted

**Decyzja:** Obowiązujące zasady pracy będą utrzymywane w jednym czytelnym pliku `docs/openhands/working-rules.md`. Każdy nowy wątek musi zapoznać się z tym plikiem, logiem rozmów i rejestrem decyzji przed kontynuacją projektowania.

**Rationale:** Użytkownik chce, aby zasady były stabilnym, widocznym artefaktem, a nie wyłącznie fragmentem rozmowy. Zasady mają też mieć kontekst wynikający z poprzednich sesji.

**Konsekwencje:** Zmiany w `docs/openhands/working-rules.md` są dopuszczalne przez ręczną edycję użytkownika albo przez OpenHands wyłącznie na wyraźne polecenie użytkownika. OpenHands nie powinien samodzielnie reinterpretować zasad bez zapisu w rejestrze decyzji.

**Źródła:** `docs/openhands/conversation-log.md`

**Powiązane pytania:** Q002

## D004 - Dokumenty operacyjne OpenHands w katalogu docs/openhands

**Data:** 2026-05-14

**Status:** Accepted

**Decyzja:** Dokumenty operacyjne OpenHands, czyli `working-rules.md`, `conversation-log.md` i `decision-register.md`, są utrzymywane w katalogu `docs/openhands/`.

**Rationale:** Użytkownik przeniósł te pliki do osobnego katalogu, żeby oddzielić metadokumenty procesu OpenHands od pozostałego researchu i dokumentacji projektu.

**Konsekwencje:** Każdy nowy wątek powinien używać ścieżek `docs/openhands/working-rules.md`, `docs/openhands/conversation-log.md` i `docs/openhands/decision-register.md`. Nowe decyzje i wpisy rozmów należy zapisywać w plikach pod `docs/openhands/`, a nie bezpośrednio w `docs/`.

**Źródła:** `docs/openhands/conversation-log.md`, `docs/openhands/working-rules.md`

**Powiązane pytania:** Q003

## D005 - Indeks OpenHands i ignorowanie lokalnych artefaktów macOS

**Data:** 2026-05-14

**Status:** Accepted

**Decyzja:** Katalog `docs/openhands/` otrzymuje własny `README.md` jako punkt wejścia dla użytkownika i kolejnych wątków. Repozytorium ignoruje `.DS_Store` przez `.gitignore`.

**Rationale:** Krótki indeks zmniejsza tarcie przy starcie nowego wątku i wskazuje właściwą kolejność czytania dokumentów. `.DS_Store` jest lokalnym artefaktem macOS i nie powinien trafiać do historii projektu.

**Konsekwencje:** Nowe wątki mogą zaczynać od `docs/openhands/README.md`, a Git nie będzie pokazywał `.DS_Store` jako pliku do śledzenia. Zmiany w dokumentach operacyjnych nadal wymagają zapisu w logu i rejestrze decyzji.

**Źródła:** `docs/openhands/README.md`, `.gitignore`

**Powiązane pytania:** Q004

## D006 - Baseline commit przed planowaniem MVP

**Data:** 2026-05-14

**Status:** Accepted

**Decyzja:** Przed rozpoczęciem Epizodu 001 należy wykonać pierwszy commit bazowy obejmujący obecny stan dokumentów projektu, dokumenty operacyjne OpenHands oraz `.gitignore`.

**Rationale:** Baseline commit daje czysty punkt odniesienia dla dalszej pracy i pozwala śledzić wszystkie kolejne zmiany w dokumentach projektowych.

**Konsekwencje:** Po commicie dalsze zmiany powinny być małe, opisane w logu i możliwe do sprawdzenia przez `git diff`. Następny etap to planowanie wizji pierwszego dokumentu projektowego.

**Źródła:** `docs/openhands/conversation-log.md`, `docs/openhands/working-rules.md`

**Powiązane pytania:** Q005

## D007 - Nowy zespół projektowany od zera i research zewnętrzny

**Data:** 2026-05-14

**Status:** Accepted

**Decyzja:** Nowy zespół multiagentów Octadecimal projektujemy od zera, na podstawie technologii i praktyk aktualnych na maj 2026. Stara infrastruktura i stare zespoły są wyłączone z domyślnego kontekstu; można włączać ich dokumentację tylko na wyraźne polecenie użytkownika. Prompty do researchu zapisujemy w `docs/openhands/questions-prompts/`, a wyniki researchu użytkownik umieszcza w `docs/openhands/research-files/`.

**Rationale:** Celem nie jest modernizacja istniejącego zespołu, tylko zaprojektowanie nowego systemu zgodnego z aktualnymi praktykami agentic software engineering, governance, izolacji i pracy z wieloma modelami.

**Konsekwencje:** OpenHands nie powinien używać `docs/current-infrastructure.md` jako domyślnego źródła wymagań lub ograniczeń. Następny etap to zebranie zewnętrznych materiałów porównawczych z repozytoriów, blogów, case studies, Reddita i dokumentacji projektów.

**Źródła:** `docs/openhands/conversation-log.md`, `docs/openhands/working-rules.md`, `docs/openhands/questions-prompts/`

**Powiązane pytania:** Q006

## D008 - Rozszerzenie OpenHands o sesje agentów, śledzenie zadań i integrację z wiedzą

**Data:** 2026-05-15

**Status:** Accepted

**Decyzja:** OpenHands zostaje rozszerzony o trzy nowe funkcjonalności:
1. **Rejestracja sesji agentów** - notatki z sesji, kto uczestniczył, co ustalono
2. **Śledzenie stanu zadań** - powiązanie z Reminders, status zadań w OpenHands
3. **Powiązanie z `knowledge-team.md`** - integracja wiedzy zespołowej z OpenHands

**Rationale:** Obecny OpenHands rejestruje tylko pytania i decyzje użytkownika. Brakuje śledzenia sesji agentskich (np. OpenHands, automation assistant), powiązania z systemem zadań (Reminders) oraz integracji z bazą wiedzy (`knowledge-team.md`). Te elementy są potrzebne do pełnej rejestracji pracy zespołu.

**Konsekwencje:** Należy zaprojektować format zapisu sesji agentskich, mechanizm powiązania z Reminders, oraz strukturę integracji z `knowledge-team.md`. Następny krok to przedyskutowanie konkretnego formatu rozszerzenia.

**Źródła:** Reminders `openhands-bmad-agents`, `docs/knowledge-team.md`

**Powiązane pytania:** Q007

## D009 - AGENTS.md jako mechanizm trwałego kontekstu

**Data:** 2026-05-15

**Status:** Accepted

**Decyzja:** Utworzono plik `AGENTS.md` w korzeniu repozytorium, który jest automatycznie ładowany na początku każdej sesji OpenHands. Plik zawiera obowiązkowy kontekst startowy, zasady dokumentowania oraz ograniczenia dotyczące zmian w Working Rules.

**Rationale:** Bez mechanizmu wymuszającego odczyt zasad, każda nowa sesja OpenHands zaczynałaby "od zera" i pomijała ustalenia z poprzednich sesji. AGENTS.md rozwiązuje problem resetu kontekstu.

**Konsekwencje:** Każda nowa sesja OpenHands automatycznie przeczyta AGENTS.md i z niego dowie się o obowiązkowym kontekście startowym. Zasady będą przestrzegane niezależnie od sesji.

**Źródła:** `AGENTS.md`, `docs/openhands/working-rules.md`

**Powiązane pytania:** Q008

## D010 - Plan AGILE dla zadania P0: Orchestracja multiagentów z macOS

**Data:** 2026-05-16

**Status:** Accepted

**Decyzja:** Stworzono kompletny plan AGILE dla zadania P0 obejmujący 6 epików, ~35 tasków technicznych, kryteria akceptacji, mapowanie faz BMAD na ekosystem macOS oraz ryzyka z mitigacjami. Plan zapisany w `docs/openhands/tasks/P0-Orchestracja-multiagentow-macOS-Plan.md`.

**Rationale:** Zadanie P0 wymaga systematycznego podejścia AGILE ze względu na złożoność integracji agentów z macOS. Plan obejmuje wszystkie kluczowe komponenty: MCP servers, TCC uprawnienia, Apple Reminders, Notes, Finder Tags oraz bezpieczeństwo.

**Konsekwencje:** Kolejne kroki to prezentacja planu użytkownikowi, zatwierdzenie zakresu, a następnie realizacja Fazy 1 (Setup środowiska MCP).

**Źródła:** Raporty researchu z `/Users/admin/Documents/Developer/Raports/Multi-agents systems/Gemini Deep Research/Integracja frameworków agentowych z macOS/`

**Powiązane pytania:** Q009

## D011 - Faza 1 UKOŃCZONA: Setup Środowiska

**Data:** 2026-05-16

**Status:** Accepted

**Decyzja:** Faza 1 (Setup Środowiska) została ukończona. Wszystkie 5 zadań technicznych wykonane pomyślnie.

**Wyniki:**
- Node.js v26.0.0 zainstalowany
- npm/npx v11.12.1 gotowe
- PATH bez zmian (wymagane katalogi już obecne)
- Katalog `_bmad/mcp/` utworzony
- Backup konfiguracji w `_bmad-output/backups/`

**Rapor:** `docs/openhands/tasks/P0-Faza1-Setup-Srodowiska-Raport.md`

**Następny krok:** Faza 2 - Instalacja i Konfiguracja MCP Servers

**Powiązane pytania:** Q010
