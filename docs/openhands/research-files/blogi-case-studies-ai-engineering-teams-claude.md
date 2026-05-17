Mam zebrane materiały - przeszło 15 źródeł od Anthropic, OpenHands/CAID, Coder, Cognition/Devin, GitHub Squad, Cursor, Vercel, Sourcegraph/Amp, DX i Octoco. Poniżej syntetyczna analiza.

---

# Wdrażanie agentów kodujących i multi-agent workflows — synteza praktyk 2025–2026

## 1. Executive summary

**Co musi wiedzieć lider techniczny zakładający nowy zespół agentów:**

1. **Domyślnie projektuj single-agent, multi-agent uzasadniaj danymi.** Anthropic, getDX i Cognition zgodnie raportują, że zespoły inwestują miesiące w skomplikowane architektury multi-agent, by odkryć, że lepszy prompt na pojedynczym agencie dawał ten sam efekt, przy 3–10× niższym zużyciu tokenów. CooperBench (styczeń 2026) pokazuje, że agenci osiągają ~50% niższy success rate przy współpracy niż solo — wąskim gardłem nie jest umiejętność kodowania, ale „social intelligence".

2. **Trzy realne uzasadnienia dla multi-agent**: zanieczyszczenie kontekstu, zrównoleglenie niezależnych podzadań, specjalizacja toolsetów. Poza tymi przypadkami koszty koordynacji zwykle przewyższają zyski.

3. **Konwergencja branży na tych samych prymitywach.** Claude Code Agent Teams, Cursor Automations, OpenAI OpenHands, Grok Build, Warp Oz mimo różnych UI zbiegły się do tych samych elementów: pamięć repo, użycie narzędzi, sub-agenci, długie wykonanie, specjalizacja ról. CAID (CMU/OpenHands) idzie dalej i pokazuje, że **git worktrees + branches + merges + testy** są infrastrukturą koordynacji, którą mamy gotową od dekad.

4. **Najlepiej działający pattern to writer/reviewer loop.** Devin podwoił PR merge rate — z 34% do 67% — po wdrożeniu strukturalnych pętli review.

5. **Governance > scaffolding.** Powstał nowy element architektury — *agent control plane* (OpenHands Enterprise, Coder Agents, JetBrains Central). To centralne miejsce na: limity budżetu, ślad audytu, scoping uprawnień, observability, marketplace pluginów. Bez tego agenci nie nadają się do produkcji — są „zbyt ryzykowne, zbyt nieprzejrzyste, zbyt niespójne, by skalować".

6. **Mierz agentów jako rozszerzenie zespołu, nie jako osobnych pracowników.** DX rekomenduje traktować agentów jako rozszerzenie deweloperów i zespołów, które je nadzorują — przy ocenie PR throughput zespołu liczyć zarówno PR-y od ludzi, jak i od agentów pod ich kierownictwem. Każdy developer staje się „liderem zespołu agentów".

7. **Realna adopcja jest niższa niż marketing.** Nawet w wiodących organizacjach aktywne użycie narzędzi AI osiąga ok. 60%. Badanie Pragmatic Engineer (marzec 2026): 95% używa AI tygodniowo, 55% regularnie używa agentów; Claude Code preferowany przez 46%.

---

## 2. Case studies

