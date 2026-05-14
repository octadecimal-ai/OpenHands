# Zewnętrzne źródła wiedzy, do analizy przydatności

| Target | Official MCP? | Community MCP? | Maturity | License | Werdykt |
|---|---|---|---|---|---|
| **Brave Search** | TAK — reference w `modelcontextprotocol/servers/src/brave-search` | — | A | MIT | Solidny, API key, 2000 free/month. |
| **Serper** | NIE oficjalny | community wrappery (C) | C | MIT | Trivial wrapper. Tańszy niż Brave przy wolumenie. |
| **Tavily** | TAK — `tavily-ai/tavily-mcp` (vendor) | — | A | MIT | Najlepszy do research/agentic search (zwraca kontent, nie tylko linki). API key. **Płatne powyżej free tier**. |
| **Exa** | TAK — `exa-labs/exa-mcp-server` (vendor) | — | A | MIT | Świetny do neural search & similar-pages. Płatne. |
| **Fetch (generic web)** | TAK — reference `modelcontextprotocol/servers/src/fetch` | — | A | MIT | HTTP GET + html→md. Bez JS render. |
| **Reddit** | NIE oficjalny | `Hawstein/mcp-server-reddit`, `adhikasp/mcp-reddit` (C) | C | MIT | OAuth Reddit API. Rate limits ścisłe. |
| **HackerNews** | NIE | community (C, np. `pskill9/hn-server`) | C | MIT | Firebase API publiczne, bez auth. Trivial. |
| **LinkedIn** | NIE | community wrappery przez `linkedin-api` (Python, **unofficial, narusza TOS**) | D | mieszane | **Ryzyko prawne.** Oficjalne LinkedIn API jest restrykcyjne (tylko approved partners). Unikać agentic scraping. |
| **X / Twitter** | NIE | `EnesCinr/twitter-mcp`, kilka innych (C) | C | MIT | Wymaga X API v2 (płatne od 2023). Free tier prawie bezużyteczny. |
| **Upwork** | NIE | brak znanego (NEEDS-VERIFY) | X | — | Upwork API wymaga approved app (długi proces). RSS feeds nadal działają — wrapper na RSS = trivial. |
| **Toptal** | NIE | brak | X | — | Brak publicznego API. Pominąć. |
| **Indeed** | NIE | brak stabilnego | X | — | Indeed Publisher API deprecated (2023). Pozostaje RSS / scraping (kruche). |
| **freelancer.com** | NIE | brak | X | — | Mają REST API, ale onboarding ciężki. Custom MCP możliwy. |
| **Pracuj.pl** | NIE | brak | X | — | Brak publicznego API. Tylko scraping (ryzyko TOS + kruchość). |
| **NoFluffJobs** | NIE | brak | X | — | NFJ ma **publiczny JSON feed** (`nofluffjobs.com/api/...`) — wrapper trivial, ale niedokumentowany → ryzyko zmian. |