# Rekonesans ekosystemu MCP dla platformy multi-agent na automation assistant + Docker (maj 2026)

## TL;DR

- **Ekosystem MCP w maju 2026 jest dojrzały dla integracji infrastrukturalnych i fragmentaryczny dla komunikacyjno-osobistych.** Większość kluczowych vendorów (GitHub, Linear, Atlassian, Cloudflare, OVHcloud, Notion, Grafana, Docker, Bitwarden, Slack) ma teraz oficjalne MCP servery, ale Slack, Notion i Atlassian preferują **remote MCP z OAuth 2.1** zamiast `stdio` — co dla architektury "stdio + Docker container per agent" oznacza konieczność owijania ich w `mcp-remote` proxy.
- **Bitwarden ma oficjalny MCP server (`@bitwarden/mcp-server`) zbudowany wokół Bitwarden CLI** — to jedyna pozycja w tym raporcie, która jest jednocześnie krytyczna i bezpieczna out-of-the-box. **1Password świadomie odmawia ekspozycji sekretów przez MCP** — zalecanym wzorcem od vendora jest `op run` z `op://` referencjami w env vars, nie wywołania tool przez agenta.
- **Najsłabsze obszary, w których trzeba budować custom lub akceptować ryzyko:** macOS-natywne integracje (architektonicznie nie mogą żyć w Docker on Mac), Wiki.js (tylko fragile community MCPs), Twenty CRM i Rocket.Chat (brak MCP), polski rynek pracy (Pracuj.pl brak MCP, NoFluffJobs tylko via płatne Apify), LinkedIn (każdy istniejący MCP narusza ToS — sprawa hiQ v. LinkedIn nadal stanowi precedens kontraktowy).

## Krytyczne ustalenie architektoniczne — LLM provider zarchiwizował reference servery

29 maja 2025 LLM provider przeniósł większość reference MCP serverów (Slack, GitHub, GitLab, Google Drive, PostgreSQL, Brave Search, EverArt) do `modelcontextprotocol/servers-archived` z wprost napisanym brakiem gwarancji bezpieczeństwa ("⚠️ IMPORTANT: This repository is archived and no longer maintained… NO SECURITY GUARANTEES ARE PROVIDED FOR THESE ARCHIVED SERVERS"). Pozostawione jako oficjalne reference w `modelcontextprotocol/servers` są tylko: **Everything, Fetch, Filesystem, Git, Memory, Sequential Thinking, Time**. Konsekwencja praktyczna: jeśli ktoś wciąż używa `@modelcontextprotocol/server-slack` lub `@modelcontextprotocol/server-github` — używa abandoned kodu. **Dla Slacka istnieje znana data-exfiltration vulnerability ("link unfurling")** opublikowana przez Embrace The Red w maju 2025, której LLM provider nie zamierza patchować.

Drugie ostrzeżenie: 15 kwietnia 2026 OX Security (researchers Moshe Siman Tov Bustan, Mustafa Naamnih, Nir Zadok, Roni Bar) opublikowało advisory **"The Mother of All AI Supply Chains"** opisujące **10 high/critical CVE w MCP SDK przez transport stdio**, dotykających 150M+ pobrań i 7000+ publicznie dostępnych serverów. CVE obejmują m.in. LiteLLM (CVE-2026-30623), LangChain, LangFlow, Flowise, LettaAI, Windsurf (CVE-2026-30615), IDE (CVE-2025-54136). Per The Register: LLM provider „repeatedly told the protocol works just fine… despite 10 (so far) high- and critical-severity CVEs". Oficjalne stanowisko LLM provider: "Sanitization is the responsibility of the client developer." Wniosek dla architektury LOCAL/stdio/Docker: **zaufanie do MCP servera musi być explicit, każdy server uruchamiany w izolowanym kontenerze, nigdy nie wystawiamy stdio MCP poza loopback, traktuj każdą zewnętrzną MCP config jako niezaufany kod.**

## Master inventory

