# OpenHands Agent Memory - Octadecimal Multiagent System

## Obowiązkowy kontekst startowy

**PRZED ROZPOCZĘCIEM KAŻDEJ SESJI** agent MUSI przeczytać:

1. `docs/openhands/working-rules.md` - obowiązujące zasady pracy
2. `docs/openhands/conversation-log.md` - przebieg pytań, odpowiedzi i ustaleń
3. `docs/openhands/decision-register.md` - skrócony rejestr decyzji
4. Dokumenty źródłowe potrzebne do bieżącego tematu

**Po przeczytaniu kontekstu** agent powinien krótko powiedzieć, co jest aktualnym stanem ustaleń i jaki ma być następny mały krok.

## Zasady dokumentowania

### Rozmowy i ustalenia
- Wszystkie pytania i odpowiedzi zapisuj w `docs/openhands/conversation-log.md`
- Wszystkie decyzje zapisuj w `docs/openhands/decision-register.md` z numerem Dxxx, datą, statusem, rationale, konsekwencjami

### Sesje agentów
- Każda sesja z użytkownikiem jest rejestrowana w `docs/openhands/sessions/YYYYmmdd-HHiiSS-nazwa.md`

### Status zadań
- Raporty z Reminders zapisywane w `docs/openhands/tasks/YYYYmmdd-reminders-status.md`

## Zmiany w Working Rules

Plik `docs/openhands/working-rules.md` może zostać zmieniony tylko na dwa sposoby:
1. Użytkownik edytuje plik własnoręcznie
2. Agent edytuje plik na wyraźne polecenie użytkownika

Agent nie może samodzielnie zmieniać zasad pracy.

## Bezpieczeństwo

- Stara infrastruktura Octadecimal jest wyłączona z domyślnego kontekstu
- Nowy zespół projektujemy od zera, na miarę technologii i praktyk aktualnych na maj 2026
- Nie wdrażamy zmian w runtime, MCP, kontenerach ani istniejących zespołach bez osobnej decyzji