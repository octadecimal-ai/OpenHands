# Prompt: bezpieczeństwo i governance agentów kodujących

Użyj tego prompta w modelu LLM z dostępem do internetu.

## Zadanie

Zrób research aktualnych ryzyk bezpieczeństwa, governance i kontroli autonomicznych agentów kodujących oraz multi-agent software engineering systems.

Interesują mnie mechanizmy, które powinny znaleźć się w pierwszej architekturze nowego zespołu Octadecimal, zanim powstaną realne integracje z sekretami, repozytoriami klientów, Cloudflare, OVH, pocztą lub komunikatorami.

## Źródła startowe

Sprawdź między innymi:

- OWASP Agentic AI / Agentic Top 10, jeśli dostępne.
- Ataki prompt injection na coding agents i GitHub PR workflows.
- MCP security advisories z 2025-2026.
- Sandboxy: Docker, devcontainers, Coder workspaces, OpenHands runtime, GitHub agent sessions.
- Human approval patterns, policy engines, audit logs, least privilege, secret isolation.
- https://venturebeat.com/security/ai-agent-runtime-security-system-card-audit-comment-and-control-2026
- https://www.openhands.dev/blog/openhands-enterprise-agent-control-plane
- https://coder.com/blog/introducing-coder-agents

Dodaj źródła pierwotne, jeśli znajdziesz: dokumentacje vendorów, advisories, papers, GitHub issues, security writeups.

## Format odpowiedzi

Zwróć wynik w Markdown:

1. `Threat model summary` - najważniejsze klasy ryzyk.
2. `Controls` - tabela: ryzyko, kontrola, gdzie wdrożyć, koszt/złożoność, priorytet MVP.
3. `Secrets` - wzorce bezpiecznego użycia Bitwarden/secret managerów przez agentów.
4. `MCP` - jak bezpiecznie uruchamiać i ograniczać MCP serwery.
5. `Human approval` - które akcje wymagają człowieka.
6. `Auditability` - jakie logi i dowody muszą istnieć.
7. `Minimum viable governance` - najmniejszy zestaw zasad dla pierwszego PoC.

Nie zakładaj zaufania do agenta ani do zewnętrznego MCP servera.