| Integracja | Oficjalny MCP | Najlepszy community MCP | Maturity | Licencja | Verdict |
|---|---|---|---|---|---|
| **GitHub** | `github/github-mcp-server` (Go, remote + lokalny via Docker, ~27k★) | — | very high | MIT | **use** — remote OAuth lub lokalny PAT |
| **Linear** | `mcp.linear.app/mcp` (Streamable HTTP, OAuth 2.1) | `tacticlaunch/mcp-linear` (TS, MIT) jako lokalna alternatywa | very high | MIT | **use** — official remote via `mcp-remote` |
| **Jira / Confluence** | `atlassian/atlassian-mcp-server` → `mcp.atlassian.com/v1/mcp` (Rovo MCP, OAuth 2.1) | `sooperset/mcp-atlassian` (Python, MIT, Server/Data Center) | high | MIT (community) | **use** — official jeśli Cloud, sooperset jeśli on-prem |
| **Git** | `modelcontextprotocol/server-git` (Python, jeden z 7 utrzymywanych reference) | — | high | MIT | **use** |
| **Cloudflare** | `cloudflare/mcp` (mcp.cloudflare.com, Code Mode, 2500 endpointów w ~1k tokenów) + 13 product-specific (bindings, observability, browser, R2, Workers, AI Gateway, DNS, ...) | — | very high | Apache-2.0/MIT | **use** — wiele serverów, wybierz po potrzebie |
| **OVH** | `mcp.eu.ovhcloud.com/mcp` / `mcp.us.ovhcloud.com/mcp` (oficjalny Labs OVHcloud, OAuth 2.0) | `runitsolutions/mcp-server-ovh` (TS, MIT, klucze API) | medium-high (oficjalny w Labs) | MIT (community) | **use** — oficjalny remote z OAuth |
| **Docker** | Docker MCP Toolkit + Docker MCP Catalog (270+ verified servers per Docker blog "top-mcp-servers-2025") | — | very high | (proprietary Docker Desktop + open katalog) | **use** — Toolkit jako gateway |
| **Bitwarden** | `bitwarden/mcp-server` (`@bitwarden/mcp-server`, npm, lokalny stdio, wrapper Bitwarden CLI) | `giuliolibrando/bitwarden-mcp-server` (alternatywa też Vaultwarden) | very high (official) | (oficjalny: weryfikuj — Bitwarden core jest GPLv3!) | **use z monitoringiem licencji** — patrz osobna sekcja |
| **1Password** | brak; **świadoma decyzja vendora** | `dkvdm/onepassword-mcp-server`, `CakeRepository/1Password-MCP` (Service Account Token) | medium (oficjalnie odrzucone) | MIT (community) | **build pattern, nie MCP** — używaj `op run` z `op://` referencjami |
| **Notion** | `mcp.notion.com/mcp` (Streamable HTTP, OAuth, hostowany przez Notion) + `makenotion/notion-mcp-server` (stdio, deprecated) | — | high | MIT | **use ostrożnie** — OAuth wymaga interakcji, brak czysto bearer-token |
| **Wiki.js** | brak | `jaalbin24/wikijs-mcp`, `RicardoCenci/wikijs-mcp`, `talosdeus/wiki-js-mcp`, `heAdz0r/wikijs-mcp-server` (wszystkie one-person, niski star count, GraphQL API) | low | MIT | **build custom** lub hardened fork — 3-5 dni |
| **Obsidian** | brak | `MarkusPfundstein/mcp-obsidian` (Python, MIT, najczęściej linkowany), `cyanheads/obsidian-mcp-server` (TS, MIT, lepiej utrzymany, 14 narzędzi) | medium | MIT | **use with monitoring** — cyanheads aktywniejszy |
| **n8n** | brak | `czlonkowski/n8n-mcp` (~20.6k★ per GitHub profile maj 2026, MIT, dla *budowania* workflow przez AI), `leonardsellem/n8n-mcp-server` (~1.6k★, MIT, dla *zarządzania* instancją). Sam n8n ma **MCP Server Trigger node** | high (community) | MIT / fair-code (sam n8n) | **use** — czlonkowski dla DX, native node dla ekspozycji workflow |
| **Grafana** | `grafana/mcp-grafana` (Go, oficjalny Grafana Labs, Helm chart, Docker image) | — | very high | Apache-2.0 | **use** — flag `--disable-write` dla read-only agentów |
| **Langfuse** | `langfuse/mcp-server-langfuse` (oficjalny, ~156★, prompt management) + wbudowany `/api/public/mcp` w samym Langfuse | `avivsinai/langfuse-mcp` (Python, MIT, pełna obserwowalność traces+analytics) | high | MIT | **use** — oficjalny dla promptów, avivsinai dla traces |
| **Rocket.Chat** | brak | brak well-maintained community MCP; istnieje REST API i App SDK | n/a | n/a | **build custom** — 3-7 dni |
| **Twenty CRM** | brak | brak; istnieje GraphQL/REST API | n/a | n/a | **build custom** — 3-7 dni |
| **Slack** | `slack-mcp` od Slacka — **GA 18 lutego 2026** (DEVOPSdigest: "February 18, 2026 · Slack announced the general availability of Real-Time Search (RTS) API and Model Context Protocol (MCP) Server"). Od limited release (Dreamforce, październik 2025) RTS queries i MCP tool calls wzrosły 25× | `korotovsky/slack-mcp-server` (Go, ~1.4k★, browser tokens xoxc/xoxd, write off-by-default), `zencoderai/slack-mcp-server` (Apache-2.0, fork z modernizacją SDK) | high | Apache-2.0 / MIT | **use** — oficjalny remote dla prod, korotovsky dla większej kontroli |
| **Discord** | brak | `SaseQ/discord-mcp` (Java/Spring, Docker image gotowy), `IQAIcom/mcp-discord` (TS, npm `@iqai/mcp-discord`), `v-3/discordmcp` (TS, MIT) | medium | MIT | **use** — SaseQ lub IQAIcom (najszerzej utrzymywane) |
| **Telegram** | brak | `chigwell/telegram-mcp` (Python/Telethon, default-deny ACL, najbardziej feature-complete), `tacticlaunch/mcp-telegram` (TS/MTProto), `sparfenyuk/mcp-telegram` (Python, read-only) | medium | MIT | **use with monitoring** — chigwell jest najpełniejszy |
| **Signal** | brak | nieliczne, mało dojrzałe — najpopularniejsze są wrappery `signal-cli` | low | n/a | **build custom** — 2-3 dni wokół `signal-cli` |
| **KDE Connect** | brak | `g20271/kdeconnect-mcp-server` (Python/FastMCP, 14 narzędzi przez D-Bus) | low (one-person) | unstated | **build custom** lub use with monitoring — 1-2 dni wokół `kdeconnect-cli` |
| **macOS Notifications** | brak | `yuki-yano/macos-notify-mcp` (TS+Swift, klikalne notyfikacje), `piatra-automation/apple-notifier-mcp` (TS, MIT, `terminal-notifier`) | medium | MIT | **use** ale **HOST process, nie Docker** |
| **macOS Calendar/Notes/Mail/Contacts/Reminders** | brak | `Dhravya/apple-mcp` (~3.1k★, MIT, "kitchen sink" via AppleScript/JXA), `FradSer/mcp-server-apple-events` (~32★, MIT, EventKit native Swift) | medium | MIT | **use jako HOST process** — nie Docker; patrz risk callout |
| **macOS Shortcuts** | brak | `dvcrn/mcp-server-siri-shortcuts` (TS, MIT, auto-generuje tool per shortcut), `recursechat/mcp-server-apple-shortcuts` (TS) | medium | MIT | **use jako HOST process** |
| **Email (IMAP/SMTP)** | brak (neutralny protokół) | wiele community wrapperów `imap`/`smtplib`; brak dominującego | low-medium | varied | **build custom** — 2-3 dni; IMAP IDLE komplikuje |
| **Web search** | Brave Search (oficjalny `@brave/brave-search-mcp-server`), Tavily (oficjalny), Exa (oficjalny), Serper (community) | — | very high | varied | **use** — Brave + Tavily wystarczą dla MVP |
| **Reddit, Hacker News** | brak oficjalnych | wiele community (low-mid quality); HN ma stabilne Firebase API | low-medium | MIT | **build custom** — trywialne, 1-2 dni |
| **LinkedIn** | brak (kontraktowo zabronione przez ToS) | `stickerdaniel/linkedin-mcp-server` (Patchright browser automation), `Shubhwithai/linkedin-scraper-mcp` (RapidAPI) | medium (legal risk) | MIT | **skip dla MVP** — patrz risk callout |
| **X / Twitter** | brak oficjalnych z dostępem do API v2 free tier | różne community wrappery; API paid only | low | varied | **skip dla MVP** |
| **Upwork** | brak oficjalnego MCP, ale **oficjalne GraphQL API** | `@chinchillaenterprises/mcp-upwork` (oficjalny API/OAuth), `vanooo/upwork-mcp` (browser via Patchright) | medium | proprietary npm / open | **use API path** — chinchillaenterprises |
| **Indeed** | `mcp.indeed.com/llm/mcp` (oficjalny remote, obecnie tylko LLM Connector) | `borgius/jobspy-mcp-server` (python-jobspy, multi-board) | medium-high | (oficjalny: niejawny), MIT (jobspy) | **use** — oficjalny gdy działa, jobspy fallback |
| **Toptal, freelancer.com** | brak | brak | n/a | n/a | **build custom** (freelancer.com ma REST API) lub skip (Toptal) |
| **Pracuj.pl** | brak | brak | n/a | n/a | **build custom** — 2-3 dni scraper, ToS risk |
| **NoFluffJobs** | brak | `memo23/apify-nofluffjobs-cheerio-scraper` (Apify, płatne) | low | proprietary | **build custom** wokół `nofluffjobs.com/api/posting` JSON feed — 1 dzień |

