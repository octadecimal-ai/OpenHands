<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

## TL;DR

- W 2025–2026 wykrystalizował się dość spójny „kanon” architektury: prosty pętlowy agent (ReAct‑style) otoczony grubym *harness’em* do bezpieczeństwa, kontekstu, orkiestracji, logów i kosztów; sam model jest tylko jądrem obliczeniowym.[^1_1][^1_2][^1_3]
- Git + GitHub stały się główną powierzchnią orkiestracji: **issues/labels → worktrees/branches → PR → human approval**, z agentami odpalanymi przez GitHub Actions lub dedykowane CLI.[^1_4][^1_5][^1_6]
- W praktyce dominuje izolacja przez **git worktrees** + piaskownice runtime (Docker/OCI, „workspaces”, kontenery OpenHands), co pozwala uruchamiać wiele agentów równolegle bez konfliktów w drzewie plików.[^1_7][^1_8][^1_9][^1_4]
- Dobrze zaprojektowane systemy multi‑agentowe rozdzielają role: *planner / decomposer*, *implementer*, *reviewer / janitor*, *tester*, czasem osobne *security / compliance* oraz *knowledge / RAG*.[^1_10][^1_11][^1_12]
- **OpenHands**, **DeepCode**, **Bernstein**, **LLM Squad** i **Microsoft Conductor** dają najbardziej praktyczne, klonowalne wzorce dla „multi‑agent coding teams” – z różnym poziomem formalizacji ról, izolacji i governance’u.[^1_11][^1_13][^1_4][^1_10][^1_7]
- Coder Agents, GitHub Copilot coding agent i OpenHands Agent Control Plane pokazują, jak wygląda „control plane” dla flot agentów: centralne polityki, audyt, budżety, hermetyzacja workspace’ów i integracja z istniejącym SDLC.[^1_14][^1_15][^1_4]
- Anty‑wzorzec: „multi‑agent” rozumiany jako kilka sesji tego samego agenta w jednym katalogu + orkiestracja przez LLM bez deterministycznej warstwy – prowadzi do konfliktów, trudnego debuggowania i nieprzewidywalnych kosztów.[^1_8][^1_16][^1_9]
- Dla Octadecimal najbardziej sensowna ścieżka to: **automation assistant jako jądro**, Git‑centryczne flow z worktrees, deterministyczny orkiestrator a’la Bernstein/Conductor + control‑plane’owy „System team” (na wzór OpenHands/Coder/GitHub) spięty z Twoim Ruflo/BMAD/AGT.[^1_15][^1_17][^1_14][^1_11]

***

## Top repositories

> Wybrane głównie pod kątem: (1) realne multi‑agent coding teams, (2) Git‑/GitHub‑centric flows, (3) bezpieczeństwo, logowanie, koszty, (4) klonowalność i czytelna architektura.


