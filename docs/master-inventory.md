# Master inventory (wybrane kluczowe; pełna tabela skrócona dla raportu)

| Integration | Official MCP? | Community MCP? | Maturity | License | Verdict |
| --- | --- | --- | --- | --- | --- |
| **GitHub** (issues, PRs, repos, code search) | Tak, github/github-mcp-server (remote + local, Go) | Tak, wiele forków | Wysoka (aktywny, tysiące stars) | MIT/Apache-like | **Use official** (OAuth, rate limits managed) |
| **Linear** | Tak, mcp.linear.app (remote, OAuth 2.1) | Kilka (np. cline/linear-mcp) | Wysoka (official) | — | **Use official** |
| **Jira (Atlassian)** | Tak, Atlassian Rovo Remote MCP (Jira + Confluence) | sooperset/mcp-atlassian (~4.6k stars?) | Wysoka | — | **Use official Rovo** |
| **Git** (local repo) | Reference (modelcontextprotocol/servers) | cyanheads/git-mcp-server, kjozsa/git-mcp | Dobra | Open | **Use reference/community** (trivial wrap) |
| **Cloudflare** (Workers, DNS, R2 etc.) | Tak, cloudflare/mcp (Code Mode, ~2500 endpoints) + product-specific | Tak | Bardzo wysoka | — | **Use official** (token-efficient) |
| **OVH** | Brak | Brak | Niska | — | **Wrap CLI/SDK** lub custom (moderate) |
| **Docker** | Tak, Docker MCP Catalog + Toolkit (Hub servers) + community (ckreiling/mcp-server-docker) | Tak | Wysoka (Docker oficjalnie wspiera) | — | **Use Docker Catalog** |
| **Bitwarden** | Tak, bitwarden/mcp-server (local-first, CLI-based) | Kilka (Vaultwarden) | Wysoka | — | **Use official** (CRITICAL) |
| **Wiki.js** | Brak | Kilka (talosdeus, heAdz0r, jaalbin24) – Python/TS | Średnia (community) | Open | **Community + wrap GraphQL** (moderate) |
| **Obsidian** | Brak | Wiele (cyanheads/obsidian-mcp-server via Local REST API) | Dobra | Open | **Community** (użyj Local REST plugin) |
| **Notion** | Tak, mcp.notion.com (remote, OAuth) | Starsze local | Wysoka | — | **Use official** |
| **n8n / Grafana / Langfuse / Rocket.Chat / Twenty** | Brak official | Community lub wrap (API/CLI) | Średnia/niska | Open | **Wrap / custom** (oceniaj na merits) |
| **macOS Notifications / Calendar / Mail / Notes / Reminders** | Brak | Community bridges (terminal-notifier etc.) | Średnia | — | **Wrap CLI / custom** (trivial-moderate) |
| **Discord** | Brak official | Kilka (v-3/discordmcp etc.) | Średnia | Open | **Community** (bot token) |
| **KDE Connect** | Brak / ograniczone | Community | Niska-średnia | — | **Wrap CLI/SDK** |
| **Web search** (Brave/Serper etc.), Reddit, HN, LinkedIn, X, Job boards | Częściowo (Brave official) | Wiele search scrapers | Różna (rate limits) | — | — |