## BITWARDEN — głębsza analiza (najważniejsza integracja raportu)

Bitwarden ogłosił oficjalny MCP server **21 października 2025** (blog "Bitwarden sets foundation for secure AI authentication with MCP server"). Architektura:

- **Lokalna**: server uruchamia się na maszynie usera, owija oficjalny Bitwarden CLI (`bw`), zachowuje zero-knowledge encryption.
- **Pakiet**: `@bitwarden/mcp-server` na npm; uruchamiany `npx -y @bitwarden/mcp-server`.
- **Auth**: `BW_SESSION` token (krótkotrwały, po `bw unlock`) lub `BW_CLIENT_ID`/`BW_CLIENT_SECRET` dla organization API access. Self-hosted instancje przez `BW_API_BASE_URL` / `BW_IDENTITY_URL`.
- **Operacje**: vault items (read/write hasła, secure notes), Sends, members, groups, policies, device approval — full IT-admin parity z Public API.
- **Disclaimer od Bitwardena** (z README): "This MCP server is designed exclusively for local use and must never be hosted publicly or exposed over a network." Rekomendowany pattern: lokalny LLM (np. via Ollama) zamiast cloud LLM, bo każdy przeczytany sekret idzie do kontekstu modelu.

**Implikacje dla multi-agent architecture:**