| Repo / projekt | URL | Stars / aktywność (2025–26) | Stack / warstwa | Model pracy zespołu agentów | Co warto skopiować | Czerwone flagi / ograniczenia |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| **OpenHands** (platforma agentów codingowych) | https://github.com/All-Hands-AI/OpenHands | Ok. **64.4k stars, 7.8k forks**, aktywny rozwój i wiele release’ów.[^1_4] | Python (78%), TypeScript (19%), Docker/uv, własny sandbox runtime.[^1_4] | Rdzeń: pętla agenta zdolna do edycji kodu, uruchamiania komend, web browse; do tego GitHub Action „resolver” do auto‑fixu issues i otwierania PR.[^1_4][^1_5][^1_6] Enterprise’owy *Agent Control Plane* dodaje orkiestrację workflowów, sandboxing, audyt i cost attribution.[^1_15][^1_18][^1_19] | Konkretny wzorzec: GitHub Action wyzwalany labelami (`fix-me`, `@openhands-agent`) → agent w piaskownicy → PR + komentarz z logiem działań.[^1_5][^1_6] Warto skopiować: osobny **runtime image** z `LOG_ALL_EVENTS=true`, krótkotrwałe tokeny, jasne zakresy uprawnień i to, że OSS część jest jednoużytkownikowa, a multi‑tenant idzie przez osobny control plane.[^1_4][^1_20] | OSS OpenHands jest zaprojektowany jako **single‑user workstation tool** – autorzy wprost ostrzegają, że nie nadaje się do multi‑tenant bez dodatkowej warstwy auth/izolacji.[^1_4] Enterprise control plane jest source‑available/commercial – nie da się go wprost „skopiować” do własnego OSS stacku. |
| **DeepCode** – Open Agentic Coding | https://github.com/HKUDS/DeepCode | ~7.8k stars wg GitHub Topics, dynamiczny rozwój w 2025.[^1_21][^1_10] | Python, multi‑agent engine + web UI/CLI/API.[^1_10][^1_22] | Wyraźna **multi‑agent architecture**: centralny orchestrating agent, Intent Understanding, Document Parsing, Code Planning, Code Generation, QA / validation; do tego CodeRAG i MCP do integracji narzędzi.[^1_10][^1_22][^1_23] Obsługuje scenariusze Paper2Code, Text2Web, Text2Backend. | Bardzo czytelny podział ról agentów i przepływ: analiza wymagań → parse+spec → plan architektoniczny → generacja → QA.[^1_10] Warto skopiować: **wyraźne role + CodeRAG + MCP** jako standardowy sposób dostępu do toolingu i repo. | Raczej „platforma badawcza” niż twardo uprodukcyjniony system; mniejszy nacisk na Git/GitHub flow (issues/PR), większy na autonomiczną generację repo. Możesz go traktować jako inspirację dla podziału ról, nie gotowy kontroler multi‑repo. |
| **Bernstein** – audit‑grade orchestrator | https://github.com/sipyourdrink-ltd/bernstein | Repo opisane jako rosnące (147+ stars, kilkanaście tys. pobrań miesięcznie na PyPI).[^1_24][^1_25][^1_16] | Python CLI, integracje z 30+ CLI coding agents (automation assistant, OpenHands, Gemini CLI, IDE, Aider itd.).[^1_11][^1_16] | Orchestrator robi **jedno wywołanie LLM do dekompozycji** celu na zadania, a cała dalsza orkiestracja (parallel exec, retrysy, routing) jest deterministyczna.[^1_11] Każdy agent pracuje w **własnym git worktree**; „janitor” sprawdza testy, lint, typy, skany PII przed merge.[^1_25][^1_11] | Referencyjny wzorzec dla Octadecimal: **manager → git worktrees per task → janitor jako reviewer/tester**.[^1_11] Do tego HMAC‑chainowany audit log, replay runs, MCP‑server mode do spięcia z automation assistant jako tool/skill.[^1_24][^1_16] Bardzo dobre źródło pomysłów na logowanie, retry, circuit breakers i cost/behavior anomaly detection. | Złożoność – to już mini‑platforma, nie prosty skrypt. Trzeba uważać, żeby nie przepisać całego Bernsteina w własnym stacku, zamiast użyć go lub zaadaptować tylko koncepty.[^1_11][^1_16] Wymaga dość dojrzałego podejścia do testów (janitor opiera się na istniejących testach/linters). |
| **LLM Squad** – TUI dla wielu agentów | https://github.com/smtg-ai/llm-squad | Otwarty projekt, w praktyce rekomendowany jako „terminal parallelism” (tekstowo: dziesiątki/ setki użytkowników, AGPL).[^1_26][^1_7] | Go / TUI, integracja z automation assistant, Aider, OpenHands CLI, Gemini i innymi CLI.[^1_7][^1_26] | Jedno polecenie tworzy **branch + git worktree + sesję agenta**; TUI pokazuje status wszystkich agentów, zmienione pliki, pozwala pauzować/wznawiać.[^1_7] Izolacja: git worktrees + tmux, każdy agent ma własny katalog i branch.[^1_7][^1_27] Agentów jest wiele, ale **koordynacja jest w 100% human‑in‑the‑loop** – człowiek decyduje co i kiedy mergować. | Idealny, praktyczny wzorzec dla „solo founder + kilka agentów równolegle”: „one command to create agent+worktree”, live dashboard, szybkie przełączanie się między sesjami.[^1_7][^1_27] Warto skopiować: **„session lifecycle” jako domenowy model** (create, navigate, stage, review, delete) zamiast abstrakcyjnych „sub‑agents”. | Brak automatycznej koordynacji między agentami – nie ma task graphu ani zależności, wszystko na Tobie.[^1_26][^1_7] Licencja AGPL komplikuje wbudowanie tego w komercyjny produkt (ale nie w użycie wewnętrzne). |
| **Code Conductor** (ryanmac) | https://github.com/ryanmac/code-conductor | Repo z 2025; opisuje się jako GitHub‑native orchestrator, starów nie podano w snippetach (prawdopodobnie kilkadziesiąt–kilkaset).[^1_28] | Python CLI + shell installer (`conductor-init.sh`), integracja z GitHub i automation assistant.[^1_28][^1_26] | Uruchamia **wiele automation assistant subagents równolegle**, każdy w osobnym git worktree, bez konfliktów.[^1_28] Taski są pobierane z GitHub (issue backlog), a agenci je „claimują”, implementują i wypychają PR.[^1_28][^1_26] | Świetny przykład **GitHub‑native multi‑agent flow**: skrypt inicjalizujący, praca przez issues, worktrees, PR‑y.[^1_28] Warto skopiować: inicjalizator, który umie zainstalować się w repo, skonfigurować worktrees i zapiąć CI / auto‑merge. | Codebase jest młody, a projekt mocno sprzęgnięty z automation assistant; mniej ogólny niż Bernstein/Conductor.[^1_28][^1_26] Brak rozbudowanej warstwy bezpieczeństwa (janitor, test gates) – raczej productivity‑tool niż kontrolowany control plane. |
| **Microsoft Conductor** | https://github.com/microsoft/conductor | Nowy projekt (blog 2026‑05), status: aktywne OSS narzędzie CLI.[^1_17][^1_13] | Python 3.12+, CLI wokół GitHub Copilot SDK; **workflow‑as‑YAML** (jak CI/CD).[^1_17][^1_29][^1_12] | Multi‑agent workflows jako **deklaratywne DAG‑i**: YAML definiuje agentów, grupy równoległe, warunki, loop‑back patterns i human gates.[^1_17][^1_29][^1_12] Każdy agent ma własną sesję, można mieszać modele (Copilot, LLM itd.), a między krokami uruchamiać skrypty (np. `pytest`) jako quality gate.[^1_17][^1_12] | Wzorzec: „**workflows as code** dla multi‑agentów” – YAML wersjonowany w repo, z równoległymi grupami (np. security/perf/style review) i krokami manualnej akceptacji.[^1_17][^1_12] Bardzo mocny przykład wpięcia agentów w istniejący SDLC/CI. | Brak własnego konceptu git worktrees – izolacja jest na poziomie workflow/środowisk, nie branchy.[^1_17][^1_12] Mocno sklejony z Copilot/GitHub; dla Octadecimal raczej inspiracja dla **warstwy orkiestracji BMAD/Ruflo**, nie gotowe narzędzie. |
| **AgenticGoKit** | https://github.com/AgenticGoKit/AgenticGoKit | ~37 stars wg GitHub Topics w 2025, ale z ambicją „production patterns”.[^1_21] | Go, event‑driven framework z MCP, multi‑agent, observability.[^1_21] | Framework LLM‑agnostic; zapewnia MCP tool discovery, event loop, wbudowany monitoring i wzorce produkcyjne (retries, backoff, tracing) dla agentów.[^1_21] | Dla Ciebie cenny jako **minimalny, strongly typed harness**: pokazuje, jak ugryźć multi‑agent event loop i MCP w języku systemowym (Go), co rezonuje z Twoim „System team” poza kontenerami.[^1_21][^1_14] | Nie jest wyspecjalizowany w coding agents – bardziej ogólny „agentic AI” framework; mniej gotowych przykładów wokół Git/GitHub niż w narzędziach powyżej.[^1_21][^1_30] |
| **Dive-into-LLM-Code** (analiza architektury) | https://github.com/VILA-Lab/Dive-into-LLM-Code | Repo towarzyszące paperowi z 2026, samo w sobie nie jest agentem ale zbiorem artefaktów analitycznych.[^1_1][^1_31] | Głównie materiały badawcze (TeX/PDF, referencje, być może skrypty analizy). | Opisuje **7‑komponentową architekturę** automation assistant, 5‑warstwowy pipeline kompaktowania kontekstu, system uprawnień z 7 trybami + klasyfikator ML, 4 mechanizmy rozszerzeń (MCP, plugins, skills, hooks) i subagentów z izolacją worktree.[^1_1][^1_2][^1_3] | To jest blueprint „jak powinien wyglądać production‑grade coding agent harness”: deny‑first permissions, context‑as‑scarce‑resource, append‑only session storage, delegacja do subagentów, human control plane.[^1_1][^1_3][^1_32] Absolutny must‑read jako materiał strategiczny dla Octadecimal. | To nie jest kod produkcyjny automation assistant – raczej reverse‑engineered analiza, więc nie masz tu „gotowego repo do forka”.[^1_1][^1_3] Ale w zamian dostajesz wyjątkowo klarowne zmapowanie decyzji architektonicznych, które możesz przenieść do własnych agentów. |