| Organizacja / projekt | Problem | Rozwiązanie | Narzędzia | Governance | Mierniki sukcesu | Link |
|---|---|---|---|---|---|---|
| **Anthropic — Claude's C Compiler** | Czy team agentów napisze nietrywialny system od zera autonomicznie? | 16 agentów Opus 4.6 w pętli, każdy w worktree + Docker, lock-files w `current_tasks/`, brak orkiestratora; specjalizacja: kodowanie, dedup, performance, code review, dokumentacja. Tests-as-oracle (GCC jako known-good compiler). | Claude Code, Docker, git bare repo, harness ~50 LOC bash | Kontener (sandbox); brak ról i orkiestracji — koordynacja przez lock-file pattern; logi i README maintained jako shared memory | 100k LOC, 2000 sesji, $20k API, 2 tygodnie; kompilator buduje Linux 6.9 na x86/ARM/RISC-V, kompiluje QEMU/FFmpeg/SQLite/Postgres/Redis, 99% test suite pass, kompiluje Doom | [Engineering blog](https://www.anthropic.com/engineering/building-c-compiler) |
| **CAID (CMU + OpenHands)** | Multi-agent na długich zadaniach (>godziny) zawodzi przez konflikty merge i zanieczyszczanie kontekstu | Manager-agent buduje graf zależności, przydziela podzadania, każdy engineer w izolowanym worktree; komunikacja przez structured JSON + git commits, **nie** free-form dialog | OpenHands, git worktree/branch/merge, dependency graph | Izolacja przez worktree jest „prerequisitem nie wygodą"; weryfikacja przez test suite; final review przez managera | Commit0: +14.3 pp vs single agent; PaperBench: +26.7 pp; działa na 3 różnych modelach (Claude 4.5 Sonnet, GLM 4.7, MiniMax 2.5) | [Blog post](https://www.openhands.dev/blog/asynchronous-software-engineering-agents) |
| **Cognition — Devin (cały zespół) builds Devin** | Skalowanie dewelopmentu samego Devina | Devin używany przez wszystkie role (web, Slack, Linear, CLI, API); Playbooks dla powtarzalnych zadań; Devin Review na każdym PR; daily audit design system; bug triage automatyczny przez `!triage-bug` playbook; DANA — dedykowany agent danych; MCP do Sentry/Datadog/Vercel | Devin + Devin Review + DeepWiki + DANA + Playbooks + MCPs (Datadog, Sentry, Notion, Linear) | Reviewer lockout: "Devin nigdy nie review'uje własnych zmian"; każdy PR przechodzi przez Devin Review; Auto-Review przy otwarciu PR; Session Insights jako retro per-sesja | 659 PR od Devina/tydzień (vs 154 w 2025); ~⅓ commitów na własnej webappce | [How Cognition uses Devin](https://cognition.ai/blog/how-cognition-uses-devin-to-build-devin) |
| **Devin @ enterprise (klienci Cognition)** | Modernizacja, security fix, test gen w skali | Fleet Devinów na różne repos, playbooki napisane przez senior engineerów | Devin + DeepWiki + Playbooks | Specyfikacja upfront, kontrola QA przez ludzi po fakcie | Security fixes: human 30 min, Devin 1.5 min (20× efficiency); jeden bank 5–10% time saved; Oracle Java migration 14× szybciej; ETL migration 3–4h vs 30–40h; test coverage 50–60% → 80–90%; Litera: +40% coverage, –93% regression cycle; PR merge rate 34% → 67%, 4× szybsze problem solving, 2× mniej zasobów | [Devin's 2025 Performance Review](https://cognition.ai/blog/devin-annual-performance-review-2025) |
| **GitHub Squad** (Brady Gaster, Microsoft) | Setup multi-agent zwykle wymaga godzin orkiestracji, vector DB, message bus | `npm install -g @bradygaster/squad-cli` + `squad init` daje team: lead, frontend, backend, tester; każdy agent w osobnym oknie kontekstu (do 200K tokens), współdzieli pamięć przez `decisions.md` ("drop-box pattern"); reviewer lockout uniemożliwia agentowi review własnego kodu; agent state versioned w `.squad/` razem z kodem | GitHub Copilot + Squad CLI/SDK | Plain-markdown audit trail w git; per-agent context replication zamiast splitting; tester może odrzucić kod od backend specialista, ale specialista nie może revisować własnej pracy | ~1000 GitHub stars w kilka dni; "asynchronous coordination jest bardziej resilient niż real-time sync, system degraduje gracefully gdy agenci są wolni" | [GitHub Blog](https://github.blog/ai-and-ml/github-copilot/how-squad-runs-coordinated-ai-agents-inside-your-repository/) |
| **Cursor Automations** | Engineerzy nie nadążają z review agent-generated kodu, "agent sprawl" | Event-driven agenty triggerowane przez merged PRs, Linear issues, Slack, PagerDuty, custom webhooks; 3 kategorie: PR security audit, blast-radius assessment + auto-approve low-risk, incident response z Datadog | Cursor + BugBot + Memories + MCP (Datadog, Notion) | "It's not that humans are out of the picture; they aren't always initiating — they're called in at the right points in this conveyor belt"; decyzje agentów logowane do Notion via MCP | Cursor jako firma: 35% wewnętrznych PR jest agent-generated; $2B ARR; BugBot processuje setki automatyzacji na godzinę | [TechCrunch + Cursor blog](https://techcrunch.com/2026/03/05/cursor-is-rolling-out-a-new-system-for-agentic-coding/) |
| **Vercel deepsec** | Security review na ogromnych monorepach | 5-fazowy pipeline: Scan (regex) → Investigate (agent per plik, Opus 4.7 max effort + GPT 5.5 xhigh) → Revalidate (drugi agent eliminuje false positives) → Enrich (git metadata: kto naprawi) → Export (tickets); skanuje w 1000+ równoległych sandboxach | Claude + OpenHands + Vercel Sandboxes | Open-source; 10–20% false positive rate akceptowalne dzięki Revalidate; fan-out z attribution | Znajdowanie subtle auth edge cases w monorepach Vercela i klientów (np. dub.co) | [Vercel engineering blog](https://vercel.com/blog/category/engineering) |
| **OpenHands Enterprise** | Brak centralnej kontroli nad fleet agentów blokuje produkcyjne użycie | Agent Control Plane: orkiestracja (workflows definiowane raz, wykonywane na wielu repach równolegle), sandboxed execution, observability i audit, cost attribution per user/conversation, plugin marketplace; Automations triggerowane przez harmonogram lub eventy | OpenHands SDK + Control Plane + Index (benchmark/leaderboard) | Każda konwersacja zalogowana i powiązana z userem; budżety per org i user; sandboxed execution | "Standardowe use cases: vulnerability remediation, dependency upgrades cross-repo, PR review, incident response, large-scale codebase migrations" | [OpenHands blog](https://www.openhands.dev/blog/openhands-enterprise-agent-control-plane) |
| **Coder Agents** | Multi-tool lock-in i fragmentacja agent stack w organizacjach | Native agent na control plane; rozdzielenie *how agents run* od *which models they use*; centralne zarządzanie modelami, promptami, MCPs, skills i network-isolated workspaces | Coder workspaces + AI Governance + Coder Agents | Self-hosted, on-prem, air-gapped; SOC 2 Type II; centralna LLM gateway, polityki sieci, audyt | Skierowane do regulowanych branż (defense, finance, gov) | [Coder blog](https://coder.com/blog/introducing-coder-agents) |
| **Booking.com** | Adopcja AI wśród 3500+ inżynierów | Roll-out z DX framework: utilization → impact → cost; standaryzacja metryk; programowa enablement | DX platform + AI tools | Brak top-down mandate, brak użycia metryk w ocenach indywidualnych | +16% throughput w kilka miesięcy | [DX framework](https://getdx.com/research/measuring-ai-code-assistants-and-agents/) |
| **Block (codename goose)** | 4000+ inżynierów, własny agent w open source | Data-driven AI strategy; własny agent „goose"; pomiary przez DX | DX + custom agent | Pomiar PR throughput w sposób uwzględniający agenty jako extensions | Standaryzacja decyzji o inwestycjach AI | [DX customers](https://getdx.com/customers/) |

**Inne potwierdzone liczby z 2025/2026:** Rakuten — 7 godzin autonomous work na vLLM (12.5M LOC) z 99.9% numerical accuracy; TELUS — 13 000+ rozwiązań AI, +30% szybsze code shipping, 500 000 godzin zaoszczędzonych; Zapier — 89% adopcji, 800+ wewnętrznych agentów. Factory AI: 5000+ inżynierów w EY.

---

## 3. Human oversight — jak zespoły kontrolują agentów

**Główna zasada (powtarza się u wszystkich):** agenci otwierają PR, ludzie merge'ują. Człowiek przesuwa się z pisania kodu na specyfikację i walidację.

Konkretne praktyki, które zadziałały produkcyjnie:

- **Reviewer lockout.** W Squad i Devinie warstwa orkiestracji uniemożliwia oryginalnemu agentowi zrewidowanie własnej pracy — inny specjalista musi to zaakceptować lub odrzucić.

- **Verification sub-agent z explicit instructions.** Anthropic ostrzega przed „early victory problem" — werifier markuje PASS po jednym teście. Mitigacja: "You MUST run the complete test suite before marking as passed"; specyfikuj konkretne kryteria, negatywne testy, multiple scenarios.

- **Sandboxed execution z scoped permissions.** OpenHands i Coder uruchamiają każdą sesję agenta w izolowanym kontenerze z explicit allowlistą sieci, plików i tooli. "Sandboxed runtime izoluje agent activity i zapewnia, że praca odbywa się w controlled environment".

- **Audit trail w git, nie w bazie wektorowej.** Squad i Anthropic C-compiler pokazują, że "asynchronous knowledge sharing inside the repository scales better than real-time synchronization": każda decyzja jako structured block w `decisions.md`, versioned i edytowalna ręcznie.

- **Blast-radius gating.** Cursor Automations "ocenia PR risk na podstawie blast radius, technical complexity i infrastructure impact; low-risk automatycznie aprobowane, high-risk dostaje reviewerów na podstawie contribution history".

- **Specyfikacja zamiast iteracyjnego coachowania.** Cognition odkrył twardo: "Devin radzi sobie z clear upfront scoping, ale nie z mid-task requirement changes — zwykle radzi sobie gorzej, gdy mówisz mu coraz więcej po starcie zadania. To kładzie odpowiedzialność na inżynierze, żeby dobrze zakresował pracę z góry".

- **Stopping criteria dla evaluator-optimizer loops.** Anthropic: "Set clear stopping criteria before iterating. Define maximum iteration counts and specific quality thresholds. Bez nich kończysz w drogich pętlach, gdzie evaluator znajduje minor issues a generator je tweakuje".

- **Hold-the-line review na każdym PR.** Cognition: "Używamy [Devin Review] na każdym PR; Auto-Review startuje przy otwarciu PR lub gdy ktoś dodawany jest jako reviewer; Bug Catcher labeluje issues po confidence level".

- **Daily/scheduled audyty** zamiast ad-hoc nadzoru. Cognition robi codzienny design system audit — "Devin skanuje PRs zmerge'owane w ostatnich 24h, flaguje hardcoded colors, non-standard spacing, tworzy Linear tickety dla każdej violation, opcjonalnie otwiera fix PRs automatycznie".

- **Cooperbench-świadomość:** jeśli planujesz multi-agent, zaplanuj **mniej** agentów niż chciałbyś — "reguła kciuka: 5–6 zadań per teammate agent. Mniej — nie ma sensu parallelism; więcej — coordination cost zjada zysk".

---

## 4. Operating model — dzień pracy, backlog, review, retry, escalation

Wzorzec, który wyłonił się jako _de facto_ standard:

**Backlog → trigger**

Trzy ścieżki wejścia zadania do agenta:
1. **Foreground (interactive)** — developer w terminalu/IDE, prompt synchroniczny (Claude Code, Cursor agent mode).
2. **Background (async)** — task uruchamiany w cloud VM lub kontenerze, developer dostaje PR (Cursor Background Agents, Devin, OpenHands Web, OpenHands).
3. **Event-triggered / scheduled** — PagerDuty alert, Linear ticket z labelem `Bug`, merged PR, daily cron (Cursor Automations, OpenHands Automations, Cognition `!triage-bug` playbook).

Addy Osmani opisuje to jako trzy „tiers": Tier 1 dla pracy interactive, Tier 2 dla parallel sprints, Tier 3 do drenowania backlogu w nocy.

**Wzór dnia (lidera/operatora)**

1. **Plan & spec** — engineer pisze precyzyjną specyfikację. Cognition: "Use Ask Devin to explore code i clarify a goal, then start session directly from search interface — Devin startuje z clear context".
2. **Fan-out** — kilka równoległych zadań dla agentów; każdy w osobnym worktree/branch/sandbox. Anthropic C-compiler: "Każdy agent klonuje lokalną kopię do `/workspace`, gdy skończy push'uje z lokalnego kontenera do upstream".
3. **Inflight monitoring** — dashboard pokazujący sesje, ich progress, blast-radius oceny. Cursor `Memories` agentów uczą się przez runs.
4. **Review** — agent review innego agenta jako pierwsza linia, human review przed merge. "Bottleneck przesunął się z pisania kodu na review go" — Cognition.
5. **Retry vs escalate** — jeśli verifier returns FAIL: feedback do generatora z `Previous attempt failed: {issues}`, max 3 próby (wzór z Anthropic `implement_with_verification(max_attempts: int = 3)`); po wyczerpaniu — escalation do człowieka.
6. **Retro (session insights)** — Cognition: "Session Insights analizuje completed sessions i daje action items, suggested improved prompts; spinujemy nowe sesje z improved promptami". Squad commit decisions do `decisions.md`, OpenHands loguje koszt i toole per-conversation.

**Wzorce komunikacji między agentami** (z Octoco/Anthropic):

- **Hub-and-spoke** (domyślnie Claude Code sub-agents, OpenHands orchestrator) — najprostszy, bottleneck na coordinator.
- **Peer-to-peer inbox** (Claude Code Agent Teams TeammateTool) — mniej overhead, więcej state awareness.
- **Shared task list** — agenci self-assign z board `pending → in_progress → completed`.
- **Structured documents** (MetaGPT, Squad `decisions.md`) — agenci wymieniają specs/plany zamiast czatować; "MetaGPT osiąga 85.9% Pass@1, znacząco wyprzedzając dialogue-based systems jak ChatDev".
- **Broadcast** — drogie w kontekście, ale potrzebne dla globalnych sygnałów.
- **File reservation leases** — exclusive locks na pliki, jak w Anthropic C-compiler.

**Wzorce orkiestracji** (z Anthropic):

| Pattern | Kiedy używać | Trade-off |
|---|---|---|
| Sequential | Etapy z zależnościami; draft → review → polish | Latencja: każdy krok czeka na poprzedni |
| Parallel | Niezależne podzadania, code review po wymiarach, eval | Koszt: wielokrotne API calls + strategia agregacji |
| Evaluator-optimizer | Pierwsza wersja nie wystarcza (gen API docs, customer comms, code z security req.) | Mnoży tokeny i iteracje |

"Start with the simplest pattern that solves your problem. Default to sequential. Move to parallel when latency is the bottleneck and tasks are independent. Add evaluator-optimizer loops only when you can measure the quality improvement".

**Meta-pattern do kosztów**: plan/execute split — Opus-tier do planowania i decomposition, Haiku/Sonnet-tier do egzekucji. Databricks: tiered model routing obniża inference cost o 45–65%.

**Decomposition rule (Anthropic):**

"Context-centric decomposition, nie problem-centric. Agent obsługujący feature powinien też pisać do niego testy, bo już ma kontekst. Splituj tylko gdy kontekst można izolować. Problem-centric split (planner / implementer / tester / reviewer) prowadzi do tego, że agenci spędzają więcej tokenów na koordynacji niż na pracy".

---

## 5. Metrics — co ma sens, a co jest teatrem

### Co ma sens

**Utilization (faza 1 — adopcja):**
- Active usage rate (% inżynierów używających ≥1× tygodniowo). Benchmark DX: nawet wiodące organizacje osiągają ok. 60% active usage.
- Adoption per use case (modernization, test gen, bug triage, PR review, codebase Q&A).
- Liczba aktywnych playbooków/skills/MCP używanych w organizacji.

**Impact (faza 2 — efekt):**
- **PR merge rate dla agent-authored PR** (Devin: 34% → 67% to twardy benchmark). Sygnalizuje czy spec i review loops działają.
- **AI-driven time savings per developer per week** (DX, direct measure).
- **PR throughput zespołu, gdzie agent PR-y są wliczane jako extension zespołu** (DX rekomendacja).
- **Test coverage delta** (Litera: +40 pp; Cognition customers: 50–60% → 80–90%).
- **Cycle time per task type** w porównywalnych klasach (security fix, framework migration, test gen) — Devin 30 min → 1.5 min na vulnerability.
- **Regression rate na agent-authored PR** (czy szybkość kosztuje jakość — DX zaleca "balance velocity with quality and maintainability").
- **First-pass verifier success rate** (zanim ludzkie review).
- **Mean Time To Investigation** dla bugów (Cognition skraca to do zera dzięki triage-on-label).

**Cost (faza 3 — ROI i governance):**
- Tokens per task per task class (nie sumy globalne).
- Koszt per zmergeowany PR.
- Koszt per defekt znaleziony przez evaluator (vs koszt postprodukcyjnego defektu).
- Per-user / per-team budget burn z attribution (Agent Control Plane primitives).
- Tool selection accuracy w środowiskach z 20+ tools.

**Reliability / recovery:**
- % zadań markowanych PASS przez verifier, które przeszły human review bez zmian.
- Stopa false-positive flag (Vercel deepsec: 10–20% akceptowalne dzięki Revalidate).
- Multi-step task success across N runs (przypomnienie: pojedynczy run 60% może spaść do 25% przy 8 runach, jeśli nie ma rekonwergencji).

### Co jest teatrem

- **Code generation volume / linie kodu**. "Metryki jak code generation volume są szczególnie podatne na gaming. Zachęcanie do zachowań, które optymalizują metrykę zamiast wyniku, ryzykuje malicious compliance".
- **Liczba „agentów" lub „workflows" w organizacji** bez powiązania z PR/incidentami.
- **Pojedyncze demos „16 agentów napisało X"** bez kontekstu kosztu i defektów. Anthropic uczciwie podał: $20k, 2000 sesji, nie potrafi w pełni zastąpić GCC, generuje mniej wydajny kod niż GCC bez optymalizacji.
- **Stopa akceptacji autocomplete** jako proxy productivity (mierzy klikanie Tab, nie wynik).
- **Marketing-leveraged benchmarki typu SWE-bench** bez własnego eval na własnym repo. Octoco: "jeden Reddit dev spędził 6 godzin orkiestrując orchestra of agents, 50k tokenów per request, wynik: single page z awful UX, mógł to zrobić w 10 minut z single agentem".
- **„Adoption rate" wymuszony przez OKR-y** — łatwo zgameować przez powierzchowne użycie.
- **Demo TTV** (time-to-prototype) — Lovable potrafi zbudować app w 10 min, ale dla brownfield codebase to nie jest predyktorem niczego.

### Anti-rules procesowe (DX)
- Nie używaj metryk AI w indywidualnych ocenach pracowniczych.
- Komunikuj wyraźnie, do czego służą metryki przed roll-outem.
- Pomiar to input do decyzji inwestycyjnych, nie micromanagement.

---

## 6. Implications for Octadecimal — co warto zastosować w pierwszym dokumencie projektowym

Założenie: budujecie zespół agentów od zera, nie naprawiacie legacy. Konkretne rekomendacje do *Project Design Doc v1*:

### A. Otwórzcie sekcję „Architecture decisions" zanim napiszecie kod

Zainspirujcie się Squad/CAID: **plik `decisions.md` w repo jako jedyne źródło prawdy o architekturze agentów**. Wersjonowany w gicie, edytowalny ręcznie, czytany przez wszystkich agentów. To wasz „centaur pod brain". Bez vector DB, bez Redis. Każdy plugin, model, polityka, naming convention — append jako structured block.

### B. Zacznijcie od jednego agenta + jednej pętli writer/reviewer

Nie startujcie z teamem 5 ról. "Start with the writer/reviewer loop. Two agents, one structured feedback cycle. Dane z Devina (34% → 67% merge rate) sugerują, że ten pojedynczy pattern dostarcza outsized returns".

Dopiero gdy obserwacyjnie potwierdzicie ograniczenie writer/reviewer pętli, dodawajcie parallelism lub specjalizację — i tylko dla **klasy zadań**, której nie da się obsłużyć inaczej (Anthropic kryteria: context pollution >1000 tokenów irrelevant content; tasks parallelizable; tools >15–20).

### C. Wybierzcie 3 first-class use cases, nie 30

Spróbujcie te trzy (najwyższy ROI w danych z 2025/2026):
1. **Security vulnerability remediation z static analysis input** (Devin: 20× efficiency, Vercel deepsec: 5-fazowy pipeline). Niski blast radius, jasne kryteria, mnóstwo równoległej pracy.
2. **Test generation / coverage uplift** (Cognition pokazuje 50-60% → 80-90%).
3. **PR review jako pierwsza linia + bug triage on Linear label** (Cognition i Cursor: każdy PR → agent review przed human merge; bug ticket dostaje label → automatyczny triage z root cause i suggested fix).

Unikajcie na start: greenfield product dev z niespecyfikowanymi wymaganiami, krytyczne ścieżki performance, UI/UX design (Devin sam mówi: "Devin doskonali budowanie interfejsów, które działają; stylowanie ich pięknie to wciąż domena człowieka").

### D. Zaprojektujcie Agent Control Plane od dnia 1 — choćby minimalny

Nawet jako 10-osobowy zespół zróbcie minimalne primitives:
- **Sandboxed execution** (Docker, ephemeral worktrees).
- **Cost attribution per user × per conversation × per agent role** (potem skalujecie do per-team).
- **Audit log każdej tool-call i każdej edycji pliku** — w gicie wystarczy commit per logical step.
- **Centralna LLM gateway** (jak Coder Agents) — żeby provider/model był decyzją centralną, nie indywidualną.
- **Allowlist/denylist na network i filesystem per role**.

Bez tego — "agenci są zbyt ryzykowne, zbyt nieprzejrzyste, zbyt niespójne, by skalować w produkcji".

### E. Specyfikacja > prompt

Wpiszcie do dokumentu projektowego, że **kontrakt z zespołem brzmi: nikt nie odpala agenta bez specyfikacji z explicit acceptance criteria, forbidden actions i required inputs** (template z Devin Playbooks i Squad). To skraca pętlę i lokuje wartość po stronie ludzi: nauka pisania specyfikacji egzekwowalnych przez agentów to nowy core skill.

### F. Pomiar — przyjmijcie DX-style framework od początku

W dokumencie projektowym opiszcie:
- **Faza 1 (m. 1–2):** utilization metrics + dev sentiment (NPS/CSAT na agent experience).
- **Faza 2 (m. 3–6):** impact metrics — PR merge rate dla agent-PR, cycle time per task class, AI-driven time savings.
- **Faza 3 (m. 6+):** cost per merged PR per class, regression rate na agent-authored zmianach, governance/standardization.

I — explicitly — **wykluczcie z dokumentu listę metryk-teatru**, do których nie wracamy: code generation volume, liczba agentów, „adoption rate" jako KPI, demo TTV.

### G. Stopping rules dla autonomicznych runów

Wpiszcie max iteration count dla evaluator-optimizer pętli, max wall-clock time dla autonomous loops, max cost per session. Anthropic C-compiler użył tego nieformalnie; produkcyjnie to musi być w polityce.

### H. Decomposition policy

W dokumencie zapiszcie regułę: **dzielimy pracę po granicach kontekstu, nie po typach pracy**. Test-writer i feature-implementer to ten sam agent. Frontend i backend separujemy jeśli mają czysty API contract; inaczej zostają razem. To jedna z najgłośniej powtarzanych lekcji 2026 roku.

### I. Plan komunikacyjny

DX uczulił całą branżę: "silnie odradzamy top-down mandates i używanie metryk do indywidualnych ocen". Komunikat dla zespołu w v1 dokumentu powinien jasno powiedzieć:
- te metryki nie wpływają na perf review,
- celem jest zrozumienie efektu agentów, nie micromanagement,
- dane służą inwestycjom organizacji.

### J. Lista rzeczy, których w pierwszej wersji *nie* robicie

- Nie budujecie własnego orkiestratora — używacie CAID, Squad, OpenHands lub Claude Code Agent Teams jako referencyjnej warstwy.
- Nie wprowadzacie 5 ról na start (lead, frontend, backend, tester, docs). Macie writer + reviewer. Specjalizacja przychodzi z dowodów.
- Nie używacie multi-agent dla tasków, które single-agent obsługuje na 100%.
- Nie integrujecie się z PagerDuty/Slack/Linear w sprintów 1–3. Najpierw repo, potem trigger surfaces.

---

### Źródła kluczowe

- Anthropic: [Eight trends defining how software gets built in 2026](https://claude.com/blog/eight-trends-defining-how-software-gets-built-in-2026); [Common workflow patterns for AI agents](https://claude.com/blog/common-workflow-patterns-for-ai-agents-and-when-to-use-them); [Building multi-agent systems: When and how](https://claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them); [Building a C compiler with parallel Claudes](https://www.anthropic.com/engineering/building-c-compiler)
- OpenHands: [Asynchronous SWE agents (CAID)](https://www.openhands.dev/blog/asynchronous-software-engineering-agents); [Enterprise Agent Control Plane](https://www.openhands.dev/blog/openhands-enterprise-agent-control-plane)
- Coder: [Introducing Coder Agents](https://coder.com/blog/introducing-coder-agents)
- Cognition: [Devin's 2025 Performance Review](https://cognition.ai/blog/devin-annual-performance-review-2025); [How Cognition uses Devin to build Devin](https://cognition.ai/blog/how-cognition-uses-devin-to-build-devin)
- GitHub Blog: [How Squad runs coordinated AI agents inside your repository](https://github.blog/ai-and-ml/github-copilot/how-squad-runs-coordinated-ai-agents-inside-your-repository/)
- Cursor: [Automations launch coverage (TechCrunch / Help Net Security)](https://techcrunch.com/2026/03/05/cursor-is-rolling-out-a-new-system-for-agentic-coding/)
- Vercel: [deepsec + Open Agents (engineering blog)](https://vercel.com/blog/category/engineering)
- DX: [Measuring AI code assistants and agents](https://getdx.com/research/measuring-ai-code-assistants-and-agents/)
- Octoco: [Multi-Agent Software Development](https://www.octoco.ai/blog/multi-agent-software-development) — bardzo dobry przegląd z odniesieniami do CooperBench, MetaGPT, Pragmatic Engineer survey 2026
- Addy Osmani: [The Code Agent Orchestra](https://addyosmani.com/blog/code-agent-orchestra/) (trzy „tiers" tooling landscape)