# Working Rules

Ten dokument opisuje obowiązujące zasady wspólnego doprecyzowania systemu multiagentów Octadecimal. Jest przeznaczony do czytania przez użytkownika i przez każdy nowy wątek Codex przed rozpoczęciem pracy.

## Obowiązkowy kontekst startowy

Każdy nowy wątek musi najpierw przeczytać:

1. `docs/codex/working-rules.md`
2. `docs/codex/conversation-log.md`
3. `docs/codex/decision-register.md`
4. Dokumenty źródłowe potrzebne do bieżącego tematu, zwykle `README.md`, `CONTRIBUTING-to-analize-and-improve.md` i odpowiednie pliki z `docs/`

Po przeczytaniu kontekstu Codex powinien krótko powiedzieć, co jest aktualnym stanem ustaleń i jaki ma być następny mały krok.

## Proces pracy

Pracujemy w krótkich epizodach projektowych:

1. `Kontekst` - Codex czyta wskazane dokumenty i podaje krótkie podsumowanie.
2. `Pytania` - Codex zadaje 1-3 konkretne pytania decyzyjne.
3. `Analiza użytkownika` - użytkownik dopowiada kontekst, priorytety i ograniczenia.
4. `Ustalenia` - Codex zapisuje pytania i odpowiedzi w `docs/codex/conversation-log.md`.
5. `Decyzje` - Codex zapisuje rozstrzygnięcia w `docs/codex/decision-register.md`.
6. `Następny krok` - Codex proponuje kolejny mały temat projektowy.

Jedna runda powinna dotyczyć jednego głównego tematu. Jeżeli temat zaczyna się rozlewać, Codex powinien zaproponować podział na osobne epizody.

## Komunikacja

Komunikaty Codex w trakcie pracy mają być krótkie i konkretne:

- co czyta lub sprawdza,
- czego się dowiedział,
- jaka decyzja jest potrzebna,
- co zostało zapisane.

Codex ma unikać dużych bloków naraz, jeśli lepsza jest seria małych kroków z decyzjami użytkownika.

## Dokumentowanie rozmów i decyzji

Wszystkie pytania i odpowiedzi z pracy nad projektowaniem systemu zapisujemy w `docs/codex/conversation-log.md`.

Wszystkie decyzje i ustalenia zapisujemy dodatkowo w `docs/codex/decision-register.md`, z numerem `Dxxx`, datą, statusem, rationale, konsekwencjami, źródłami i powiązanymi pytaniami.

Kontekst zasad również powinien być ustalany podczas wspólnej analizy z użytkownikiem i zapisywany w tych dokumentach.

## Zmiany w Working Rules

`docs/codex/working-rules.md` może zostać zmieniony tylko na dwa sposoby:

1. Użytkownik edytuje plik własnoręcznie.
2. Codex edytuje plik na wyraźne polecenie użytkownika.

Codex nie może samodzielnie zmieniać zasad pracy tylko dlatego, że uzna to za wygodne. Jeżeli pojawi się potrzeba zmiany zasad, Codex powinien zapytać użytkownika albo poczekać na wyraźne polecenie.

Każda istotna zmiana zasad powinna zostać odnotowana w `docs/codex/decision-register.md`.

## Git i historia zmian

Lokalne repozytorium Git jest rejestrem zmian w plikach projektu.

Zasady pracy z Git:

- przed większą zmianą Codex sprawdza status repo,
- po zmianie Codex sprawdza, jakie pliki zostały dodane lub zmienione,
- commit jest wykonywany tylko na wyraźne polecenie użytkownika albo zgodnie z później przyjętą decyzją,
- istniejących zmian użytkownika nie wolno cofać bez jego wyraźnej zgody.

## Bezpieczeństwo i zakres

Na tym etapie projektujemy system i proces. Nie wdrażamy jeszcze zmian w runtime, MCP, kontenerach ani istniejących zespołach.

Istniejące zespoły produkcyjne Claude Code opisane w `docs/current-infrastructure.md` są nietykalne, dopóki osobna decyzja nie dopuści migracji, eksperymentu albo audytu.

Dane z `docs/` traktujemy jako wcześniejszy research. Nie są automatycznie prawdą produkcyjną. Fakty zależne od aktualnego stanu rynku, narzędzi, cen lub bezpieczeństwa trzeba weryfikować przed decyzjami wdrożeniowymi.

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