***

## Architecture patterns

### Agents jako jądro, harness jako „produkt”

- W automation assistant zasadniczy agent to **prosta pętla while‑true → LLM → tools → update state**, a 98% kodu systemu to warstwa wokół: permissions, kompaktowanie kontekstu, subagenci, storage.[^1_2][^1_3][^1_1]
- OpenHands, Coder Agents, GitHub Copilot coding agent i OpenHands Agent Control Plane robią to samo: agent to „kernel”, a produkt to **control layer** – orkiestracja workflowów, izolacja wykonania, audyt i governance.[^1_18][^1_14][^1_15][^1_4]

**Implikacja dla Octadecimal:** Twoje „teams” w Ruflo/BMAD powinny traktować automation assistant/OpenHands jako *compute kernel*, a cała logika: planowanie, retry, metrics, polityki – powinna żyć w zewnętrznym harnessie.[^1_3][^1_14]

### Git jako główny system operacyjny

- Zarówno OpenHands resolver, jak i GitHub Copilot coding agent używają tego samego schematu: **issue/label/mention → job → PR z logiem działań**, czasem z osobnym branch/roboczym środowiskiem.[^1_5][^1_6][^1_4]
- Code Conductor, LLM Squad, Bernstein i szerszy ekosystem orchestratorów opierają się na **git worktrees per agent/task**: każda instancja ma własny katalog i branch, może commitować/pushować niezależnie, a integracja dzieje się przez PR/merge.[^1_28][^1_7][^1_8][^1_11]

**Do skopiowania:** „Git‑first workflow” – to Git issues, branches, worktrees i PR‑y są głównym interfejsem systemu, a agenci są pod spodem tylko wykonawcami.[^1_9][^1_8]

### Izolacja: worktrees + sandbox runtime

- Problemy z równoległymi agentami w jednym katalogu (nadpisywanie `package.json`, brudne PR‑y) są dobrze opisane – i rozwiązywane właśnie przez **git worktrees**.[^1_27][^1_8][^1_9]
- LLM Squad, Bernstein, Code Conductor, a także wiele nowszych narzędzi wykorzystuje ten wzorzec: **branch + worktree per agent**, czasem z dodatkowymi warstwami (tmux, osobne venvy).[^1_33][^1_7][^1_11]
- OpenHands i Coder Agents dodają drugi wymiar izolacji: **sandbox runtime** (dedykowane kontenery/„workspaces”, osobne images z określonymi uprawnieniami, network policies).[^1_34][^1_14][^1_4]

