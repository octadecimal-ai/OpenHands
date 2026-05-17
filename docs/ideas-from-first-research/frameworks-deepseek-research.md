# Raport rozpoznawczy: frameworki orkiestracji multi-agent dla automation assistant

**Dla:** Octadecimal (jednoosobowy software house)
**Data:** 2026-05-14
**Autor:** Senior Engineering Researcher
**Status:** Wersja robocza, przeznaczona dla założyciela technicznego

---

## 1. TL;DR

- **Dojrzały krajobraz, ale bardzo rozdrobniony.** Żaden framework nie dostarcza od razu governance + multi-team modeling + konteneryzacji. Trzeba będzie złożyć platformę z 2-3 komponentów, a warstwę reguł zbudować samodzielnie.
- **Ruflo (dawniej LLM Flow) jest najbliżej gotowego produktu** – 31k+ gwiazdek, 60+ agentów, 215 narzędzi MCP, self-learning memory – ale governance to wciąż ręczne promptowanie, a nie formalny rulebook.
- **OpenHands ma najlepszy model sandboxingu kontenerowego** – Docker z wieloma runtime'ami, MIT license, SDK dla agentów – ale automation assistant jest do niego podpinany przez ACP (Agent-Client Protocol), integracja dopiero się stabilizuje.
- **Mastra to cichy lider dla warstwy TypeScript** – Apache 2.0, observability, workflows, wsparcie LLM – świetnie pasuje do stacku Octadecimal.
- **Natywne Agent Teams automation assistant zmienia reguły gry.** Wszystkie nakładki orkiestracyjne, które duplikują funkcję już wbudowaną w automation assistant, tracą rację bytu – frameworki muszą robić coś ponad to (governance, observability, pamięć międzysesyjną).
- **Największa luka rynkowa:** nikt nie rozwiązał problemu deterministycznego governance z wielopoziomową eskalacją. Trzeba zbudować samemu.

---

## 2. Inventory