1. **Per-agent credentials** — `BW_SESSION` jest krótki (rotuje się przy każdym `bw unlock`), więc każdy kontener agenta musi mieć osobny session token lub współdzielić unlocked vault przez bind-mount socketa CLI. Pattern: jeden "wallet agent" trzyma unlocked session, inne agenty wołają via inner-RPC, **nie** uruchamiają osobnych `bw` instancji.
2. **Licencja oficjalnego serwera** — Bitwarden core repo jest **GPLv3** — sprawdź licencję samego `@bitwarden/mcp-server` w `package.json` przed wdrożeniem w closed-source produkcie. **Community MCP `giuliolibrando/bitwarden-mcp-server` jest MIT** — bezpieczniejszy z perspektywy copyleft, ale single-maintainer.
3. **Read vs write separation** — defaultowo MCP eksponuje write, ale agent orkiestrator nie powinien móc tworzyć/usuwać sekretów. Konfiguruj allowlist tools (`get_item`, `list_items`, `generate_password`) i blokuj `delete_item`, `update_item`.
4. **Alternatywa 1Password** — vendor explicite odmawia ekspozycji sekretów przez MCP (blog "Securing the agentic future: Where MCP fits and where it doesn't"). Rekomendowany pattern to `op run -- <command>` który injektuje sekrety z referencji `op://Vault/Item/field` w env vars i czyści po wyjściu procesu. **Dla multi-agent w Dockerze**: każdy kontener startuje przez wrapper `op run --env-file ./agent.env -- ...` z service account tokenem zamontowanym jako Docker secret.

