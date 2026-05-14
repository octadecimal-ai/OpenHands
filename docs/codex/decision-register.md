# Decision Register

Ten plik jest skróconym rejestrem decyzji projektowych dla systemu multiagentów Octadecimal. Szczegółowy przebieg rozmów znajduje się w `docs/codex/conversation-log.md`, a obowiązujące zasady pracy w `docs/codex/working-rules.md`.

## D001 - Proces iteracyjnego doprecyzowania systemu

**Data:** 2026-05-14

**Status:** Accepted

**Decyzja:** Projekt będzie doprecyzowywany w krótkich epizodach: kontekst, pytania, analiza użytkownika, ustalenia, decyzje i następny krok. Wyniki rozmów będą zapisywane w `docs/codex/conversation-log.md`, a decyzje w `docs/codex/decision-register.md`.

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

**Decyzja:** Obowiązujące zasady pracy będą utrzymywane w jednym czytelnym pliku `docs/codex/working-rules.md`. Każdy nowy wątek musi zapoznać się z tym plikiem, logiem rozmów i rejestrem decyzji przed kontynuacją projektowania.

**Rationale:** Użytkownik chce, aby zasady były stabilnym, widocznym artefaktem, a nie wyłącznie fragmentem rozmowy. Zasady mają też mieć kontekst wynikający z poprzednich sesji.

**Konsekwencje:** Zmiany w `docs/codex/working-rules.md` są dopuszczalne przez ręczną edycję użytkownika albo przez Codex wyłącznie na wyraźne polecenie użytkownika. Codex nie powinien samodzielnie reinterpretować zasad bez zapisu w rejestrze decyzji.

**Źródła:** `docs/codex/conversation-log.md`

**Powiązane pytania:** Q002

## D004 - Dokumenty operacyjne Codex w katalogu docs/codex

**Data:** 2026-05-14

**Status:** Accepted

**Decyzja:** Dokumenty operacyjne Codex, czyli `working-rules.md`, `conversation-log.md` i `decision-register.md`, są utrzymywane w katalogu `docs/codex/`.

**Rationale:** Użytkownik przeniósł te pliki do osobnego katalogu, żeby oddzielić metadokumenty procesu Codex od pozostałego researchu i dokumentacji projektu.

**Konsekwencje:** Każdy nowy wątek powinien używać ścieżek `docs/codex/working-rules.md`, `docs/codex/conversation-log.md` i `docs/codex/decision-register.md`. Nowe decyzje i wpisy rozmów należy zapisywać w plikach pod `docs/codex/`, a nie bezpośrednio w `docs/`.

**Źródła:** `docs/codex/conversation-log.md`, `docs/codex/working-rules.md`

**Powiązane pytania:** Q003

## D005 - Indeks Codex i ignorowanie lokalnych artefaktów macOS

**Data:** 2026-05-14

**Status:** Accepted

**Decyzja:** Katalog `docs/codex/` otrzymuje własny `README.md` jako punkt wejścia dla użytkownika i kolejnych wątków. Repozytorium ignoruje `.DS_Store` przez `.gitignore`.

**Rationale:** Krótki indeks zmniejsza tarcie przy starcie nowego wątku i wskazuje właściwą kolejność czytania dokumentów. `.DS_Store` jest lokalnym artefaktem macOS i nie powinien trafiać do historii projektu.

**Konsekwencje:** Nowe wątki mogą zaczynać od `docs/codex/README.md`, a Git nie będzie pokazywał `.DS_Store` jako pliku do śledzenia. Zmiany w dokumentach operacyjnych nadal wymagają zapisu w logu i rejestrze decyzji.

**Źródła:** `docs/codex/README.md`, `.gitignore`

**Powiązane pytania:** Q004

## D006 - Baseline commit przed planowaniem MVP

**Data:** 2026-05-14

**Status:** Accepted

**Decyzja:** Przed rozpoczęciem Epizodu 001 należy wykonać pierwszy commit bazowy obejmujący obecny stan dokumentów projektu, dokumenty operacyjne Codex oraz `.gitignore`.

**Rationale:** Baseline commit daje czysty punkt odniesienia dla dalszej pracy i pozwala śledzić wszystkie kolejne zmiany w dokumentach projektowych.

**Konsekwencje:** Po commicie dalsze zmiany powinny być małe, opisane w logu i możliwe do sprawdzenia przez `git diff`. Następny etap to planowanie wizji pierwszego dokumentu projektowego.

**Źródła:** `docs/codex/conversation-log.md`, `docs/codex/working-rules.md`

**Powiązane pytania:** Q005