**Wniosek:** dla Octadecimal warto przyjąć twardą zasadę: *brak współdzielonych katalogów między agentami*, zawsze „worktree per agent/task”, a do tego kontener (Docker/Apple Container) jako warstwa izolacji systemowej.[^1_14][^1_9]

### Role: planner, implementer, reviewer, tester, security, knowledge

- DeepCode ma dość książkowy podział: **Central Orchestrating Agent**, Intent Understanding, Document Parsing, Code Planning, Code Generation, QA/Validation – to wprost mapuje się na roles planner → specifier → implementer → tester.[^1_22][^1_10]
- Conductor ma przykładowe workflowy typu `parallel-validation.yaml`, gdzie **security, performance i style** działają jako równoległe, wyspecjalizowane walidatory kodu.[^1_12]
- Bernstein wprost rozróżnia **managera, właściwe coding agents i „janitora”**, który dopiero po przejściu testów/linters/PII pozwala na merge.[^1_25][^1_11]

**Implikacja:** nie trzeba robić hiper‑skomplikowanego planner‑graphu; wystarczy wyraźnie zdefiniowane role i kolejność: **decompose → implement (równolegle) → validate (równolegle) → merge**, przy czym walidacja to osobny „agent z polityką”, a nie tylko kolejny sampling LLM.[^1_11][^1_12]

### Mechanizmy uprawnień i human approval

- automation assistant ma **7 trybów uprawnień** (od „ask‑every‑time” po auto‑approve) i klasyfikator ML, który próbuje przewidywać poziom ryzyka, w duchu „deny‑first with human escalation”.[^1_1][^1_2]
- GitHub Copilot coding agent respektuje istniejące branch protections, ma kontrolowany dostęp do internetu, a PR wygenerowane przez agenta **zawsze wymagają ludzkiej akceptacji przed odpaleniem CI/CD**.[^1_4]
- OpenHands Agent Control Plane wprowadza scoping uprawnień (secrets, network, external systems) plus sandboxed execution; każdy workflow ma pełny log i atrybucję użytkownika.[^1_19][^1_15][^1_18]
- Conductor ma w YAML **human gates** – kroki, które wymagają interactywnej decyzji w webowym dashboardzie; można też ustawić max iterations / timeout.[^1_17][^1_35][^1_12]

**Do skopiowania:** *permissions jako osobna oś konfiguracji*, niezależna od ról: np. „implementer może tylko pisać kod i testy, security reviewer może tylko uruchamiać skanery, janitor może tylko mergować po zielonych testach”.[^1_11][^1_1]

### Observability, logging, cost control

- OpenHands control plane: pełne logowanie każdej konwersacji, powiązanie z użytkownikiem, wgląd w to „co, kiedy, dlaczego”; do tego cost attribution na poziomie organizacji/użytkownika/workflow i budżety.[^1_15][^1_18][^1_19]
- GitHub Copilot coding agent zapisuje **agent session logs** i bazuje na Actions, więc masz standardowe logi CI/CD oraz rozliczalność (Actions minutes + Copilot premium requests).[^1_4]
- Coder Agents dają centralny widok na modele, prompty, użycie i workspace’y, często w tandemie z modułem AI Governance do network policies i visibility.[^1_36][^1_34][^1_14]
- Bernstein idzie w stronę **audit‑grade**: HMAC‑chainowane logi, replay runs, explicit cost/behavior anomaly detection i circuit‑breaker dla agentów „uciekających w nieskończoność”.[^1_24][^1_16][^1_11]

**Dla Octadecimal:** logi i koszty powinny być cechą *System team*, nie pojedynczych agentów – patrz Twoje AGT jako policy kernel + telemetry sink.[^1_16][^1_14]

### Extensibility: MCP, skills, plugins, hooks

- automation assistant ma cztery główne mechanizmy rozszerzeń: **MCP, plugins, skills, hooks**, plus pliki konfiguracyjne typu `AGENTS.md` w repo – wszystko opisane w paperze.[^1_3][^1_1]
- DeepCode wykorzystuje MCP jako standardowy sposób integracji z zewnętrznymi usługami i CodeRAG.[^1_10]
- Coder Agents wprost mówią o MCP oraz „skills” i „sub‑agents” jako sposobie na budowę złożonych workflowów.[^1_34][^1_14]
- Bernstein ma adaptery do dziesiątek CLI agents oraz MCP‑server mode, który umożliwia użycie go jako jednego narzędzia w automation assistant.[^1_24][^1_16][^1_11]

**Pattern:** warto oddzielić **MCP / tools** (zewnętrzne API, repo, CI) od **skills/sub‑agents** (kompozycje tych tools z promptami i politykami) – wtedy Twój harness może mieszać providerów/modeli bez przepisywania core’u.[^1_34][^1_1]

### Deterministyczna orkiestracja vs LLM‑based scheduling