**Rekomendacja**: dla MVP **użyj oficjalnego Bitwarden MCP** dla scenariuszy, w których agent musi czytać/pisać do vaultu (np. orkiestrator tworzący nowy serwis i zapisujący wygenerowane hasła). Dla *typowego* startu agenta (potrzeba GitHub token, OVH key) **nie używaj MCP** — używaj `bw get` wywołanego przez Dockerfile entrypoint przed startem agenta, w stylu 1Password `op run`. Najmniejsza powierzchnia ekspozycji sekretów do LLM.

## Gap analysis — co trzeba zbudować

| Komponent | Effort | Uzasadnienie |
|---|---|---|
| **Wiki.js MCP** | 3-7 dni | Wszystkie 4 community MCPs to one-person, <50★, ostatnia aktywność wątpliwa. GraphQL API stabilne, fork+harden najbezpieczniejszy. |
| **Rocket.Chat MCP** | 3-7 dni | Solidny REST API, ale brak istniejącego MCP. Oczywiste tools: send_message, read_history, list_channels, upload_file. |
| **Twenty CRM MCP** | 3-7 dni | GraphQL API; need CRUD na contact, opportunity, note. |
| **Signal MCP** wokół `signal-cli` | 2-3 dni | Pattern dobrze znany; uwaga na rate limity Signal. |
| **Email MCP (IMAP/SMTP)** | 2-3 dni dla prostego, 5-7 z IMAP IDLE | Brak dominującego community; własny wrapper + nodemailer + node-imap. |
| **Pracuj.pl scraper MCP** | 2-3 dni + ryzyko ToS | Playwright + rate limiting + retry; **udokumentować w-house compliance check** |
| **NoFluffJobs MCP** | 1-2 dni | Publiczny JSON feed `nofluffjobs.com/api/posting`, trywialny wrapper |
| **macOS native bridge** (host-side) | 1-2 dni glue | Nie nowy MCP — wybór gotowych (Dhravya/apple-mcp, FradSer, yuki-yano) + uruchomienie ich jako host services pingujących Docker agenty przez REST |
| **Custom Bitwarden read-only wrapper** | 1 dzień | Owinięcie oficjalnego MCP w cienki guard, który blokuje narzędzia mutujące — bezpieczniej niż polegać na prompcie agenta |

**Total custom-build dla MVP+phase-2**: ~3-4 tygodnie pracy jednego dewelopera, jeśli robimy wszystko poza krytyczną ścieżką.

## Critical-path MCPs dla MVP (7 sztuk)

Minimalny zestaw, który odblokowuje pierwszą działającą wersję multi-agent platformy:

1. **GitHub** — `github/github-mcp-server` (lokalny Docker image `ghcr.io/github/github-mcp-server` z PAT lub remote OAuth). 100% must-have.
2. **Bitwarden** — `@bitwarden/mcp-server` lokalny stdio + dodatkowa warstwa entrypoint która używa `bw` CLI do injekcji sekretów per-agent. Bez tego cała architektura jest niebezpieczna.
3. **Cloudflare** — `mcp.cloudflare.com/mcp` via `mcp-remote` OAuth. Pokrywa DNS, R2, Workers, KV — całą infrastrukturę edge'ową.
4. **Docker MCP Toolkit / Gateway** — jako warstwa orkiestracji wszystkich pozostałych MCP serverów. Container isolation + signed images + OAuth manager rozwiązuje problemy z izolacją per-agent.
5. **Filesystem + Git + Fetch** — oficjalne reference servery (`@modelcontextprotocol/server-filesystem`, `@modelcontextprotocol/server-git`, `@modelcontextprotocol/server-fetch`). Trivial, MIT, must-have.
6. **Brave Search** — oficjalny `@brave/brave-search-mcp-server` (API key). Najbardziej free-tier-friendly z web-searchów.
7. **Linear** lub **Atlassian** (wybór jeden) — `mcp.linear.app/mcp` lub `mcp.atlassian.com/v1/mcp` przez `mcp-remote`. Dla MVP wystarcza task management w jednym narzędziu.

