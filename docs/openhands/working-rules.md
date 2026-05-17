# Working Rules

Ten dokument opisuje obowiązujące zasady wspólnego doprecyzowania systemu multiagentów Octadecimal. Jest przeznaczony do czytania przez użytkownika i przez agenta OpenHands przed rozpoczęciem pracy.

## Obowiązkowy kontekst startowy

Każdy nowy wątek musi najpierw przeczytać:

1. `docs/openhands/working-rules.md` (ten plik)
2. `docs/openhands/conversation-log.md`
3. `docs/openhands/decision-register.md`
4. Dokumenty źródłowe potrzebne do bieżącego tematu, zwykle `README.md`, `CONTRIBUTING-to-analize-and-improve.md` i odpowiednie pliki z `docs/`

Po przeczytaniu kontekstu agent powinien krótko powiedzieć, co jest aktualnym stanem ustaleń i jaki ma być następny mały krok.

## Proces pracy

Pracujemy w krótkich epizodach projektowych:

1. `Kontekst` - agent czyta wskazane dokumenty i podaje krótkie podsumowanie.
2. `Pytania` - agent zadaje 1-3 konkretne pytania decyzyjne.
3. `Analiza użytkownika` - użytkownik dopowiada kontekst, priorytety i ograniczenia.
4. `Ustalenia` - agent zapisuje pytania i odpowiedzi w `docs/openhands/conversation-log.md`.
5. `Decyzje` - agent zapisuje rozstrzygnięcia w `docs/openhands/decision-register.md`.
6. `Następny krok` - agent proponuje kolejny mały temat projektowy.

Jedna runda powinna dotyczyć jednego głównego tematu. Jeżeli temat zaczyna się rozlewać, agent powinien zaproponować podział na osobne epizody.

## Komunikacja

Komunikaty agenta w trakcie pracy mają być krótkie i konkretne:

- co czyta lub sprawdza,
- czego się dowiedział,
- jaka decyzja jest potrzebna,
- co zostało zapisane.

Agent ma unikać dużych bloków naraz, jeśli lepsza jest seria małych kroków z decyzjami użytkownika.

## Dokumentowanie rozmów i decyzji

Wszystkie pytania i odpowiedzi z pracy nad projektowaniem systemu zapisujemy w `docs/openhands/conversation-log.md`.

Wszystkie decyzje i ustalenia zapisujemy dodatkowo w `docs/openhands/decision-register.md`, z numerem `Dxxx`, datą, statusem, rationale, konsekwencjami, źródłami i powiązanymi pytaniami.

Kontekst zasad również powinien być ustalany podczas wspólnej analizy z użytkownikiem i zapisywany w tych dokumentach.

## Zmiany w Working Rules

`docs/openhands/working-rules.md` może zostać zmieniony tylko na dwa sposoby:

1. Użytkownik edytuje plik własnoręcznie.
2. Agent edytuje plik na wyraźne polecenie użytkownika.

Agent nie może samodzielnie zmieniać zasad pracy tylko dlatego, że uzna to za wygodne. Jeżeli pojawi się potrzeba zmiany zasad, agent powinien zapytać użytkownika albo poczekać na wyraźne polecenie.

Każda istotna zmiana zasad powinna zostać odnotowana w `docs/openhands/decision-register.md`.

## Git i historia zmian

Lokalne repozytorium Git jest rejestrem zmian w plikach projektu.

Zasady pracy z Git:

- przed większą zmianą agent sprawdza status repo,
- po zmianie agent sprawdza, jakie pliki zostały dodane lub zmienione,
- commit jest wykonywany tylko na wyraźne polecenie użytkownika albo zgodnie z później przyjętą decyzją,
- istniejących zmian użytkownika nie wolno cofać bez jego wyraźnej zgody.

## Bezpieczeństwo i zakres

Na tym etapie projektujemy system i proces. Nie wdrażamy jeszcze zmian w runtime, MCP, kontenerach ani istniejących zespołach.

Istniejące zespoły produkcyjne Claude Code opisane w `docs/current-infrastructure.md` są nietykalne, dopóki osobna decyzja nie dopuści migracji, eksperymentu albo audytu.

Stara infrastruktura Octadecimal jest wyłączona z domyślnego kontekstu projektowania nowego zespołu. Agent nie powinien używać `docs/current-infrastructure.md` ani dokumentacji starej infrastruktury jako źródła wymagań, ograniczeń lub wzorca architektury, chyba że użytkownik wyraźnie poprosi o włączenie konkretnego fragmentu.

Nowy zespół projektujemy od zera, na miarę technologii i praktyk aktualnych na maj 2026. Dopuszczalne jest wzorowanie się na projektach, repozytoriach, blogach, case studies i dyskusjach innych developerów budujących podobne systemy z użyciem najnowszych narzędzi.

Dane z `docs/` traktujemy jako wcześniejszy research. Nie są automatycznie prawdą produkcyjną. Fakty zależne od aktualnego stanu rynku, narzędzi, cen lub bezpieczeństwa trzeba weryfikować przed decyzjami wdrożeniowymi.

## Research zewnętrzny

Prompty do ręcznego researchu zapisywane są w `docs/openhands/questions-prompts/`.

Nazwa pliku prompta ma format:

`YYYYmmdd-HHiiSS-temat-zapytania.md`

Wyniki researchu użytkownik zapisuje w `docs/openhands/research-files/`. Po dostarczeniu wyników agent analizuje je, wyciąga ustalenia, aktualizuje log rozmowy i proponuje decyzje do `docs/openhands/decision-register.md`.

## Proponowana kolejność epizodów

1. Wizja MVP i granice systemu.
2. Role agentów i odpowiedzialności zespołów.
3. Runtime i izolacja: Docker, Apple `container`, hybryda.
4. Governance, uprawnienia, eskalacje i human approval.
5. Warstwa wiedzy: pamięć osobista, projektowa, zespołowa, firmowa.
6. Integracje MCP i priorytety wdrożenia.
7. Komunikacja z founderem i kanały alertów.
8. Observability, koszty, logi, replay sesji.
9. Backlog MVP: epiki, story, kryteria akceptacji.
10. Plan pierwszego PoC.

## Rozszerzenie OpenHands (D008)

System OpenHands został rozszerzony o trzy nowe funkcjonalności:

### 1. Rejestracja sesji agentów

Sesje z agentami (OpenHands, Claude Code, inne) są rejestrowane w `docs/openhands/sessions/`. Każda sesja otrzymuje własny plik z:
- Datą i czasem sesji
- Uczestnikami (agent, użytkownik)
- Celem sesji
- Kluczowymi ustaleniami
- Referencjami do plików/projektów

Format pliku sesji: `YYYYmmdd-HHiiSS-agent-nazwa.md`

### 2. Śledzenie stanu zadań

Agent może odczytywać zadania z Reminders (lista `openhands-bmad-agents`) i powiązywać je z kontekstem projektu. W `docs/openhands/tasks/` utrzymujemy raporty ze statusem zadań.

Format: `YYYYmmdd-reminders-status.md` - raport z danego dnia.

### 3. Integracja z knowledge-team

Powiązanie dokumentacji OpenHands z `docs/knowledge-team.md`. Gdy agent podejmuje decyzję dotyczącą wiedzy zespołowej, informacja jest propagowana do odpowiednich plików.

Pliki z `docs/knowledge-team.md` są włączane do kontekstu OpenHands przy okazji tematów dotyczących zarządzania wiedzą.