- Bernstein świadomie unika „LLM‑as‑orchestrator”: używa jednego wywołania modelu do dekompozycji celu, a dalej wszystko robi plain Python – scheduling, retrysy, janitor, logi – co daje pełną powtarzalność i brak token‑burn na meta‑sterowaniu.[^1_16][^1_11]
- W przeglądzie orchestratorów autor zauważa, że większość narzędzi „rozwiązuje równoległość” przez git worktrees, ale **koordynacja i merge często zostają na barkach człowieka** – czyli w praktyce brak deterministycznego planera.[^1_26]
- Microsoft Conductor idzie w kierunku **YAML‑first determinismu**: struktura workflowu jest z góry znana, a LLM jest tylko wypełniaczem treści w krokach typu „research”, „generate code”, „review commentary”.[^1_13][^1_17][^1_12]

**Implikacja:** sensowny wzorzec dla Ciebie to: *BMAD/Ruflo jako deklaratywny workflow*, bardzo cienka warstwa LLM‑decomposition, a reszta – deterministyczne grafy z wyraźnymi quality gates.[^1_17][^1_14]

***

## Anti-patterns

### Wspólny katalog dla wielu agentów

- Opisane przykłady pokazują klasyczne problemy: kilka sesji automation assistant w tym samym repo naraz → nadpisywanie zmian w `package.json`, trudne do rozplątania diffy, brak możliwości czystego commita jednej pracy bez drugiej.[^1_8][^1_27][^1_9]
- Blogi wprost mówią, że różnica między „kilka agentów” a **real multi‑agent development** to to, czy każdy agent ma *własną gałąź i katalog* (worktree) i może end‑to‑end zrobić edit → commit → push → PR.[^1_9][^1_8]

**Do unikania:** jakakolwiek architektura, w której dwa agents potrafią pisać do tego samego working directory.

### „Multi-agent” jako theater bez harnessu

- OpenHands opisuje, że zespoły często zaczynają od ad‑hoc skryptów i pojedynczych agentów, ale zatrzymują się w momencie, gdy trzeba je dopuścić do produkcji – brak centralnych polityk, audytu, mierzalności kosztów i standardowego runtime’u.[^1_18][^1_19][^1_15]
- Przegląd open‑source orchestratorów wskazuje, że wiele narzędzi uruchamia co prawda agentów równolegle, ale **nie rozwiązuje** task alignmentu, conflict resolution i decyzyjności co do merge – to dalej siedzi w głowie człowieka.[^1_37][^1_26]

**Anti‑pattern:** system, który tylko odpala wiele sesji LLM, ale nie daje CI *w ogóle* ram: brak jasnych ról, brak polityk i brak centralnych metryk.

### LLM jako scheduler wszystkiego

- Wielu autorów zauważa, że orchestratory oparte na ciągłym „myśleniu” LLM (planner decyduje, kto co robi w każdej iteracji) są **niepowtarzalne i drogie** w tokenach, a przy rosnącej mocy modeli zyskują mniej niż deterministyczne harnessy.[^1_26][^1_3]
- Bernstein expresis verbis krytykuje ten wzorzec i pokazuje alternatywę: jeden strzał LLM do planu, potem wszystko offline w Pythonie.[^1_16][^1_11]

**Do unikania:** budowanie orchestration‑loopu jako kolejnej „rozmowy” z LLM, zamiast zapisu w YAML/JSON + prosty scheduler.

### Brak twardych quality gates

- Bez warstwy typu „janitor” (testy, lints, statyczna analiza, security scanners) lub Conductor‑style script steps, PR‑y agentów stają się *„wchodzi, co przejdzie review”*, co szybko zabija zaufanie.[^1_12][^1_33][^1_11]
- Tam, gdzie gates istnieją (Bernstein, Conductor, OpenHands workflows), służą jako **nie‑LLM‑owe** bezpieczeństwo – sprawdzane są konkretne sygnały (exit code testów, obecność plików, brak PII), a nie ocena tekstowa modelu.[^1_15][^1_12][^1_11]

**Anti‑pattern:** dopuszczanie agentów do mergowania bez automatycznych testów/linters, licząc tylko na ludzkie review.

### Nadużywanie narzędzi single‑user jako multi‑tenant

- OpenHands wprost ostrzega, że lokalne OpenHands jest **„meant to be run by a single user”**, bez auth, izolacji i skalowania – multi‑tenant wymaga osobnego helm chartu i control plane’u.[^1_4]
- Podobne ryzyka pojawiają się przy budowaniu „platformy” na bazie single‑user CLI/TUI (LLM Squad, część orchestratorów) bez dodatkowej warstwy isolation/governance.[^1_7][^1_26]

**Anti‑pattern:** wystawienie jednego procesu agentowego jako „usługi dla wielu ludzi” bez separacji kont, repo, secrets i limitów kosztowych.

***

## Najlepsze kandydaty do głębokiej analizy

1. **OpenHands (OSS + Enterprise/Control Plane)**
    - Dlaczego: pełny stack od single‑user agenta po enterprise control plane z sandboxed execution, policy enforcement i cost attribution.[^1_18][^1_15][^1_4]
    - Co przeanalizować: Docker runtime image, event log format, GitHub Action resolver (`openhands-resolver.yml`), Git‑centric flows (labels, mentions) i jak implementują „Automations” (vuln remediation, dependency upgrades, PR review).[^1_20][^1_6][^1_5]