Wszystkie official-grade lub MIT z >1k★. Żadnych one-person projektów na krytycznej ścieżce.

## Phase-2 dodaj (gdy podstawa działa)

- **Notion** lub **Obsidian** (knowledge base — wybór zależy od tego, gdzie founder już pisze)
- **OVH** — `mcp.eu.ovhcloud.com/mcp` dla VPS, domen, mail
- **Slack** lub **Discord** lub **Telegram** (jedna z komunikacji)
- **Grafana** — `grafana/mcp-grafana` z `--disable-write` na początku
- **Langfuse** — oficjalny prompt MCP + agent skill dla observability
- **n8n** — `czlonkowski/n8n-mcp` jeśli zamierzasz dawać agentom budowanie workflow
- **macOS native bridge** (na hoście, nie w Dockerze)

## Risk callouts

### Security-critical

- **Slack reference server** — używaj wyłącznie zencoderai/korotovsky lub oficjalnego remote; reference LLM provider ma niepatched data-exfiltration via link unfurling (Embrace The Red, maj 2025).
- **MCP stdio RCE-class vulns** — OX Security, 15 kwietnia 2026, **10 high/critical CVE** w MCP SDK dotyczących 150M+ pobrań przez stdio config-to-command. Mitigation: każdy MCP server w osobnym kontenerze bez network access poza loopbackiem, externalne configi z untrusted sources traktować jako kod.
- **Bitwarden + cloud LLM** — Bitwarden explicite ostrzega: rozważ local LLM dla pełnej zero-knowledge property. Cloud LLM widzi sekrety w kontekście.
- **1Password "MCP for credentials" antywzorzec** — 1Password oficjalnie *nie chce* eksponować sekretów przez MCP. Trzymaj się ich `op://` env-var pattern.

### Licencja-critical (closed-source commercial)

- **Sam Bitwarden core jest GPLv3** — sprawdź licencję `@bitwarden/mcp-server` w `package.json` przed wdrożeniem. Jeśli pakiet linkuje jako library, GPL może się propagować. `giuliolibrando/bitwarden-mcp-server` na pewno MIT, ale single-maintainer.
- **GPL/AGPL kontaminacja w community MCPs** — wiele small-time community serwerów nie deklaruje licencji w README. Polityka: jeśli `LICENSE` file brakuje, traktuj jak "all rights reserved" (Github default) i **nie używaj**.
- **`ahacop/macos-notify-bridge` jest GPLv3** — odrzuć dla closed-source.

### Fragile / abandoned

- `jerhadf/linear-mcp-server` — explicit deprecation w README ("use official Linear remote"), nadal pojawia się w awesome lists.
- `@modelcontextprotocol/server-github`, `-slack`, `-gdrive`, `-postgres`, `-brave-search`, `-everart` — wszystkie zarchiwizowane od maja 2025. NPM packages żyją, ale unmaintained.
- `Siddhant-K-code/mcp-apple-notes` — autor explicite oznaczył "Not actively maintained".
- Wszystkie 4 Wiki.js community MCPs (jaalbin24, RicardoCenci, talosdeus, heAdz0r) — one-person, niski star count, ryzyko bus factor = 1.
- `leonardsellem/n8n-mcp-server` — autor sam pisze "maintained on a part-time basis by a passionate individual who isn't a seasoned engineer". Użyj `czlonkowski/n8n-mcp` zamiast.

### Architectural tensions

