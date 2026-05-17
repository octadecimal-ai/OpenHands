**TL;DR** (stan na 2026-05-14, źródła preferencyjnie >2025-09):

- **Silny ekosystem** wokół GitHub, Linear, Jira/Atlassian, Cloudflare, Bitwarden i Notion – official MCP servers dostępne, często remote z OAuth.
- **Git lokalny i Docker** mają dobre reference/community serwery (TypeScript/Python). Łatwo wrapować CLI.
- **Bitwarden** ma oficjalny local-first MCP (CRITICAL – priorytet). 1Password nie eksponuje raw credentials via MCP (bezpieczeństwo).
- **Self-hosted (n8n, Grafana, Langfuse, Rocket.Chat, Twenty)** – głównie community lub wrap CLI/SDK; brak official w większości.
- **MVP unblockery**: GitHub + Linear/Jira + Git local + Bitwarden + Cloudflare/Docker + Slack/Discord + macOS/Notifications. Reszta w phase-2.

**Master inventory** (wybrane kluczowe; pełna tabela skrócona dla raportu):

**Integration** | **Official MCP?** | **Community MCP?** | **Maturity** | **License** | **Verdict**
--- | --- | --- | --- | --- | ---
**GitHub (issues, PRs, repos, code search)** | Tak, github/github-mcp-server (remote + local, Go) | Tak, wiele forków | Wysoka (aktywny, tysiące stars) | MIT/Apache-like | **Use official** (OAuth, rate limits managed)
**Linear** | Tak, mcp.linear.app (remote, OAuth 2.1) | Kilka (np. cline/linear-mcp) | Wysoka (official) | - | **Use official**
**Jira (Atlassian)** | Tak, Atlassian Rovo Remote MCP (Jira + Confluence) | sooperset/mcp-atlassian (~4.6k stars?) | Wysoka | - | **Use official Rovo**
**Git (local repo)** | Reference (modelcontextprotocol/servers) | cyanheads/git-mcp-server, kjozsa/git-mcp | Dobra | Open | **Use reference/community** (trivial wrap)
**Cloudflare (Workers, DNS, R2 etc.)** | Tak, cloudflare/mcp (Code Mode, ~2500 endpoints) + product-specific | Tak | Bardzo wysoka | - | **Use official** (token-efficient)
**OVH** | Brak | Brak | Niska | - | **Wrap CLI/SDK** lub custom (moderate)
**Docker** | Tak, Docker MCP Catalog + Toolkit (Hub servers) + community (ckreiling/mcp-server-docker) | Tak | Wysoka (Docker oficjalnie wspiera) | - | **Use Docker Catalog**
**Bitwarden** | Tak, bitwarden/mcp-server (local-first, CLI-based) | Kilka (Vaultwarden) | Wysoka | - | **Use official** (CRITICAL)
**1Password** | Brak raw credentials | Community (CakeRepository/1Password-MCP) | Średnia | - | **Skip raw lub community z ostrożnością** (polityka bezpieczeństwa)
**Wiki.js** | Brak | Kilka (talosdeus, heAdz0r, jaalbin24) – Python/TS | Średnia (community) | Open | **Community + wrap GraphQL** (moderate)
**Obsidian** | Brak | Wiele (cyanheads/obsidian-mcp-server via Local REST API) | Dobra | Open | **Community** (użyj Local REST plugin)
**Notion** | Tak, mcp.notion.com (remote, OAuth) | Starsze local | Wysoka | - | **Use official**
**n8n / Grafana / Langfuse / Rocket.Chat / Twenty** | Brak official | Community lub wrap (API/CLI) | Średnia/niska | Open | **Wrap / custom** (oceniaj na merits)
**macOS Notifications / Calendar / Mail / Notes / Reminders** | Brak | Community bridges (terminal-notifier etc.) | Średnia | - | **Wrap CLI / custom** (trivial-moderate)
**Slack** | Tak, mcp.slack.com (remote) | Community | Wysoka | - | **Use official**
**Discord** | Brak official | Kilka (v-3/discordmcp etc.) | Średnia | Open | **Community** (bot token)
**Telegram / Signal / KDE Connect** | Brak / ograniczone | Community | Niska-średnia | - | **Wrap CLI/SDK**
**Web search (Brave/Serper etc.), Reddit, HN, LinkedIn, X, Job boards** | Częściowo (Brave official) | Wiele search scrapers | Różna (rate limits) | - | **Używać dedykowanych + custom dla job boards**