| Framework | Repo URL | Status utrzymania | Ostatnia istotna aktualizacja | Licencja | Overall fit-score (max 25) |
|---|---|---|---|---|---|
| **Ruflo (ex LLM Flow)** | [github.com/ruvnet/ruflo](https://github.com/ruvnet/ruflo) | Aktywny (5.8k+ commitów) | 2026-03-27 (v3.5.0) | MIT | 20 |
| **LLM-Squad (bijutharakan)** | [github.com/bijutharakan/multi-agent-squad](https://github.com/bijutharakan/multi-agent-squad) | Średnio aktywny | 2025-12-14 | Brak jawnie wskazanej | 12 |
| **BMAD-METHOD** | [github.com/TheDarkSkyXD/BMAD-METHOD-AI-Vibe-Planning-v6](https://github.com/TheDarkSkyXD/BMAD-METHOD-AI-Vibe-Planning-v6) | Aktywny (v6 Alpha) | 2025-12-27 | CC-BY-4.0 / MIT (kod) | 13 |
| **SuperLLM** | [PyPI: superllm](https://pypi.org/project/superllm/) | Aktywny (v4.3.0) | 2026-03-22 | MIT | 15 |
| **OpenHands** | [github.com/All-Hands-AI/OpenHands](https://github.com/All-Hands-AI/OpenHands) | Bardzo aktywny | 2026-05-01 (ciągłe) | MIT (core) | 22 |
| **Agent OS** | [github.com/buildermethods/agent-os](https://github.com/buildermethods/agent-os) | Aktywny (v3.0.0) | 2025-10-21 | MIT | 14 |
| **ContextForge** | [github.com/timeisenbuerger/codex-context-forge](https://github.com/timeisenbuerger/codex-context-forge) | Aktywny (v3.2.0) | 2025-12-17 | MIT | 11 |
| **Aider (multi-agent modes)** | [github.com/paul-gauthier/aider](https://github.com/paul-gauthier/aider) | Bardzo aktywny | 2026-05 (ciągłe) | Apache 2.0 | 10 |
| **Cline (ex LLM Dev)** | [github.com/cline/cline](https://github.com/cline/cline) | Bardzo aktywny | 2026-05 (ciągłe) | Apache 2.0 | 13 |
| **Roo Code** | [github.com/RooCodeInc/Roo-Code](https://github.com/RooCodeInc/Roo-Code) | Aktywny | 2026-04-23 | Apache 2.0 | 14 |
| **CrewAI** | [github.com/crewAIInc/crewAI](https://github.com/crewAIInc/crewAI) | Aktywny | 2026-05 (ciągłe) | MIT | 17 |
| **AutoGen (Microsoft)** | [github.com/microsoft/autogen](https://github.com/microsoft/autogen) | Aktywny | 2026-05 (ciągłe) | MIT | 15 |
| **LangGraph** | [github.com/langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) | Bardzo aktywny | 2026-05 (ciągłe) | MIT | 16 |
| **Letta Code** | [github.com/letta-ai/letta-code](https://github.com/letta-ai/letta-code) | Aktywny (v0.6.2) | 2025-12-16 | Apache 2.0 | 14 |
| **OpenAI Swarm / parruda/swarm** | [github.com/parruda/swarm](https://github.com/parruda/swarm) | Średnio aktywny | 2025-10-17 | MIT | 9 |
| **swarm-code** | [npm: swarm-code](https://www.npmjs.com/package/swarm-code) | Aktywny (v0.1.24) | 2026-03-14 | MIT | 13 |
| **Mastra** | [github.com/mastra-ai/mastra](https://github.com/mastra-ai/mastra) | Bardzo aktywny | 2026-03-28 | Apache 2.0 (core) | 19 |

---

## 3. Deep Dives

### 3.1 Ruflo (dawniej LLM Flow) – najbliżej kompletnego produktu

Ruflo to najbardziej dojrzały framework orkiestracji agentów dla automation assistant. Powstał jako osobisty eksperyment Reuvena Cohena w maju 2025, a do lutego 2026 przeszedł pełny rebranding z LLM Flow na Ruflo z całkowitą przebudową architektury na Rust/WASM. Obecnie ma 31k+ gwiazdek na GitHubie, 100k+ aktywnych użytkowników miesięcznie i 5800+ commitów.

**Architektura:** Model "hive mind" z Queen Agent na szczycie koordynującą 60+ wyspecjalizowanych sub-agentów. Komunikacja przez MCP (Model Context Protocol). System zawiera AgentDB (SQLite + HNSW dla semantycznego wyszukiwania, 150x szybszego), consensus algorithm (Raft, Byzantine, Gossip), drift control, ONNX Runtime dla lokalnych embeddingów. Trzy warstwy routingu modeli redukują zużycie API o 75%.

**Governance:** Brak formalnego rulebooka. SPARC (Specification, Pseudocode, Architecture, Refinement, Completion) to metodologia workflow, nie system reguł. W v3.5 dodano MutationGuard z kryptograficzną weryfikacją zapisów i AttestationLog, ale to wciąż zabezpieczenia techniczne, a nie warstwa governance w rozumieniu Octadecimal. Agent może samodzielnie modyfikować swój AGENTS.md, co jest problemem udokumentowanym przez społeczność automation assistant.

**Konteneryzacja:** Działa jako MCP server lub standalone CLI. Brak natywnej konteneryzacji Docker – instaluje się przez `npx` i odpala jako daemon na hoście. To duży minus dla architektury Octadecimal (Mac host + Docker containers).

**Ostre krawędzie:** 417 otwartych issues na GitHubie (stan na maj 2026). Systematyczny bug `classifyHandoffIfNeeded is not defined` dotykający 100% agentów. Problemy z rebrandingiem – statusline wciąż pokazuje stare nazwy. Hardcodowane prefixy MCP, które nie działają po zmianie nazwy pakietu. Memory leak w rejestrze instancji. To nie są drobnostki – to oznaki zbyt szybkiego wzrostu i niedostatecznego testowania.

**Licencja:** MIT – czysta, komercyjna, bez haczyków.

### 3.2 OpenHands – najlepszy model sandboxingu i otwartości

OpenHands (dawniej OpenDevin) przeszedł fundamentalną transformację w styczniu 2026 wraz z wydaniem Software Agent SDK. To już nie jest webowa aplikacja do chatu z agentem – to platforma agentowa z własnym SDK, MIT-licencjonowanym, pozwalającym budować własne agenty kodujące w kilku linijkach kodu.

**Architektura:** Event-driven z Agent-Client Protocol (ACP). OpenHands pełni rolę warstwy abstrakcji – możesz podpiąć automation assistant, Gemini CLI, Codex CLI jako back-endy agentowe, zachowując wspólny interfejs. Trwają intensywne prace nad zrównaniem API delegacji z natywnym automation assistant Task tool.

**Konteneryzacja:** To tutaj OpenHands błyszczy. Dwa typy kontenerów Docker: aplikacyjny (orchestrator) i runtime'owy (sandbox dla agentów). Multi-runtime support pozwala uruchamiać agenty w izolowanych środowiskach Docker z pełną separacją. MIT-licensed obrazy Docker. Idealne dla architektury Octadecimal – Mac host, Linux containers.

**Governance:** Brak wbudowanego rulebooka. Jako platforma agentowa, OpenHands daje narzędzia (hooks, permission system), ale nie dostarcza gotowej warstwy reguł biznesowych. To jest do zbudowania na wierzchu.

**Ostre krawędzie:** Heavy dependency – 70+ pip packages. Legacy system (V0) wciąż obecny, z planowanym usunięciem na kwiecień 2026, co sugeruje pewną niestabilność architektoniczną w okresie przejściowym. Integracja z automation assistant przez ACP jest w fazie implementacji, nie produkcji. Młode SDK (4 miesiące od premiery) – brak referencji produkcyjnych.

**Licencja:** MIT dla core, enterprise/ ma osobną licencję. Czysto dla celów Octadecimal.

### 3.3 Mastra – TypeScript-first, observability-first

Mastra to TypeScriptowy framework agentowy zbudowany na Vercel AI SDK. 11.3k gwiazdek, używany przez duże firmy do wewnętrznej automatyzacji AI. Apache 2.0 od lipca 2025.

**Architektura:** Trzy filary: Agents (LLM + tools + workflows), Workflows (durable graph-based state machines z OpenTelemetry tracing), RAG (ETL pipeline z vector search). Model-agnostic przez Vercel AI SDK – LLM, GPT, Gemini, Llama przez jeden interfejs. Agents mogą wywoływać inne agents, tworząc hierarchię. Każdy krok workflow ma wbudowany tracing OpenTelemetry.

**automation assistant integration:** Nie jest to first-class integration w sensie "uruchamiam automation assistant CLI". Mastra używa LLM przez API LLM provider, a nie przez automation assistant. Dla Octadecimal to oznacza dodatkową warstwę integracji – chyba że akceptujesz model API-zamiast-CLI.

**Governance:** Workflows Mastra mają wbudowane: human-in-the-loop (czekanie na input), error handling, retries, conditional branching. Ale to governance na poziomie flow, nie rulebooka między zespołami agentów. Brak natywnego systemu reguł z eskalacją.

**Ostre krawędzie:** Dual-licensing – core Apache 2.0, ale katalogi `ee/` są source-available pod Mastra Enterprise License. Trzeba uważać co się importuje. Sub-agenty nie forwardują reasoning events w streamie – zgłoszone jako bug. Brakuje natywnego "automation assistant"-style behavior – trzeba ręcznie implementować planowanie i orkiestrację sub-agentów.

**Docker:** Mastra działa na Node.js, może być konteneryzowana standardowo. Brak dedykowanego rozwiązania sandboxingu, ale to nie problem – sandboxing powinien być warstwą niżej (OpenHands lub własny).

### 3.4 CrewAI – najwięcej userów, najwięcej ograniczeń

CrewAI to Pythonowy framework z 47k+ gwiazdkami, MIT license, zbudowany wokół koncepcji "Crews" – zespołów agentów z rolami. Ma największą bazę użytkowników wśród frameworków multi-agent.

**Architektura:** Role-based agents (Agent, Task, Crew, Process). Dwa tryby: Crews (collaborative multi-agent groups) i Flows (event-driven, stateful). Pamięć short/long-term. Integracja z LLM przez API LLM provider, nie przez automation assistant CLI. Dostępny jest "Agent Workflow Designer" jako skill dla automation assistant, ale to zewnętrzny dodatek.

**Governance:** CrewAI aktywnie inwestuje w governance w 2026 – webinary z Galileo, "Flows architecture" z deterministycznym routingiem, obserwowalną egzekucją i ścieżkami eskalacji. To najdojrzalsza propozycja governance wśród badanych frameworków. Jest też integracja z Galileo Agent Control – zewnętrznym control plane dla agentów.

**Ostre krawędzie:** Python-only – nie pasuje do stacku TypeScript dla MCP. Brak integracji z automation assistant jako CLI – tylko API. "Agents still have no schema" – krytyka, że brakuje formalnej walidacji outputów agentów. Do pełnej observability potrzebuje zewnętrznych narzędzi (LangSmith, Arize, Langfuse).

### 3.5 Cline + Roo Code – IDE-first, nie platforma

Oba to rozszerzenia VS Code (Apache 2.0). Cline (58k+ gwiazdek) jest oryginałem, Roo Code (22k+ gwiazdek) forkiem. Cline potrafi spawn-ować automation assistant CLI jako sub-agenty, co jest ciekawym wzorcem orkiestracji, ale fundamentalnie są to narzędzia IDE, a nie platformy orkiestracyjne.

**Cline:** Wieloagentowa orkiestracja przez `llm-code-subagents.md` rule. Spawnuje automation assistant CLI z różnymi permission modes (w tym `bypassPermissions`). Wzorce: Parallel Variations (Midjourney for Code), Parallel Features on Existing Codebase. Ciekawe dla fazy prototypowania, za lekkie dla platformy produkcyjnej.

**Roo Code:** Ma Orchestrator Mode z hub-and-spoke architecture. Aktywnie rozwija hierarchiczne workflow (Issue #6298). Problem: "Lack of Predictability and Stability" – orchestrator dynamicznie decyduje o następnym kroku, może pomijać krytyczne etapy. To dokładnie przeciwieństwo governance, którego Octadecimal potrzebuje.

---

## 4. Buy / Borrow / Build

| Framework | Klasyfikacja | Uzasadnienie |
|---|---|---|
| **Ruflo** | **Borrow** (wzorce, nie kod) | Architektura swarm, AgentDB, wzorce MCP – skopiować koncepcje. Nie adoptować: za dużo bugów, brak governance, brak konteneryzacji. |
| **OpenHands** | **Buy** (adoptować jako warstwę sandboxingu) | MIT license, Docker-native, SDK dla agentów. Idealne jako warstwa wykonawcza dla kontenerów dev teams. Nie zapewnia governance – to zbudować na wierzchu. |
| **Mastra** | **Buy** (adoptować jako warstwę orkiestracji TypeScript) | Apache 2.0, TypeScript, observability, workflows. Dobrze pasuje do stacku. Brakuje natywnego automation assistant CLI supportu – trzeba dodać adapter. |
| **CrewAI** | **Borrow** (wzorce governance i flows) | Najlepsze wzorce governance w ekosystemie. Nie adoptować – Python, API-only, nie pasuje do TypeScript/CLI stacku. |
| **Cline / Roo Code** | **Build** (nie używać jako platformy) | Za lekkie, IDE-first, brak deterministycznego governance. Wzorzec spawn-owania automation assistant CLI można wykorzystać we własnym rozwiązaniu. |
| **BMAD-METHOD** | **Skip** | Ciekawe metodologicznie (21 agentów, scale-adaptive intelligence), ale zbyt mocno związane z konkretnym IDE, problemy z discoverability komend slash. Licencja CC-BY-4.0 dla dokumentacji to potencjalny problem. |
| **SuperLLM** | **Skip** | Ciekawy pomysł (meta-programming configuration framework), ale za dużo bugów instalacyjnych, problemy z kompatybilnością macOS, community zbyt małe. |
| **Agent OS** | **Borrow** (wzorce spec-driven development) | Pomysł konwersji standardów na automation assistant Skills jest wart skopiowania. Sam framework za prosty dla potrzeb Octadecimal. |
| **LangGraph** | **Borrow** (wzorce grafowe) | MIT license, stateful graphs, ale LangGraph Platform jest proprietary. Dobre do studiowania wzorców, nie do adopcji jako całość. |
| **AutoGen** | **Skip** | MIT license, ale Microsoft – ryzyko vendor lock-in. Python-only, nie pasuje do stacku. |
| **Letta Code** | **Borrow** (wzorzec pamięci) | Persisted agents z long-term memory to koncept, który trzeba ukraść. Sam framework ma tylko 142 gwiazdki, zbyt mała społeczność. |
| **swarm-code / parruda/swarm** | **Skip** | Ciekawe eksperymentalnie, za mało dojrzałe. |

---

## 5. Top 3 Recommendations

### Rekomendacja 1: OpenHands jako warstwa sandboxingu + Mastra jako warstwa orkiestracji + własny governance layer

**Opis:** OpenHands zapewnia Docker-runtime'y dla każdego zespołu agentów. Mastra dostarcza TypeScript-ową orkiestrację (workflows, agents, observability). Własny komponent Octadecimal Governance Layer implementuje rulebook z 3-poziomową eskalacją, wykorzystując automation assistant hooks i MCP.

**Trade-off:** Składasz platformę z 2 frameworków, które nie były projektowane do współpracy. Koszt integracji będzie wyższy niż adopcja pojedynczego rozwiązania. Ale żaden pojedynczy framework nie spełnia wymagań.

### Rekomendacja 2: Ruflo jako baza z własnym governance

**Opis:** Ruflo daje 60+ agentów, swarm coordination, memory, MCP tools. Dodać warstwę governance jako MCP server, który przechwytuje tool calls i egzekwuje rulebook przed wykonaniem. Docker wrapper dookoła.

**Trade-off:** Ruflo ma 417 otwartych issues i systematyczne bugi. Jesteś na łasce roadmapy jednoosobowego maintainera (Reuven Cohen). Ale dostajesz najwięcej funkcjonalności od razu.

### Rekomendacja 3: Build – własny, minimalistyczny orchestrator na automation assistant Agent Teams + MCP

**Opis:** automation assistant ma teraz natywne Agent Teams (od lutego 2026). Zamiast nakładać ciężki framework, zbudować lekki orchestrator w TypeScript, który: (a) definiuje zespoły jako AGENTS.md z różnymi rulebookami, (b) używa MCP do komunikacji między zespołami, (c) implementuje 4-warstwową propagację wiedzy przez współdzielony vector store, (d) używa `colmena` (lub własnego rozwiązania) jako deterministycznej warstwy governance.

**Trade-off:** Najwięcej pracy, największe ryzyko, że zbudujesz coś, co już istnieje. Ale pełna kontrola nad architekturą i zero zależności od zewnętrznych roadmap. automation assistant Agent Teams mogą w 2027 uczynić zewnętrzne orchestratory zbędnymi – buildując własny, jesteś najbliżej metalu.

**Moja rekomendacja:** Rekomendacja 3 (Build) z horyzontem 3 miesięcy na MVP, ale z równoległym POC Rekomendacji 1 (OpenHands + Mastra) jako Plan B. Jeśli po 6 tygodniach własny orchestrator nie będzie stabilny, przełączasz się na Plan B.

---

## 6. Open Questions

1. **Czy automation assistant PreToolUse hooks da się użyć do deterministycznego governance?** RFC #45427 udokumentował 4 failure modes: subagent bypass, silent hook failure, model self-modification, alternative tool paths. Bez odpowiedzi LLM provider na to RFC, każda warstwa governance zbudowana na hookach będzie dziurawa. **Hands-on test:** zbudować hook, który blokuje Write i próbować 100 sposobów obejścia.

2. **Jak bardzo stabilne jest OpenHands SDK?** Wydane w styczniu 2026, wciąż w fazie aktywnego developmentu. API delegacji dopiero jest przepisywane, by dorównać automation assistant Task tool. **Hands-on test:** zbudować agenta w OpenHands SDK, który deleguje do automation assistant przez ACP i zmierzyć stabilność na 100-task benchmarku.

3. **Czy Mastra `agent.network()` jest wystarczająca dla 7+ zespołów?** Dokumentacja jest skąpa. Bug z missing reasoning events w sub-agentach sugeruje, że multi-agent to wciąż drugorzędny feature. **Hands-on test:** skonfigurować 7 agentów Mastra z różnymi rulebookami i zmierzyć, czy komunikacja między-agentowa działa niezawodnie.

4. **Jak zachowuje się Ruflo w kontenerze Docker?** Oficjalnie nie jest wspierane. Użytkownicy zgłaszają problemy z daemon mode. **Hands-on test:** spakować Ruflo w Docker, uruchomić swarm 8 agentów, zmierzyć stability i resource usage.

5. **Czy `colmena` (local-first governance layer) realnie blokuje 100% nieautoryzowanych tool calls?** Projekt ma 15 dni (powstał 5 maja 2026), zero production track record. Obiecuje <15ms latency, zero LLM calls w hot path. **Hands-on test:** skonfigurować colmena z 50 regułami, puścić 1000 złośliwych promptów, zmierzyć false-positive/false-negative rate.

---

## 7. Red Flags

| Framework | Red Flag | Severity |
|---|---|---|
| **Ruflo** | 417 otwartych issues, systematyczny bug `classifyHandoffIfNeeded` (100% agentów), rebranding w trakcie – potencjalne porzucenie lub pivot | **HIGH** |
| **LLM-Squad (bijutharakan)** | Ostatni commit ~6 miesięcy temu, brak licencji w README, tylko 1 autor | **HIGH** – prawdopodobnie abandoned |
| **BMAD-METHOD** | Ciężkie problemy z discoverability slash commands w automation assistant (5 osobnych issues), hardcodowana ścieżka `~/Dev/`, model "expansion packs" pachnie vendor lock-in | **MEDIUM** |
| **SuperLLM** | Bug kasujący lokalną instalację automation assistant, problemy z instalacją na macOS, community zbyt małe (głównie 1 maintainer) | **MEDIUM** |
| **Letta Code** | Tylko 142 gwiazdki, platforma Letta ma pricing ($20/miesiąc za API), co podważa "open-source" narrację | **LOW-MEDIUM** |
| **LangGraph Platform** | LangGraph biblioteka jest MIT, ale Platform (deployment, persistence) jest proprietary – klasyczny open-core vendor lock-in | **MEDIUM** |
| **CrewAI** | Python-only, brak automation assistant CLI integracji, governance zależne od zewnętrznych narzędzi (Galileo) | **MEDIUM** |
| **Roo Code** | "Lack of Predictability" w orchestrator mode – AI dynamicznie decyduje o krokach, może pomijać krytyczne etapy. Dokładnie przeciwieństwo deterministycznego governance | **HIGH** |
| **swarm-code** | 0.1.24 – pre-alpha. README wspomina o arXiv:2512.24601 (Recursive Language Model), co brzmi jak research project, nie production tool | **HIGH** |

---

## Źródła

- Ruflo GitHub: https://github.com/ruvnet/ruflo/issues/945 (dostęp 2026-05-14), https://github.com/ruvnet/ruflo/issues/1240 (dostęp 2026-05-14)
- Ruflo bugi: https://github.com/ruvnet/ruflo/issues/1431, #1280, #1109, #1391, #1339 (dostęp 2026-05-14)
- LLM Flow → Ruflo historia: https://dev.to/stevengonsalvez/llm-flow-the-multi-agent-swarm-orchestrator-before-it-got-a-new-name-4kd4 (dostęp 2026-05-14)
- OpenHands SDK: https://openhands.dev/blog/2026-01-08-introducing-openhands-sdk (dostęp 2026-05-14)
- OpenHands ACP integracja: https://github.com/OpenHands/software-agent-sdk/issues/590 (dostęp 2026-05-14)
- OpenHands delegacja: https://github.com/OpenHands/software-agent-sdk/issues/2057 (dostęp 2026-05-14)
- OpenHands kontenery: https://deepwiki.com/All-Hands-AI/OpenHands/2-deployment-container-architecture (dostęp 2026-05-14)
- Mastra: https://github.com/mastra-ai/mastra (dostęp 2026-05-14)
- Mastra license: https://mastra.ai/blog/mastra-is-now-apache-2-0-licensed (dostęp 2026-05-14)
- Mastra sub-agent bug: https://github.com/mastra-ai/mastra/issues/11123 (dostęp 2026-05-14)
- CrewAI governance: https://blog.crewai.com/building-agent-security-in-the-wrong-order (dostęp 2026-05-14), https://www.tipranks.com/news/company-announcements/galileo-targets-enterprise-ai-governance-with-multi-agent-control-focus (dostęp 2026-05-14)
- automation assistant Agent Teams: https://www.sitepoint.com/llm-provider-llm-code-agent-teams/ (dostęp 2026-05-14)
- automation assistant governance RFC: https://github.com/llm-providers/llm-code/issues/45427 (dostęp 2026-05-14)
- automation assistant "Fake Done": https://dev.to/catadef/fake-done-your-ai-coding-agent-says-it-finished-it-didnt-5b6f (dostęp 2026-05-14)
- Colmena: https://github.com/4rth4S/colmena (dostęp 2026-05-14)
- Cline sub-agenty: https://deepwiki.com/cline/prompts/5-orchestration-and-automation (dostęp 2026-05-14)
- Roo Code orchestrator: https://github.com/RooCodeInc/Roo-Code/issues/6298 (dostęp 2026-05-14)
- Reddit agent landscape: https://dev.to/patty_wingfield_d285feb08/from-agent-teams-to-boring-plumbing-ten-reddit-threads-mapping-ai-agents-in-may-2026-39pc (dostęp 2026-05-14)
- Multi-agent porównanie: https://www.morphllm.com/blog/ai-agent-frameworks-2026 (dostęp 2026-05-14)
- Licencje: sprawdzone przez `pip show` / `npm view` / GitHub LICENSE files dla każdego frameworku (dostęp 2026-05-14)