- **macOS native MCPs nie działają w Dockerze** — Docker Desktop na macOS to Linux VM (LinuxKit), nie ma dostępu do AppleScript/JXA, EventKit, ani SQLite stores w `~/Library`. Każdy `Dhravya/apple-mcp`, `FradSer/mcp-server-apple-events`, `dvcrn/mcp-server-siri-shortcuts` musi działać jako **host process** na Macu (uruchomiony przez `npx`/`bunx`/`uvx`), Docker-side agenty komunikują się z nim przez HTTP/MCP-remote lub przez Unix socket bind-mountowany do kontenera. **Konsekwencja**: macOS-native MCPs są ekstra warstwą deployment, nie częścią dockerowego mesh'u. Jeśli architektura ma być portable Linux-friendly w przyszłości, ogranicz macOS integracje do scenariuszy, gdzie founder fizycznie używa swojego Maca jako orchestratora.
- **KDE Connect MCP też nie w Dockerze** — wymaga lokalnego D-Bus i zsparowanych urządzeń. Same constraints jak macOS.

### Legal / compliance

- **LinkedIn ToS** — User Agreement §8.2 wprost zakazuje scrapingu. Sprawa **hiQ Labs v. LinkedIn** (9th Cir. 2022; po remandzie 2022-2024) — scraping publicznie dostępnych stron *nie narusza* CFAA, ale hiQ przegrał na breach-of-contract i ma permanent injunction. Każdy z istniejących LinkedIn MCPs (`stickerdaniel`, `eliasbiondo`, `superyuser`) wymaga zalogowanej sesji → breach-of-contract risk. Bezpieczniejszy pattern: RapidAPI-based MCPs (`Shubhwithai`) płacące third-party providerowi, który bierze na siebie scraping risk.
- **Pracuj.pl + NoFluffJobs ToS** — oba regulaminy zakazują automated harvesting. NoFluffJobs ma publiczny JSON feed `/api/posting` który jest gray-area (technicznie dostępny, ale ToS i tak zakazują auto-scrapingu). Pracuj.pl wprost zakazuje. Recommendation: skontaktuj się z Pracuj.pl o ich Partner API zamiast scraping.
- **GDPR** dla polskich job boardów — ogłoszenia często zawierają imię/nazwisko rekrutera (PII). Agent scrapujący masowo CV-like data jest controllerem PII pod GDPR.

## Rekomendacja końcowa

**MVP set (use teraz):**
- GitHub MCP (official) — Docker image, PAT
- Bitwarden MCP (official) + `bw get` entrypoint pattern (read-only allowlist)
- Cloudflare MCP (official remote, OAuth)
- Docker MCP Toolkit jako gateway
- Filesystem + Git + Fetch (oficjalne reference)
- Brave Search (oficjalny)
- Linear MCP (official remote) — wybór nad Jira jeśli zaczynasz fresh

**Phase-2 (gdy MVP działa):**
- OVHcloud MCP (official remote)
- Atlassian MCP (jeśli klienci używają)
- Notion MCP (official remote) — knowledge base
- Slack MCP (oficjalny, GA od 18 lutego 2026) lub Discord (`SaseQ`) lub Telegram (`chigwell`) — pick one
- Grafana MCP (official, read-only)
- Langfuse MCP (oficjalny prompts + avivsinai dla traces)
- n8n MCP (`czlonkowski/n8n-mcp`)
- macOS bridge na hoście (Dhravya + FradSer + yuki-yano)
- Indeed MCP (oficjalny, gdy ich LLM Connector zostanie open beta)
- Reddit + Hacker News + Email — własne, ~2 dni każdy

**Build custom (nie odpalaj bez tego do prod):**
- Wiki.js MCP — fork i hardening jednej z 4 community implementacji, ~5 dni
- Rocket.Chat MCP — 3-7 dni, własny wokół REST API
- Twenty CRM MCP — 3-7 dni, własny wokół GraphQL
- NoFluffJobs MCP — 1 dzień wokół JSON feed
- Pracuj.pl MCP — 2-3 dni, ale **wstrzymaj się i skontaktuj się z nimi o Partner API**