2. **Bernstein**
    - Dlaczego: najbardziej dojrzały, deterministyczny orchestrator wielu coding agents z „janitorem”, git worktrees per agent i audit‑grade loggingiem.[^1_25][^1_24][^1_11]
    - Co przeanalizować: pipeline `decompose → spawn worktrees → run agents → janitor → merge`, HMAC chain, mechanizmy cost/anomaly detection, MCP‑server mode jako integracja z automation assistant/AGT.[^1_11][^1_16]
3. **LLM Squad**
    - Dlaczego: najlepszy „manualny” wzorzec dla solo‑dev/małego studia: prostota UX, git worktrees + tmux, TUI do zarządzania wieloma agentami naraz.[^1_27][^1_33][^1_7]
    - Co przeanalizować: CLI/TUI jako „agent session manager”, model stanu (sesje, status, zmienione pliki), integracja z wieloma CLI (automation assistant, OpenHands, Aider). To dobra inspiracja dla Twojego System team UI (np. w terminalu).[^1_26][^1_7]
4. **DeepCode**
    - Dlaczego: jedyny OSS projekt, który tak klarownie modeluje **pełen cykl wytwarzania** (od Paper2Code po backend) jako multi‑agent system z centralnym orchestrating agentem i szeregiem wyspecjalizowanych ról.[^1_23][^1_10]
    - Co przeanalizować: jak reprezentują specyfikacje, jak łączą Document Parsing + Intent Understanding + Code Planning, jak wpinają CodeRAG i MCP.[^1_22][^1_10]
5. **Microsoft Conductor**
    - Dlaczego: referencja dla **YAML‑as‑workflow**: multi‑agent, multi‑provider, human‑in‑the‑loop, z wpiętymi testami jako zwykłymi krokami skryptowymi.[^1_13][^1_17][^1_12]
    - Co przeanalizować: przykładowe workflowy (`parallel-validation.yaml`, `design-review.yaml`), model input/output, sposób reprezentacji human gates i retry, integracja z Copilot SDK (analogiczna do spięcia Ruflo z automation assistant).[^1_29][^1_12]
6. **Coder Agents**
    - Dlaczego: wzorzec jak budować **control plane nad workspace’ami** – centralne sterowanie modelami/promptami, network‑isolated workspaces, integracja z istniejącą infrastrukturą dev (CI, Slack, GitHub).[^1_36][^1_14][^1_34]
    - Co przeanalizować: jak rozdzielają „native agent” vs „third‑party agents w workspace’ach”, jak wygląda API do uruchamiania zadań (foreground/background), jak spinają to z Coder Tasks i AI Governance.[^1_38][^1_34]
7. **GitHub Copilot coding agent**
    - Dlaczego: przykład **agent‑as‑first‑class obywatel SDLC**: start od issue assignment, praca w Actions, poszanowanie branch protections, human approval gate przed CI.[^1_4]
    - Co przeanalizować: integracja z MCP (configure MCP servers per repo), sposób użycia Actions jako „compute environment”, jak rozwiązują constraints typu ograniczony internet, branch protections, billing (Copilot premium requests + Actions minutes).[^1_39][^1_4]
8. **Dive-into-LLM-Code (paper + repo)**
    - Dlaczego: jedyny tak dokładny opis architektury produkcyjnego coding agenta, w tym permission modes, context compaction, subagent delegation z worktree isolation, extensibility i logowanie.[^1_2][^1_1][^1_3]
    - Co przeanalizować: tabelę design principles vs values, sekcje o permission system, compaction pipeline, extensibility, subagent delegation, plus open design directions (observability‑evaluation gap, governance).[^1_32][^1_40][^1_1]
9. **AgenticGoKit**
    - Dlaczego: kompaktowy, Go‑owy framework LLM‑agnostic z MCP i observability, dobry jako inspiracja dla „System team” poza kontenerami na macOS Tahoe.[^1_21][^1_30][^1_14]
    - Co przeanalizować: event loop, mechanizmy rejestrowania narzędzi (MCP discovery), integracja metryk i tracingu dla agentów w stylu 12‑factor apps.[^1_21][^1_33]
10. **OpenHands GitHub resolver/Action**
    - Dlaczego: bardzo praktyczny, minimalny wzorzec: „oznacz issue etykietą → agent w Actions → PR + komentarz z logiem”.[^1_6][^1_5]
    - Co przeanalizować: workflow `openhands-resolver.yml`, sposób konfiguracji secrets, retry/timeouty, sposób raportowania statusu do issue/PR.[^1_41][^1_5]

***

## Pytania dla Octadecimal (co trzeba zdecydować po lekturze)

1. **Model izolacji agentów**
    - Czy przyjmujesz twardy standard **„one task = one branch + one worktree + jeden kontener (Docker/Apple Container)”** jako niełamalną zasadę? Jeśli tak, które narzędzie będzie zarządzało życiem tych worktrees (Twój własny „Squad”, adaptacja LLM Squad, czy coś w stylu Bernsteina)?[^1_14][^1_7][^1_9][^1_11]
2. **Warstwa orkiestracji vs LLM scheduling**
    - Na ile orkiestracja ma być zadeklarowana (Ruflo/BMAD jako YAML/JSON workflows w stylu Conductor/OpenHands Automations), a na ile dopuszczasz LLM‑based planners? Gdzie umieścisz granicę: jedno wywołanie „decompose”, reszta deterministyczna jak w Bernsteine, czy coś innego?[^1_17][^1_3][^1_14][^1_11]