**Źródła**: registry.modelcontextprotocol.io, github.com/modelcontextprotocol/servers, mcpservers.org, mcp.so, vendor blogs (2025-2026).

**Gap analysis – co MUST budować custom** (TypeScript preferowane):

- **OVH** – moderate (3-7 dni): wrap CLI/SDK (OVH API dobre).
- **macOS native full (Shortcuts, Activity Monitor)** – moderate: AppleScript/terminal-notifier bridge.
- **Self-hosted inventory bez API** (np. niektóre Twenty/Rocket.Chat) – moderate-hard.
- **Specyficzne job boards (Pracuj.pl, NoFluffJobs)** – hard (>1 tydzień) ze względu na scraping/rate limits.
- **Signal/KDE Connect full** – moderate-hard (end-to-end encryption).

**Effort ogólny**: Większość pokryta official/community → fokus na wrapperach i auth isolation.

**Critical-path MCPs dla MVP** (pierwsza działająca wersja multi-agent na automation assistant + Docker):

1. GitHub (repo/code/Issues/PRs)
2. Linear lub Jira (task management)
3. Git local + Docker (dev workflow)
4. Bitwarden (secrets – bezpieczeństwo)
5. Cloudflare (infra)
6. Slack/Discord lub Email/Notifications (comm)
7. Web search + Notion/Obsidian (knowledge)

To unblock core loop: observe → plan → act w repo/tasks/infra.

**Risk callouts**:

- Community one-person/abandoned: sprawdzaj last commit, stars, maintainer (np. starsze Wiki.js/Obsidian forks).
- **Credential handling**: Bitwarden official local-first OK; unikać serwerów eksponujących raw secrets. Używać per-agent isolation + OAuth gdzie możliwe. MCP isolation w multi-agent wymaga ostrożnej konfiguracji (shared vs per-agent creds).
- Rate limits: GitHub/Cloudflare/Linear – monitorować w 24/7 orchestrator (backoff, queuing).
- License: Wszystkie official/community top zazwyczaj MIT/Apache – pozwalają closed-source commercial.
- Abandoned: Starsze reference servers z github.com/modelcontextprotocol/servers (archived).

**Recommendation**:

- **Minimal MVP set**: Official GitHub + Linear/Jira + Bitwarden + Cloudflare + Git local + Docker Catalog + Slack + jeden search (Brave/Tavily). Używać Docker do hostowania community serwerów.
- **Phase-2**: OVH custom, pełny macOS, Wiki.js/Obsidian polish, self-hosted wrappers (n8n/Grafana na merits), job boards, Signal/KDE Connect.
- **Architektura**: TypeScript MCP servers, per-agent credential scoping, Docker isolation, monitoring via Langfuse/Grafana (istniejące). Testować w automation assistant, skupić się na auth security i rate-limit resilience.

**Cytowane źródła** (przykłady, dostęp 2026-05-14):
- https://github.com/modelcontextprotocol/servers
- https://github.com/github/github-mcp-server
- https://linear.app/changelog/2025-05-01-mcp
- https://bitwarden.com/blog/bitwarden-mcp-server/
- https://developers.cloudflare.com/.../mcp-servers-for-cloudflare/
- registry.modelcontextprotocol.io, mcp.so, mcpservers.org.

Raport gotowy do iteracji – ekosystem MCP ewoluuje tygodniowo.