# Praktyczny przegląd: AI-native engineering teams (2025-2026)

## Executive summary

Trzy rzeczy, które lider techniczny musi zrozumieć, zanim zacznie projektować zespół agentów:

**1. Branża skonwergowała na bardzo podobnej architekturze, ale w praktyce większość zysków pochodzi z bardzo prostych wzorców.** LLM provider, IDE, OpenAI OpenHands, Coder, OpenHands, Cognition i GitHub w ciągu pierwszego kwartału 2026 wypuściły niemal identyczne klocki: izolowane sandboksy/worktrees, agent control plane (governance + observability + budżet), peer-to-peer messaging między agentami, harness z testami jako "zewnętrznym sędzią", oraz wzorzec writer/reviewer. To nie jest moda — to są te same prymitywy, których używają zespoły ludzkie (git branch, merge, CI, code review). CooperBench (styczeń 2026) pokazał, że agenci pracujący wspólnie mają ~50% niższy success rate niż solo — wąskim gardłem nie jest model, tylko koordynacja. Wniosek: zaczynaj od najprostszego wzorca, który rozwiązuje problem.

**2. Większość realnych deploymentów to nie "16 agentów buduje feature", tylko "1-2 agenty robią dobrze zdefiniowaną pracę o niskiej kreatywności w pętli z człowiekiem".** Devin (Cognition) merguje 659 PR-ów tygodniowo we własnym kodzie, ale 67% z nich to junior-level execution: vulnerability fixes, migracje, test coverage, dokumentacja. IDE Bugbot przegląda 2 mln PR-ów miesięcznie — ale jako jeden agent reviewer, nie jako 16-osobowa drużyna. LLM provider eksperyment z kompilatorem C kosztował 20 000 USD przy ~2000 sesjach i sam Carlini przyznaje, że to "barely achievable" — to demo, nie operating model.

**3. Bottleneck przesunął się z pisania kodu na review, kontekst i specyfikację.** IDE podaje, że 35% wewnętrznych PR-ów to kod agenta. Cognition mówi wprost: "shipujemy więcej kodu z agentami, więc bottleneck przesunął się z pisania kodu na review." OpenAI w swoim playbooku dla "AI-native engineering team" rysuje to jako trójpodział **Delegate / Review / Own** na każdym etapie SDLC. To jest właściwy mental model dla projektowania nowego zespołu od zera: nie "ilu agentów", tylko "co delegujemy, co reviewujemy i co zachowujemy jako wyłączną odpowiedzialność człowieka".

Dla nowego zespołu projektowanego od zera oznacza to: zaczynaj od jednego dobrze zdefiniowanego workflow (writer/reviewer albo automation triggerowana eventem), zainwestuj w testy/verifiery zanim w agentów, oddziel infrastrukturę uruchamiania od wyboru modelu, i mierz outcome (merge rate, resolution rate, bugi w produkcji) zamiast aktywności (liczba PR-ów, tokeny).

---

## Case studies