3. **Standard ról agentów**
    - Jakie *role* chcesz mieć jako pierwszorzędowe byty w systemie: **planner, implementer, reviewer, tester, security reviewer, knowledge curator**? Jak je zmapujesz na istniejące komponenty (Ruflo swarm roles, BMAD phases, AGT policies) i na struktury w Git (np. branch naming, labelki, statusy PR)?[^1_10][^1_12][^1_14][^1_11]
4. **Permission model i human approval**
    - Czy wprowadzasz warstwę uprawnień podobną do automation assistant/GitHub Copilot: tryby auto/ask‑every‑time, deny‑first, ML‑classifier dla ryzyka? Na jakich operacjach chcesz wymuszać human approval (PR merge, zmiany w infra, dostęp do sekretnych MCP, modyfikacje BMAD rules)?[^1_1][^1_15][^1_16][^1_4]
5. **Observability, logi, koszty**
    - Gdzie będzie mieszkał **prawdziwy dziennik**: w AGT jako centralny log „co zrobił który agent, za ile tokenów, z jakim wynikiem”? Jakie minimalne metryki chcesz mieć (tokeny per task, czas, liczba retrys, coverage testów) i jak je połączysz z Git (issue/PR IDs)? Czy wzorujesz się bardziej na OpenHands Control Plane, Coder Governance czy Bernstein‑style audit trails?[^1_14][^1_15][^1_16][^1_11]
6. **Git‑centric workflow**
    - Jak formalnie zdefiniujesz przepływ „issue → worktree → PR → merge” dla agentów? Czy przyjmujesz coś w stylu OpenHands/GitHub (etkietki `fix-me`, `@agent`), czy budujesz własny zestaw labeli/statusów (np. `octa:planned`, `octa:in-progress/agent`, `octa:needs-human-review`)?[^1_5][^1_28][^1_6][^1_8]
7. **Granica między single‑user a multi‑tenant**
    - Na jakim poziomie stawiasz granicę: czy każdy „human dev” w Octadecimal ma **własny lokalny agent harness** (automation assistant + git worktrees w stylu LLM Squad), a **System team** tylko orkiestruje? Czy budujesz centralny, multi‑tenant control plane a’la OpenHands Enterprise/Coder/GitHub Copilot agent – wtedy musisz zdecydować o auth, tenantach, izolacji secrets i rate limiting.[^1_7][^1_15][^1_34][^1_14][^1_4]
8. **Strategia extensibility (MCP, skills, plugins)**
    - Czy MCP jest *główną* powierzchnią integracji (jak w automation assistant, Coder, DeepCode), a skills/sub‑agents są tylko kompozycjami tych MCP? Jak będziesz wersjonował i dystrybuował skills/agents w ekosystemie Octadecimal – osobne repo z rules/skills (w stylu `agentic-coding`/`deliberate-agentic-development`), czy wpinane per‑repo `AGENTS.md`/`.octa/`?[^1_21][^1_34][^1_10][^1_1][^1_14]
9. **Quality gates i janitor**
    - Jakiego rodzaju „janitora” chcesz mieć: osobny agent (LLM) z polityką, czy czysto nietekstowy zestaw testów/linters/statycznych analiz w stylu Bernsteina/Conductor? Jak wkomponujesz w to security reviewerów (SAST/DAST, PII scanners) i kto ma ostateczne słowo przy merge (janitor vs human lead)?[^1_33][^1_12][^1_11]
10. **Ewolucja w czasie (governance)**
    - Paper o automation assistant podkreśla, że brakuje mechanizmów wspierających **długoterminową spójność kodu i rozwój umiejętności ludzi**. Jak zamierzasz uniknąć „przyspieszenia kosztem zrozumienia”: czy planujesz retrospekty z agentami, knowledge curation (np. Packmind‑style), centralne zasady architektoniczne (BMAD) egzekwowane przez AGT?[^1_3][^1_1]

Te pytania są w praktyce backlogiem architektonicznym dla Octadecimal – odpowiedzi możesz oprzeć bezpośrednio na powyższych repo/patternach, zamiast projektować wszystko od zera.[^1_3][^1_14]
<span style="display:none">[^1_42][^1_43][^1_44][^1_45][^1_46][^1_47][^1_48][^1_49][^1_50][^1_51][^1_52][^1_53][^1_54][^1_55][^1_56][^1_57][^1_58][^1_59]</span>

<div align="center">⁂</div>

[^1_1]: https://arxiv.org/html/2604.14228v1

[^1_2]: https://arxiv.org/abs/2604.14228

[^1_3]: https://arxiviq.substack.com/p/dive-into-llm-code-the-design

[^1_4]: https://www.perplexity.ai/search/2fc13e99-a2b0-4414-a735-68f859e465c2

[^1_5]: https://openhands.dev/blog/open-source-coding-agents-in-your-github-fixing-your-issues

[^1_6]: https://docs.openhands.dev/openhands/usage/run-openhands/github-action

[^1_7]: https://www.rbaconsulting.com/blog/taming-multi-agent-chaos-git-worktrees-for-cleaner-ai-driven-prs/