**Skip dla MVP:**
- LinkedIn MCPs (breach-of-contract risk po hiQ v. LinkedIn)
- Toptal (brak API + agresywny anti-bot)
- Twitter/X (paid API, niska wartość dla operacyjnego agenta)
- 1Password MCP (vendor odradza; użyj `op run` pattern)

**Benchmarki, które zmieniłyby rekomendację:**
- Jeśli LLM provider wprowadzi remote MCP standard z built-in per-agent identity (a nie tylko OAuth user-level) → przesuwa wszystkie OAuth-only servery w stronę "use without `mcp-remote`".
- Jeśli któryś z one-person community MCPs (Wiki.js, Rocket.Chat) dorobi się 500+★ i 2+ aktywnych maintainerów → przesunąć z "build" do "use with monitoring".
- Jeśli Pracuj.pl/NoFluffJobs udostępni publiczne API z partnership tier → eliminuje custom scraper, idziemy na MCP wrapper API.
- Jeśli wyjdzie kolejna RCE-class CVE w MCP stdio SDK bez patcha → wszystkie nie-oficjalne MCPs idą do quarantine w sandbox kontenerach z `--cap-drop=ALL --network=none` poza dedykowanym egress proxy.

## Caveats

- Star counts i daty ostatnich commitów dla mniejszych projektów (zwłaszcza macOS native i Polish job boards) pochodzą z third-party trackerów (PulseMCP, mcpservers.org, lobehub), nie z live GitHub API — mogą być przeszacowane lub przedawnione o tygodnie.
- "Oficjalny" Bitwarden MCP licencyjnie wymaga weryfikacji w `package.json` — Bitwarden core to GPLv3, ale moduły CLI mają mieszane licencje. **Sprawdź przed komercyjnym wdrożeniem.**
- Krajobraz MCP zmienia się tygodniowo. Ten raport jest snapshotem 14 maja 2026; każda decyzja architektoniczna powyżej powinna być re-weryfikowana co 6-8 tygodni.
- Wszystkie remote MCPs z OAuth (Linear, Atlassian, Notion, Cloudflare, OVH, Indeed) są typu "per-user" — w architekturze multi-agent oznacza to, że każdy agent technicznie używa Twojego OAuth tokena, chyba że zbudujesz własny per-agent OAuth bridge. Slack i Atlassian wprowadziły OAuth scope per-server, ale per-agent identity to wciąż otwarty problem dla całego ekosystemu.
- LLM provider w grudniu 2025 przekazał MCP do Agentic AI Foundation (AAIF) — directed fund pod Linux Foundation, współzałożony z Block i OpenAI. Dalsze "official servery" mogą teraz pochodzić od AAIF, nie tylko LLM provider. Monitoruj registry pod `modelcontextprotocol.io`.

## Completion table

| Wymaganie z briefu | Pokrycie |
|---|---|
| Developer tooling (GitHub, Linear, Jira, Git) | ✅ |
| Infrastructure (Cloudflare, OVH, Docker) | ✅ |
| Secrets (Bitwarden deep-dive, 1Password) | ✅ |
| Knowledge (Wiki.js, Obsidian, Notion) | ✅ |
| Self-hosted on merits (n8n, Grafana, Langfuse, Rocket.Chat, Twenty CRM) | ✅ |
| Communication (Slack, Discord, Telegram, Signal, KDE Connect, macOS notif, Email) | ✅ |
| macOS native (Calendar, Mail, Notes, Contacts, Reminders, Shortcuts) | ✅ |
| Web / external (search, Reddit, HN, LinkedIn, X, job boards incl. Pracuj/NoFluff) | ✅ |
| LLM provider archived servers note | ✅ |
| stdio vs OAuth implications for per-agent isolation | ✅ |
| License flagging (GPL/AGPL) | ✅ |
| Docker-on-macOS architectural tension | ✅ |
| LinkedIn/Pracuj/NoFluff ToS legal risk | ✅ |
| MVP critical path (5-7) + Phase-2 list | ✅ |
| Comparison tables for multi-MCP categories (Slack, Telegram, Discord, Obsidian, Wiki.js) | ✅ |
| Sources post-2025-09 prioritized | ✅ |
| Recency caveat | ✅ |