# Prompt: repozytoria agentic coding i multi-agent software engineering

Użyj tego prompta w wybranym modelu LLM z dostępem do internetu.

## Zadanie

Zrób research aktualnych repozytoriów open source i publicznych projektów z lat 2025-2026, które pokazują praktyczne podejścia do budowy zespołów agentów AI dla software engineering.

Interesują mnie zwłaszcza:

- multi-agent coding teams,
- Claude Code / OpenHands / OpenHands / Coder Agents / GitHub coding agents,
- orkiestracja przez Git issues, worktrees, pull requests, kolejki zadań,
- role typu planner, implementer, reviewer, tester, security reviewer, knowledge curator,
- mechanizmy izolacji, logowania, kontroli kosztów, human approval,
- projekty, które można realnie sklonować, przeczytać i potraktować jako wzorzec architektury.

## Źródła startowe

Sprawdź między innymi:

- https://github.com/topics/agentic-coding
- https://github.com/All-Hands-AI/OpenHands
- https://www.openhands.dev/blog/openhands-enterprise-agent-control-plane
- https://coder.com/blog/introducing-coder-agents
- https://github.com/newsroom/press-releases/coding-agent-for-github-copilot
- https://arxiv.org/abs/2604.14228

Dodaj też własne źródła znalezione podczas researchu.

## Format odpowiedzi

Zwróć wynik w Markdown:

1. `TL;DR` - 5-8 najważniejszych wniosków.
2. `Top repositories` - tabela: nazwa, URL, stars/aktywność jeśli dostępne, stack, model pracy, co warto skopiować, czerwone flagi.
3. `Architecture patterns` - powtarzające się wzorce.
4. `Anti-patterns` - czego nie kopiować.
5. `Najlepsze kandydaty do głębokiej analizy` - 5-10 pozycji.
6. `Pytania dla Octadecimal` - decyzje, które trzeba podjąć po lekturze.

Nie streszczaj marketingu. Szukaj praktycznych mechanizmów, plików konfiguracyjnych, przepływów pracy i ograniczeń.