| Organizacja / projekt | Problem | Rozwiązanie | Narzędzia | Governance | Mierniki sukcesu | Link |
|---|---|---|---|---|---|---|
| **LLM provider — C compiler (Feb 2026)** | Demo długo-horyzontowej autonomii: czy 16 agentów napisze działający kompilator C w Ruście od zera? | Single-loop harness ("Ralph loop") w pętli `while true`; każdy agent w osobnym kontenerze Docker z własnym klonem repo; lock-file w `current_tasks/` jako sync; GCC jako "known-good oracle" dla parallelizacji długich tasków; specjalizowane role (refactor, performance, docs, review) | LLM Opus 4.6 + automation assistant, Docker, git, własny harness, CI z testami | Pełna autonomia w sandboksie; brak orchestratora; każda zmiana musi przejść stricter CI; aktualizowane README/PROGRESS.md jako pamięć między sesjami | 100 000 linii Rusta, kompiluje Linux 6.9, ~2000 sesji, ~20 000 USD; 99% pass na GCC torture test suite | [llm-provider.com](https://www.llm-provider.com/engineering/building-c-compiler) |
| **Cognition — "Devin builds Devin" (Feb 2026)** | Skalowanie własnego zespołu inżynierskiego: jak realnie wbić agentów w codzienny workflow każdej roli | Devin dostępny przez web, Slack, Linear, CLI, API; Playbooks jako "custom system prompts" dla powtarzalnych zadań; DANA jako wyspecjalizowany agent danych; DeepWiki indeksuje repo + diagramy; Auto-Review na każdym PR | Devin + Devin Review + Auto-Review + Playbooks + MCP marketplace (Datadog, Sentry, Vercel, Redshift, Notion) | Każdy PR ma Devin Review link; "Bug Catcher" oznacza severe/non-severe; humans nadal mergują; daily audit design system | 659 zmergowanych PR-ów Devina/tydzień (z 154 rok wcześniej); 67% PR merge rate (vs 34% rok wcześniej); 4× szybsze problem solving; coverage 50-60% → 80-90% | [cognition.ai](https://cognition.ai/blog/how-cognition-uses-devin-to-build-devin) |
| **IDE — Automations (Mar 2026)** | "Prompt-and-monitor" nie skaluje się; review i maintenance nie nadążają za produkcją kodu | Event-driven agenty: trigger ze Slacka, Linear, GitHub PR merged, PagerDuty incident, webhook lub schedule; każda automation odpala cloud sandbox z własnym zestawem MCP i modelu | IDE Cloud Agents, Bugbot, MCP (Datadog, Notion), GitHub Actions | Każdy agent ma zdefiniowany cel + scope; security review na każdy push do main, ale nie blokuje PR; risk-based auto-approve dla low-blast-radius zmian; log do Notion dla audytu | Bugbot resolution rate: 52% → 80% (LLM-judge na public repos); ~2 mln PR-ów review/miesiąc; 35% Bugbot Autofix mergowanych; ~1 USD/PR | [ide.com](https://ide.com/blog/automations), [ide.com](https://ide.com/blog/building-bugbot) |
| **OpenHands Enterprise — Agent Control Plane (May 2026)** | Agenci działają u poszczególnych developerów, brak centralnej polityki, brak audit trail, brak budżetu | Self-hosted control plane: orchestration (workflow defined once, run across repos), sandboxed runtime, plugin marketplace, observability i cost attribution na poziomie user/org/conversation | OpenHands SDK + OpenHands Index (model leaderboard), własny runtime | Wszystko w sandboksie; każda konwersacja zalogowana i przypisana do usera; budżety na poziomie org i user; policy enforcement | OpenHands Index porównuje modele po ability/cost/runtime; case use: vulnerability remediation, dependency upgrades, large-scale migracje | [openhands.dev](https://www.openhands.dev/blog/openhands-enterprise-agent-control-plane) |
| **CAID (akademicki, CMU + OpenHands, Apr 2026)** | Multi-agent breaks na integracji: dwóch agentów pisze poprawny kod, który po mergu się sypie | Manager agent buduje dependency graph; każdy engineer agent w izolowanym git worktree; integracja przez `git merge`; cała komunikacja przez structured JSON + commity, nie free-form chat | OpenHands + LLM 4.5 Sonnet / GLM 4.7 / MiniMax 2.5 | Test suite jako automated verifier na każdym kroku; ablation pokazała, że bez izolacji worktree wynik istotnie spada | +14.3% absolute na Commit0; +26.7% na PaperBench vs single-agent baseline | [openhands.dev](https://www.openhands.dev/blog/asynchronous-software-engineering-agents) |
| **Coder Agents (May 2026)** | Każdy zespół używa innego agenta z innym providerem — fragmentacja, lock-in, brak kontroli sieci | Provider-agnostic agent runtime w infrastrukturze klienta (self-hosted/air-gapped); centralne zarządzanie modelami, promptami, MCP, skills; network-isolated workspaces | Coder Workspaces + Coder Agents + AI Governance (LLM gateway) | Centralizacja modeli i promptów; on-prem; opcjonalnie third-party agenci (automation assistant, OpenHands) działają wewnątrz Coder Workspaces z gateway'em | Brak publicznych liczb; case: U.S. defense intelligence org, 2500+ developerów | [coder.com](https://coder.com/blog/introducing-coder-agents) |
| **GitHub Copilot — Agent Control Plane (Feb 2026)** | Multi-vendor: LLM, OpenHands, Copilot — różne UI, różny audit, różna polityka | Unified Agent Control Plane: LLM, OpenHands i Copilot współdzielą memory, repo context, instructions/policies; enable per-org/per-repo; sessions widoczne jako draft PR | GitHub Copilot, LLM, OpenAI OpenHands, VS Code 1.109+ | Enterprise AI Controls → Agents, centralne policy management, audit logging; każda sesja = jeden premium request | Cele operacyjne — porównanie podejść (assign issue do wielu agentów), nie metryki productivity | [github.blog](https://github.blog/changelog/2026-02-26-llm-and-openhands-now-available-for-copilot-business-pro-users/) |
| **Rakuten (LLM provider case study)** | Refaktor w 12.5 mln linijek kodu (vLLM): activation vector extraction | Single-agent automation assistant w pełni autonomicznie przez kilka godzin | automation assistant, Opus | Pełny audit ścieżki kodu; numeryczna walidacja na końcu | Task zakończony w 7h pracy autonomicznej, 99.9% accuracy numerycznej | [llm.com/customers/rakuten](https://llm.com/customers/rakuten) |
| **TELUS (LLM provider case study)** | Demokratyzacja AI w całej organizacji | 13 000+ custom AI solutions zbudowanych wewnętrznie | LLM + automation assistant | Wewnętrzny program governance dla "every employee builds" | 30% szybszy ship engineering code, 500 000 godzin saved | [llm.com/customers/telus](https://llm.com/customers/telus) |
| **Doctolib (healthcare, LLM provider case study)** | Legacy testing infrastructure | Wymiana wewnętrzną z użyciem automation assistant w skali zespołu | automation assistant | Standardowy code review + ich własny SDLC | Testing infra wymieniona w godziny zamiast tygodni; 40% szybszy shipping features | [llm.com/blog/how-enterprises-are-building-ai-agents-in-2026](https://llm.com/blog/how-enterprises-are-building-ai-agents-in-2026) |
| **Litera (LLM provider / Cognition)** | Każdy engineering manager dostaje "team of Devins" w roli QE/SRE/DevOps | Każdy EM ma fleet Devinów do QE testing | Devin | Standardowy human review | +40% test coverage; 93% szybsze regression cycles | [cognition.ai](https://cognition.ai/blog/devin-annual-performance-review-2025) |
| **Goldman Sachs / bank (Cognition)** | Migracja proprietary ETL framework w setkach tysięcy plików | Fleet Devinów równolegle, każdy plik osobno | Devin | Code owners review po batchach | 10× szybciej (3-4h vs 30-40h na plik) | [cognition.ai](https://cognition.ai/blog/devin-annual-performance-review-2025) |
| **EightSleep (Cognition)** | Slow data analyst pipeline | DANA (specjalizowany agent danych) w Slacku | Devin/DANA + MCP do warehouse | Walidacja SQL przed użyciem wyniku | 3× więcej data features i investigations | [cognition.ai](https://cognition.ai/blog/how-eight-sleep-uses-devin-as-a-data-analyst) |

---

## Human oversight

W praktyce produkcyjnej widać pięć powtarzających się mechanizmów kontroli — i żaden z nich nie polega na "agent prosi człowieka o pozwolenie przed każdą akcją". Tak działa tylko najsłabsza forma oversight.

**Verifier-as-oversight.** Najpoważniejsze zespoły inwestują w testy/CI/lintery/security scannery zanim w agentów. Carlini z LLM provider powiedział to wprost przy projekcie kompilatora: harness pisze się dla LLM, nie dla człowieka — logi muszą być greppable, błędy oznaczone `ERROR` w jednej linii, agregaty pre-policzone, kontekst nie zanieczyszczony tysiącami bajtów. CAID idzie dalej i traktuje test suite jako jedyne źródło prawdy między agentami: cała komunikacja przez structured JSON + git commity, nigdy free-form chat. To jest sedno: jeśli verifier jest słaby, agenci rozwiążą zły problem.

**Writer/reviewer loop jako structural primitive.** Devin Review robi to dla każdego PR-a Cognition; IDE Bugbot dla 2 mln PR-ów miesięcznie. Cognition podaje konkretny efekt: po wprowadzeniu strukturalnej pętli review-fix-recheck merge rate wzrósł z 34% do 67%. Bugbot publikuje resolution rate (procent flagów które developer faktycznie naprawia przed mergem) — to anty-vanity metryka, bo karze fałszywie pozytywne i pozwala odróżnić "louder" od "more accurate".

**Risk-based auto-approve.** IDE opisuje wewnętrzną automation, która ocenia każdy PR po blast radius, complexity i infrastructure impact — low-risk zmiany auto-approve, high-risk eskalują do człowieka, decyzje logowane do Notion. To skaluje review, którego ludzie inaczej nie nadążą wykonać.

**Sandboxing + cost attribution + budget caps.** OpenHands Enterprise i Coder pokazują, że bez tego agent w produkcji jest po prostu nieubezpieczalny przez bezpieczeństwo i compliance. Każda konwersacja przypisana do usera, koszt per-org/per-user/per-conversation, hard budgets. To jest też właściwy moment, żeby zatrzymać agenta, który "happily spend hours running tests instead of making progress" (Carlini).

**Mid-task scope freeze.** Cognition pisze wprost: Devin radzi sobie z dobrze zdefiniowanym scope, ale gorzej z mid-task scope changes — "nie da się go coachować jak juniora w trakcie zadania". To zmienia mental model: oversight nie polega na "interweniuj kiedy widzisz problem", tylko na "włóż całą pracę specyfikacyjną przed startem, a po starcie albo akceptuj, albo restart". To również argument za krótkimi sesjami, nie maratonami.

Czego nie robić: nie polegaj na "agent powie kiedy czegoś nie wie". METR podaje, że frontier modele utrzymują ~2h17min coherentnego rozumowania z ~50% pewnością — tzn. agenci regularnie deklarują sukces przy złych testach lub przerwanych zadaniach. Dlatego verifier-as-oversight jest ważniejszy niż self-reporting.

---

## Operating model

Najbardziej operacyjnie konkretny opis dnia pracy zespołu AI-native dostarcza OpenAI w swoim playbooku dla OpenHands i Cognition w "How Cognition Uses Devin to Build Devin". Połączone wzorce wyglądają tak:

**Backlog i wejście pracy.** Ticket w Linear/Jira jest pierwszym punktem styku z agentem, nie z człowiekiem. Devin/OpenHands analizuje opis, przeszukuje codebase i generuje wzbogacony session prompt z dependencies, edge cases i propozycją dekompozycji. Cognition robi to przez Ask Devin (codebase Q&A): inżynier eksploruje kod konwersacyjnie zanim wystartuje sesję, więc agent dostaje już sklarowany cel. OpenAI rekomenduje, żeby workflow tagowania, deduplikacji i auto-uzupełniania ticketów był jednym z pierwszych deployments — daje wartość bez ryzyka, bo nie pisze kodu produkcyjnego.

**Dzień pracy delegacja/review/own.** OpenAI rysuje to per faza SDLC (Plan / Design / Build / Test / Review / Document / Deploy). W każdej fazie agent robi pierwszy draft (delegate), człowiek weryfikuje (review), a strategia i finalna odpowiedzialność zostaje przy człowieku (own). W praktyce to oznacza, że inżynier rano przegląda PR-y agentów z poprzedniej nocy, akceptuje/odrzuca/koryguje, równolegle pisze specyfikacje nowych tasków, a w międzyczasie robi własną pracę na rzeczach niejednoznacznych. IDE wewnętrznie ma "weekly digest" automation, który podsumowuje istotne zmiany w repo z ostatnich 7 dni — to oversight na poziomie tygodnia, nie tylko PR.

**Retry i recovery.** Bezpośrednio z eksperymentu LLM provider: jeden agent zakleszczył się na buildzie kernela Linux — wszystkich 16 agentów dochodziło do tego samego buga, naprawiało go i nadpisywało zmiany nawzajem. Rozwiązanie: GCC jako oracle do delta debugging (sprawdź, które pliki w subseta agenta psują kompilację, zawęź, fix). Wzorzec: kiedy parallelizacja nie pomaga, dodaj "known-good baseline" i parallelizuj nad różnicą. IDE Bugbot Autofix idzie podobną drogą — agent wykonuje fix we własnej VM i testuje go zanim zaproponuje PR.

**Eskalacja.** Devin radzi sobie ze "scoped junior 4-8h tasks"; sygnałami eskalacji są: niejasne wymagania, mid-task scope change, decyzje wizualne wymagające osądu, soft skills. Wszystkie idą do człowieka. IDE security review automation eskaluje high-risk findings do Slacka on-call. PagerDuty incidents → automation pulluje logi przez Datadog MCP, sugeruje fix w PR i powiadamia on-call inżyniera — czas response istotnie się skrócił, ale to człowiek mergeu.

**Komunikacja agent-agent.** Convergence: structured documents > free-form chat. CAID, MetaGPT i kompilator LLM provider używają plików/JSON/git commits jako medium. Wzorce, które się powtarzają: hub-and-spoke (jeden coordinator), shared task list (każdy agent claimuje task przez lock-file), peer-to-peer messaging (automation assistant Agent Teams). Wzorzec, którego należy unikać: free-form dialog między agentami — kosztowny, niesynchronizowalny, generuje halucynacje koordynacyjne.

**Single agent jako default.** Z LLM provider blog post o workflow patterns: spróbuj zadania jako single agent call zanim zbudujesz workflow. Jeśli wynik wystarczy — skończone. Jeśli nie — zidentyfikuj, gdzie zawodzi, i wybierz najmniejszy potrzebny wzorzec (sequential → parallel → evaluator-optimizer). Octoco/Pragmatic Engineer pokazują anty-wzorzec: 6 godzin orchestrowania "orchestry agentów", 50 tys. tokenów na request, wynik gorszy niż 10 minut z jednym agentem i planem.

---

## Metrics

Metryki w tej dziedzinie dzielą się czysto na dwie kategorie: **wskaźniki outcome** (czy kod faktycznie pomógł) i **theater** (aktywność, która imponuje na deskach, ale nie koreluje z wartością).

### Sensowne (outcome i resolution)

| Metryka | Co mierzy | Skąd wiemy |
|---|---|---|
| **Merge rate PR-ów agenta** | % PR-ów wygenerowanych przez agenta, które trafiają do main bez major rewrite | Cognition: 34% → 67% rok do roku to ich główny KPI; pokazuje, czy agent rozwiązuje właściwy problem |
| **Resolution rate komentarzy reviewera-agenta** | % flagów Bugbot/Devin Review, które developer faktycznie naprawia przed mergem | IDE: 52% → 80% (LLM-judge na public repos) — anty-vanity, bo karze fałszywie pozytywne |
| **Time-to-fix per task** | Wall-clock per vulnerability/migration/test | Cognition: 30 min → 1.5 min na vulnerability (20×); migracja file: 30-40h → 3-4h (10×) |
| **Bugs in production / regression rate** | Czy kod agenta wprowadza regresje vs ludzki baseline | DORA-style; brakuje publicznych liczb, ale każdy serious deployment to monitoruje |
| **Test coverage / coverage delta** | Czy faktycznie wzrasta po wprowadzeniu agentów | Cognition customers: 50-60% → 80-90% przy Devin do test gen |
| **Cost per successful task** | USD per task, który człowiek zaakceptował | IDE: ~1 USD per Bugbot run; LLM provider compiler: 20 000 USD / 100 000 linii (jednorazowo, dlatego ekonomicznie niedobrze) |
| **% agent-merged PR z odwołaniem (revert/hotfix)** | Trailing indicator jakości | Devin podaje ⅓ commitów w ich własnym web appie pochodzi z agenta; revert rate nie jest publiczny ale każdy zespół powinien go śledzić |
| **Median planning lead-time** | Czas od ticketu do gotowego planu/spec | Devin podaje "draft architecture w 15 min" jako jeden z większych zysków — to oszczędza godziny meetingów |

### Theater (mierzą aktywność, nie wartość)

- **Liczba PR-ów wygenerowanych przez agentów** — sam w sobie nic nie mówi; ważne tylko relative do merge rate i revert rate.
- **Liczba zaadoptowanych "agent teammates" / instancji** — LLM provider chwali się 13 000 custom AI solutions w TELUS, ale to liczba narzędzi, a nie outcome. Zespół powinien dodatkowo mierzyć, ile z tych 13 000 jest faktycznie używanych po 30 dniach.
- **% developerów używających AI tygodniowo** — Pragmatic Engineer 2026: 95% tygodniowo, 75% przy ≥50% pracy. Ciekawe demograficznie, bezużyteczne operacyjnie.
- **Linijki kodu wygenerowane przez agenta** — anty-wzorzec; więcej linii = więcej do reviewu, większy surface attack, większy maintenance burden.
- **Tokens consumed** — input metric, nie output. Sensowny tylko jako składowa cost-per-successful-task.
- **Liczba dostępnych modeli / connectorów / MCP** — Sourcegraph/awesome-list-style, mówi o platformie, nie o produktywności.
- **Benchmarki SWE-bench / HumanEval na produkcji** — research paper "The Measurement Imbalance in Agentic AI Evaluation" (2026) pokazuje, że tylko 15% papers łączy technical + human dimensions; healthcare diagnostic agents osiągające 95% accuracy na benchmarku często lądują w doradczej roli, bo nie mierzą trust i workflow integration.

**Antywzorzec mierzenia, którego należy się wystrzegać:** Microsoft research z Jellyfish opisany w "Impact of AI-tooling on the Engineering Workspace" pokazuje, że samo wprowadzenie Copilota nie zmniejszyło czasu pracy nad repetitive task tak, jak się spodziewano — przesunęło efektywność. Z kolei "Beyond the Commit" (ICSE-SEIP 2026) pokazuje rozjazd między commit-based metrics a developer-perceived productivity. Wniosek: zbieraj zarówno hard metrics (merge rate, revert rate, time-to-fix), jak i okresowo perceived productivity od engineerów — bez tego drugiego stracisz subtelne efekty na morale i cognitive load.

---

## Implications for Octadecimal

Konkretne rekomendacje do pierwszego dokumentu projektowego nowego zespołu agentowego. Każdy punkt to decyzja, którą warto podjąć świadomie na początku, bo zmiana później jest kosztowna.

**1. Architektura: kontrolna płaszczyzna jest pierwszym deliverable, nie agenci.** Wzorzec konwergentny — OpenHands Agent Control Plane, GitHub Copilot Agent Control Plane, Coder Agents control plane — to nie przypadek. Najpierw: gateway do LLM (model-agnostic), sandbox runtime (Docker / micro-VM), centralne policy/budget, audit log per-konwersacja przypisany do usera, observability. Dopiero potem konkretni agenci. Praktyczna konsekwencja: jeśli zaczniemy od konkretnego agenta z lock-inem do LLM provider/OpenAI/IDE, refaktor wymiany kosztuje miesiące. Coder explicite ostrzega: "most agent tools are tightly coupled to a single provider's ecosystem, creating deeper lock-in".

**2. Operating model: trzykolumnowa matryca Delegate / Review / Own, per faza SDLC.** Zapożyczona z OpenAI playbook. Dla każdego procesu w zespole (planning, design, build, test, review, docs, deploy & maintain) napisz wprost, co agent robi sam, co człowiek weryfikuje i co zostaje wyłącznie człowiekiem. Bez tego dokumentu każdy inżynier improwizuje granicę i powstaje organizational debt. To jest też materiał na onboarding i materiał szkoleniowy.

**3. Pierwszy workflow: writer/reviewer loop, nie multi-agent fleet.** CooperBench: agenci współpracujący są ~50% słabsi niż solo. Devin: writer/reviewer podniósł merge rate z 34% do 67%. Octoco wprost: "start with the writer/reviewer loop. Two agents, one structured feedback cycle. This gives you multi-agent benefits with minimal coordination complexity." Konkretnie: agent A pisze PR, agent B (Bugbot-equivalent) review'uje, agent A wprowadza poprawki, człowiek mergeuje. Plan/execute split (Opus do planu, Sonnet/Haiku do execution) to drugi krok, nie pierwszy.

**4. Trigger event-driven, nie chat-driven.** IDE Automations pokazują, że największa wartość w skali to agenty triggerowane przez ticket utworzony, PR otwarty, push do main, alert PagerDuty, deploy, schedule. Chat-driven (developer prompt → agent action) skaluje się tylko do produktywności indywidualnej. Dla zespołu: zdefiniuj 3-5 triggerów (np. "Linear ticket z label `bug`" → triage agent, "PR opened" → review agent, "push to main" → security review, "PagerDuty incident" → log investigation, "daily 8:00" → test coverage backfill). Każdy trigger = jeden konkretny owner i jeden konkretny success metric.

**5. Verifier-first: testy/CI/lintery są pre-requirementem, nie nice-to-have.** Carlini: "the task verifier is nearly perfect, otherwise LLM will solve the wrong problem." To zmienia priorytety dokumentu projektowego: zanim wybierzemy modele i orchestrator, opisujemy, jakie testy/CI/linty/security scanners mamy w każdym repo, jak są greppable i czy ich output jest agent-friendly (single-line ERROR z reasonem, pre-computed aggregates, nie 10 000 linii logów). Bez tego cała reszta jest theater.

**6. AGENTS.md / AGENTS.md per repo, plus Playbooks dla powtarzalnych zadań.** OpenAI OpenHands i Cognition Devin konwergują na tym: per-repo plik z konwencjami (style, testowanie, security patterns, "forbidden actions") + reusable playbooks dla powtarzalnych przepływów (migracja, ingest danych, integracja z X). Playbook zawiera: outcome, kroki, postconditions, advice to correct priors, forbidden actions, required inputs. To jest tańsze i bardziej deterministyczne niż dotyczne tweakowanie promptów ad-hoc.

**7. Izolacja przez worktrees / dedicated workspaces dla każdego agenta.** CAID ablation pokazał istotny spadek wydajności bez izolacji — to nie jest cosmetic, to prerequisite. LLM provider kompilator: każdy agent w osobnym kontenerze, własny klon repo. Praktycznie: użyj `git worktree` lub spawnuj nowy sandbox per session; nigdy nie pozwalaj dwóm agentom edytować tych samych plików bez file reservation lease.

**8. Komunikacja agent-agent: structured JSON i git commits, nie chat.** MetaGPT 85.9% Pass@1 dzięki dokumentom; ChatDev wyraźnie słabszy z dialogiem. Octadecimal: jeśli będziemy mieli więcej niż jednego agenta w workflow, ich komunikacja przez plik plan/spec + commit messages, nie przez "powiedz drugiemu agentowi, co zrobiłeś".

**9. Metryki w MVP: merge rate, resolution rate, time-to-fix, cost-per-successful-task, revert rate.** I nic poza tym. Liczba sesji, tokeny, liczba "agent teammates" — wykluczyć z dashboardu na pierwszy rok. Plus okresowy survey perceived productivity (ICSE-SEIP 2026 ostrzeżenie o rozjeździe commit-based vs perceived).

**10. Granica scope per sesja: 4-8h junior work, dobrze zdefiniowany cel, brak mid-task scope change.** Devin operating envelope, ale potwierdzone wszędzie. Konsekwencja: jakość specyfikacji input → 60% wyniku. Inżynierowie którzy nie potrafią pisać dobrych spec staną się wąskim gardłem zespołu agentowego; warto wczesnie zainwestować w wewnętrzne szkolenie z "context engineering" / "writing specifications agents can execute".

**11. Faza pilot: jeden workflow, jedna metryka, jedno repo, 30 dni.** OpenHands rekomenduje exact same path: single workflow → controlled env → defined-in-code → connected to real systems → scale przez control plane. Antywzorzec: "zaczniemy od orchestratora 16 agentów, bo to demo LLM provider" — to projekt R&D, nie operating model.

**12. Wybór pierwszego workflow z najwyższym ROI / najniższym ryzykiem:**
   - **Vulnerability remediation z static analysis** (SonarQube/Veracode → agent → PR). Cognition: 5-10% developer time saved. Output mierzalny binarnie (CVE zamknięte / niezamknięte), low blast radius.
   - **Test generation backfill** (50-60% → 80-90% coverage). Mierzalny przez coverage tool. Output niskoryzykowny — testy gorszy scenariusz są pomijane przez code review.
   - **PR review reviewer (Bugbot-style)**. Resolution rate jako metryka outcome.
   - **Dokumentacja codebase'u** (DeepWiki-style indexing + auto-doc). Niska entropia, wysoka wartość onboardingowa, niskie ryzyko.

   Nie wybieraj jako pierwszego: nowy feature development end-to-end (mid-task scope change kills it), refaktor architektoniczny (wymaga senior judgment), customer-facing UI (wizualne osądy).

---

**Źródła rdzeniowe użyte w analizie** (najważniejsze, w kolejności praktyczności):

- [OpenAI — Building an AI-Native Engineering Team (OpenHands playbook)](https://developers.openai.com/openhands/guides/build-ai-native-engineering-team)
- [Cognition — How Cognition Uses Devin to Build Devin (Feb 2026)](https://cognition.ai/blog/how-cognition-uses-devin-to-build-devin)
- [Cognition — Devin's 2025 Performance Review](https://cognition.ai/blog/devin-annual-performance-review-2025)
- [LLM provider — Building a C compiler with parallel LLMs (Feb 2026)](https://www.llm-provider.com/engineering/building-c-compiler)
- [LLM provider / LLM — Common workflow patterns for AI agents (Mar 2026)](https://llm.com/blog/common-workflow-patterns-for-ai-agents-and-when-to-use-them)
- [OpenHands — Agent Control Plane (May 2026)](https://www.openhands.dev/blog/openhands-enterprise-agent-control-plane)
- [OpenHands / CMU — Effective Strategies for Asynchronous SWE Agents (CAID, Apr 2026)](https://www.openhands.dev/blog/asynchronous-software-engineering-agents)
- [Coder — Introducing Coder Agents (May 2026)](https://coder.com/blog/introducing-coder-agents)
- [IDE — Automations (Mar 2026)](https://ide.com/blog/automations)
- [IDE — Building Bugbot](https://ide.com/blog/building-bugbot) i [Bugbot self-improves with learned rules](https://ide.com/blog/bugbot-learning)
- [GitHub Blog — LLM and OpenHands in Copilot (Feb 2026)](https://github.blog/changelog/2026-02-26-llm-and-openhands-now-available-for-copilot-business-pro-users/)
- [Octoco — Multi-Agent Software Development (Apr 2026)](https://www.octoco.ai/blog/multi-agent-software-development) (świetna meta-analiza branży)
- [LLM provider / LLM — Eight trends defining how software gets built in 2026](https://llm.com/blog/eight-trends-defining-how-software-gets-built-in-2026)
- Research: CooperBench (arXiv 2601.13295), "Beyond the Commit" (ICSE-SEIP 2026), "Measurement Imbalance in Agentic AI Evaluation" (arXiv 2506.02064) — kontekst do metryk