[^1_8]: https://vibehackers.io/blog/git-worktrees-multi-agent-development

[^1_9]: https://nimbalyst.com/blog/git-worktrees-for-ai-coding-agents-complete-guide/

[^1_10]: https://github.com/HKUDS/DeepCode

[^1_11]: https://github.com/sipyourdrink-ltd/bernstein

[^1_12]: https://github.com/microsoft/conductor/blob/main/examples/README.md

[^1_13]: https://github.com/microsoft/conductor

[^1_14]: https://www.perplexity.ai/search/79100c7f-558c-4278-95d8-ec1727ceba00

[^1_15]: https://www.perplexity.ai/search/97b940e2-3768-4eb2-9574-0089daa8c1d7

[^1_16]: https://skillsllm.com/skill/bernstein

[^1_17]: https://opensource.microsoft.com/blog/2026/05/14/conductor-deterministic-orchestration-for-multi-agent-ai-workflows/

[^1_18]: https://www.businesswire.com/news/home/20260506314667/en/OpenHands-Launches-an-Agent-Control-Plane-to-Manage-Software-Agents

[^1_19]: https://www.openhands.dev/blog/openhands-enterprise-agent-control-plane

[^1_20]: https://docs.openhands.dev/openhands/usage/cloud/github-installation

[^1_21]: https://www.perplexity.ai/search/aae498cd-78be-4561-aee4-4f4764628383

[^1_22]: https://jimmysong.io/ai/deepcode/

[^1_23]: https://huggingface.co/papers/2512.07921

[^1_24]: https://github.com/hesreallyhim/awesome-llm-code/issues/1653

[^1_25]: https://www.reddit.com/r/alphaandbetausers/comments/1sc7r5u/bernstein_opensource_cli_that_orchestrates_ai/

[^1_26]: https://www.augmentcode.com/tools/open-source-agent-orchestrators

[^1_27]: https://www.reddit.com/r/LLMAI/comments/1t9tolw/running_two_llm_code_agents_on_the_same_repo/

[^1_28]: https://github.com/ryanmac/code-conductor

[^1_29]: https://github.com/microsoft/conductor/blob/main/AGENTS.md

[^1_30]: https://github.com/topics/agentic-ai-development?o=asc\&s=stars

[^1_31]: https://github.com/VILA-Lab/Dive-into-LLM-Code

[^1_32]: https://zhiqiangshen.com/projects/LLM_Code_Report/LLM_Code_Report.pdf

[^1_33]: https://boundaryml.com/podcast/2025-12-09-git-worktrees

[^1_34]: https://coder.com/blog/introducing-coder-agents

[^1_35]: https://www.youtube.com/watch?v=tSoHkOzI4To

[^1_36]: https://www.globenewswire.com/news-release/2025/12/09/3202461/0/en/coder-introduces-ai-development-infrastructure-for-hybrid-human-and-agent-teams.html

[^1_37]: https://nimbalyst.com/blog/best-multi-agent-coding-tools-2026/

[^1_38]: https://coder.com/blog/launch-week-2025-introducing-coder-tasks

[^1_39]: https://github.blog/developer-skills/agentic-ai-mcp-and-spec-driven-development-top-blog-posts-of-2025/

[^1_40]: https://www.linkedin.com/posts/andriyburkov_a-must-read-for-anyone-interested-in-building-activity-7453999022152908800-LzLl

[^1_41]: https://github.com/OpenHands/OpenHands/actions/workflows/openhands-resolver.yml

[^1_42]: https://github.com/GlobalAICommunity/global-ai-bootcamp-2025-session-ai-agents

[^1_43]: https://www.youtube.com/watch?v=N4vBhw7_myg

[^1_44]: https://www.youtube.com/watch?v=G3h6ecOPc4g

[^1_45]: https://www.linkedin.com/posts/zaka-rehman-f23020_ai-repository-activity-7368968871950610434-DJsg

[^1_46]: https://www.youtube.com/watch?v=NA-usu666-0

[^1_47]: https://davidmelamed.com/2025/08/08/overview-of-advanced-ai-coding-agents-august-2025/

[^1_48]: https://github.com/sriharsha-inthub/agentic-ai

[^1_49]: https://www.linkedin.com/posts/openhands-ai_from-agents-to-systems-introducing-openhands-activity-7457793295851884544-afxb

[^1_50]: https://www.reddit.com/r/LLMCode/comments/1q9dmxd/multiagent_orchestration_for_parallel_work_tools/

[^1_51]: https://app.daily.dev/posts/deepcode-open-agentic-coding-paper2code-text2web-text2backend--ihse63plr

[^1_52]: https://github.com/OpenHands/OpenHands/actions/runs/18998892498

[^1_53]: https://github.com/wshobson/agents

[^1_54]: https://dev.to/siddhesh_surve/deepcode-the-open-source-agent-that-writes-code-better-than-phds-1nlg

[^1_55]: https://github.com/smtg-ai/llm-squad/discussions

[^1_56]: https://huggingface.co/papers/2604.14228

[^1_57]: https://www.youtube.com/watch?v=HRI34v68igw

[^1_58]: https://x.com/jonoringer/status/2048747028172136827

[^1_59]: https://aiweekly.substack.com/p/dive-into-llm-code

