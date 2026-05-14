# Scrum i rytuały Scrumowe dla zespołów agentów AI

## TL;DR

- Scrum dla zespołów agentów AI ma sens tylko tam, gdzie służy jako **ramka feedback‑loopów dla człowieka‑„agent managera”**, a nie jako teatr, w którym boty „udają ludzi”.[^1_2][^1_3]
- Praktycy raportują realną wartość z **planowania, krótkich sprintów i retrospektyw**, ale w formie: asynchroniczne logi, automatyczne raporty, reguły systemowe i pamięć długoterminowa – nie spotkania z „mówiącymi” agentami.[^1_4][^1_5][^1_1]
- **Daily stand‑up w klasycznej formie jest w dużej mierze zbędny dla agentów** – większość tego, co „powiedziałby” agent, i tak jest w obserwowalności; realna wartość to alerty odchyleń, nie rytuał.[^1_6][^1_1][^1_4]
- **Retrospektywa i knowledge propagation** są najmocniejszym uzasadnieniem Scrum‑opodobnego cyklu: praktycy Claude Code, BMAD i narzędzi retro/lessons budują na tym trwałe artefakty (CLAUDE.md, retro.md, lessons.md, globalne zasady), które poprawiają kolejne iteracje.[^1_7][^1_8][^1_5][^1_9]
- Dla jednoosobowego software house’u najbardziej sensowna jest **kadencja epizodyczna (intent → done) z cienką warstwą 2–3‑dniowych sprintów**, zautomatyzowanym „/retro → rules update” i bardzo lekką definicją velocity.[^1_10][^1_11][^1_12]

---

## 2. Uczciwa ocena: Scrum‑for‑AI – substancja czy teatr?

### Co mówią praktycy i konsultanci

Poważniejsze teksty „Scrum + AI” mocno podkreślają, że próba wsadzenia 24/7 agentów w **niemodyfikowany Scrum** kończy się źle: przepełnione sprinty, martwe velocity, dług techniczny. Artykuł o AI‑augmented Scrum opisuje, że przy botach wykonujących pracę deweloperów klasyczne ceremonie trzeba przeprojektować na **asynchroniczne monitorowanie odchyleń i debugging agentów**, a nie rytuały statusowe.[^1_1]

Scrum.org i konsultanci wprost piszą, że Scrum z agentami ma sens tylko wtedy, gdy **traktuje się agentów jako zasoby wykonawcze, a Scrum jako pętlę inspekcja‑adaptacja dla ludzi** – Product Owner kuratoruje, jak AI jest używany, Scrum Master staje się orkiestratorem automatyzacji, a daily to raczej synchronizacja na bazie logów niż rozmowa.[^1_13][^1_3]

Stevo („What I Learned Running 19 Sprints With AI Agents”) po 19 sprintach z agentami zauważa, że **multi‑agent „team theatre” często przegrywa z pojedynczym mocnym agentem + człowiek na sterze**, zwłaszcza przy mniejszych repozytoriach. Jego wniosek: *„Default should be single‑agent until you hit context limits or have genuinely independent workstreams that justify the coordination cost.”*[^1_12]

Na r/ClaudeAI i wokół Claude Code dominuje pragmatyzm: ludzie budują **/groom → /implement → /retro → /lessons** jako self‑learning loop dla Claude’a, ale jest to podporządkowane wydajności, a nie „pełnemu Scrumowi”. W wątku „Claude Code workflow tips after 6 months of daily use” senior dev opisuje własny **/retro skill, który aktualizuje pamięć i CLAUDE.md**, a społeczność pisze wprost: *„The retro one hits different when you actually feed it back into the next sprint.”*[^1_8][^1_14][^1_7]

### Gdzie jest teatr?

- **Daily stand‑up z agentami mówiącymi w kółku, „co zrobiły”** – powszechnie bezwartościowy; sens ma automatyczne raportowanie stanu i wyjątków.[^1_4][^1_6][^1_1]
- **Liczenie story points dla botów** – praktycy mówią wprost, że trzeba przejść na metryki compute/tokenów i throughputu zadań, bo klasyczne velocity degraduje do vanity metric.[^1_15][^1_6][^1_1]
- **Multi‑agent role‑play (PM, Architect, Dev, QA) w małych projektach** – BMAD i podobne kadencje pokazują wartość struktury, ale same role‑play’e bez dyscypliny artefaktów szybko stają się show bez trwałego efektu.[^1_16][^1_17]

### Gdzie jest substancja?

- **Krótkie, silnie obserwowalne sprinty (1–3 dni)** z wyraźnymi celami są rekomendowane w środowisku AI‑driven, bo 2‑tygodniowe sprinty zbierają za dużo zmian, by sensownie je zreviewować.[^1_11][^1_10]
- **Retrospektywy z logami tokenów, trace’ami akcji i promptami** jako materiałem do debugowania workflowu agentów (a nie nastrojów zespołu) są wskazywane jako kluczowy mechanizm podnoszenia jakości.[^1_5][^1_9][^1_1]
- **Systematyczna „lekcja → reguła → pamięć”**: narzędzia retro dla Claude Code generują retro.md i lessons.md, z mechanizmami wynoszenia lekcji do projektowej CLAUDE.md lub globalnych zasad – to jest faktyczna continuous improvement.[^1_9][^1_18][^1_5]

Wniosek: **Scrum dla agentów ma sens jako warstwa zarządzania wiedzą, feedback‑loopów i priorytetów dla człowieka‑operatora, nie jako antropomorficzny teatr.** Kadencja musi być skrócona, asynchroniczna i podparta telemetryką.[^1_3][^1_1]

---

## 3. Ocena ceremonii Scrumowych (keep / modify / drop)

### Planning

**Techniczna potrzeba**

Agentic coding narzędzia (Sweep, Aider, Mentat) oraz Devin/Devon pokazują, że agentom realnie służy **upfront plan / decomposition**, zanim ruszą w długą pętlę akcji. Devin jest z definicji agentem, który „planuje i wykonuje złożone zadania wymagające tysięcy decyzji”, co przypomina mini‑sprint plan, ale wykonywany w ramach jednego epizodu.[^1_19][^1_20][^1_21][^1_22]

Sweep ma osobny „Planning mode”, w którym LLM generuje plan reviewowany przez człowieka, a dopiero potem przekazywany jest do trybu Agent. Oficjalny docs wprost radzi: **„one chat per task”** i jedno zadanie na wątek – to jest bardziej epizod niż klasyczny sprint backlog.[^1_21]

W Claude Code praktycy budują dedykowane **/groom lub /plan** dla pojedynczego feature’u / zadania, nie tablice sprintowe z Jiry. BMAD używa agenta‑PM do generowania PRD i architekta do projektowania struktury systemu, co jest de facto fazy analysis + planning, ale niekoniecznie time‑boxed sprint planning.[^1_17][^1_14][^1_16][^1_8]

**Werdykt – keep / modify / drop**

- **Zachować, ale mocno przeformatować (KEEP/MODIFY).**
- Dla agentów lepiej działa **episode backlog**: konkretne intents (tickets) z planem wykonania i warunkami zakończenia.
- W Octadecimal ma sens:
  - lekkie planning co 2–3 dni (batch epizodów),
  - silne planning per epizod: /plan generuje plan, founder zatwierdza, orchestrator agent wykonuje.

---

### Daily standup (Daily Scrum)

**Techniczna potrzeba**

Daily w Scrumie służy inspekcji postępu i adaptacji planu. W AI‑augmented Scrum autorzy wprost piszą, że przy botach **Daily Scrum powinien stać się asynchronicznym przeglądem logów i odchyleń**, zamiast meetingu z udziałem agentów („Your AI agents don't need coffee, but they do need strict oversight”).[^1_23][^1_1]

Autonomous reporting narzędzia pokazują, że agenci świetnie nadają się do **ciągłego generowania sprint reports, backlog status, flagowania niezsynchronizowanych PR‑ów, zaległych reviewów, flakiness testów** – bez rytualnego standupu. Integracje agentów z Jira (Aziro, RelevanceAI) stawiają na **ciągłe wykrywanie bottlenecków, predykcję ryzyka sprintu, automatyczne statusy i reasignacje** – to „perpetual standup”.[^1_24][^1_6][^1_4]

**Werdykt – keep / modify / drop**

- **Porzucić klasyczną formę (DROP).**
- Zastąpić ją:
  - automatycznym dziennym raportem generowanym przez agenta (AgentOps),
  - krótkim (5–10 min) przeglądem przez Foundera, opcjonalnie korekta priorytetów.
- Zero „what did you do yesterday/ today” dla agentów – to jest w telemetryce i logach.[^1_6][^1_1][^1_4]

---

### Refinement (Backlog Refinement / Grooming)

**Techniczna potrzeba**

LLM‑y działają dużo lepiej, gdy zadania są **dobrze opisane, mają klarowne constraints i strukturę I/O** – to jest dokładnie cel backlog refinement. W Claude Code praktycy budują **/groom /grooming** skills, które przekształcają luźne pomysły w dobrze określone zadania, plany i check‑listy.[^1_14][^1_25][^1_22][^1_8][^1_21]

Jednocześnie w jednym z wątków o budowaniu self‑learning Scrum workflow pada ostrzeżenie: zbyt rozbudowane „sprint frameworks” w wąskich skillsach deweloperskich prowadzą do clutteru – „Claude tends to provide more context than necessary… detailed sprint frameworks for a development agent focused solely on coding.”[^1_14]

**Werdykt – keep / modify / drop**

- **Zachować w formie zautomatyzowanej (KEEP/MODIFY).**
- Refinement ma sens, jeśli:
  - outputem jest „spec do zjedzenia przez agenta” (przemyślany prompt + kontekst z repo),
  - jest prowadzony przez slash skills (/groom, BMAD‑Analyst/PM), a nie długie spotkanie.
- Dla Octadecimal:
  - /groom jako podstawowe wejście do epizodu,
  - specy w markdown (PRD.md, TASK.md) konsumowane przez orchestrator‑agenta.[^1_25][^1_16][^1_17]

---

### Sprint review

**Techniczna potrzeba**

W AI‑heavy zespołach praktycy piszą, że **2‑tygodniowe sprinty są za długie** – sprint review co 2–3 dni jest „just right”, bo liczba elementów do omówienia jest jeszcze strawna. Review jest bardziej **przeglądem wyników, artefaktów i metryk** niż show‑and‑tell.[^1_10]

Gdy klient = PO = dev manager (jak u Ciebie), klasyczny review może wydawać się redundantny. Z drugiej strony, AI‑native patterns (np. talk o 4 patterns of AI‑native dev) pokazują wartość w **sformalizowanym zamknięciu epizodu**: testy, PR, dokumentacja, knowledge update zamiast „ciągłego niedokończenia”.[^1_26]

**Werdykt – keep / modify / drop**

- **Zmodyfikować, często wchłonąć w retro (MODIFY).**
- Rola Sprint Review w Octadecimal:
  - checklistowe potwierdzenie Definition of Done (PR merged, testy zielone, docs zaktualizowane),
  - snapshot metryk (czas, koszt, interwencje) dla retro,
  - może być krokiem wstępnym do retrospektywy, nie osobnym meetingiem.[^1_26][^1_10]

---

### Retrospective

**Techniczna potrzeba**

Artykuł „AI‑Augmented Scrum Framework” jest bezlitosny: **„A retrospective without analyzing your AI's token logs is just a complaining session.”** Retrospektywa w środowisku agentów ma służyć **systematycznemu debugowaniu workflowu, optymalizacji promptów i narzędzi**, nie wentylacji emocji.[^1_1]

Claude Code ekosystem ma cały cluster retro tools:

- **Retro skill** – „end‑of‑session analysis”, generuje retro.md i lessons.md, z „adaptive depth system”.[^1_5]
- **Development Retrospective** – zawiera „lesson graduation”, czyli wynoszenie krytycznych insightów do CLAUDE.md lub globalnych reguł.[^1_9]
- **Sprint Retro Facilitator** i **reviews‑retros‑reflection** – strukturyzowane retro (Start/Stop/Continue, 4Ls) z naciskiem na akcje i owners.[^1_27][^1_28][^1_29]
- Playbook „Lessons Learned” – uznany pattern: Successes / Problems / Actions / Process Changes / Knowledge transfer.[^1_18]

W wątku o Claude Code workflow senior dev opisuje /retro skill aktualizujący CLAUDE.md; komentarze podkreślają, że wartość retro pojawia się dopiero, gdy wnioski faktycznie trafiają do pamięci i kolejnych sesji.[^1_7]

**Mechanizmy poprawy między sprintami**

- zmiany w system prompts / policies agentów,
- zmiany konfiguracji toolingu (jakie testy agent odpala, jakie heurystyki ma orchestrator / security analyzer),[^1_30]
- aktualizacja semantic memory (CLAUDE.md / knowledge graph),
- modyfikacja architektury multi‑agent (np. powrót do single‑agent, jak w wnioskach z 19 sprintów).[^1_12]

**Werdykt – keep / modify / drop**

- **Zachować i postawić w centrum (KEEP++).**
- Retrospektywa staje się głównym rytuałem: wszystko inne wspiera pętlę „epizody → metryki → retro → reguły/pamięć → lepsze epizody”.[^1_5][^1_9][^1_1]
- W Octadecimal:
  - co 2–3 dni, 30 minut max,
  - RetroAgent przygotowuje draft (retro.md, proposal rules updates),
  - Founder zatwierdza / częściowo edytuje, agent wprowadza zmiany w plikach i konfiguracji.

---

### Knowledge propagation

**Techniczna potrzeba**

Produkcyjne systemy agentowe potrzebują **warstwowej pamięci: semantic, episodic, procedural**, aby unikać „ciągłego zaczynania od zera”. Blog Redis o long‑term memory mówi wprost: „Most production systems end up using a mix of all three… Episodic memory often getting consolidated into semantic memory over time.”[^1_31][^1_32][^1_33]

Voyager w Minecraft, Contextual Experience Replay (CER) i Just‑In‑Time RL pokazują, że **agent musi mieć mechanizmy konsolidacji doświadczeń i selekcji pamięci**, inaczej będzie powtarzać te same błędy w nowych zadaniach.[^1_34][^1_35][^1_36]

Mem0 i pokrewne pipeline’y proponują: **episodic → refleksja → semantic** (fakty, reguły, preferencje) z mechanizmami priorytetyzacji i decay.[^1_32][^1_37]

Claude Code ekosystem: **CLAUDE.md jako root semantic memory** plus retro.md, lessons.md, session logs – społeczność rekomenduje „breadcrumbs” i automatyzację /retro do aktualizacji tych plików.[^1_18][^1_7][^1_5]

**Werdykt – keep / modify / drop**

- **Najważniejsza „ceremonia”, ale w formie pipeline’u danych, nie spotkania (KEEP, but as architecture).**
- W praktyce jest to:
  - architektura pamięci (patrz kolejna sekcja),
  - proces retro → lessons → reguły / knowledge graph,
  - mechanizmy awansu lekcji (lokalna → projektowa → globalna).[^1_33][^1_31][^1_32]

---

## 4. Wzorce propagacji wiedzy – architektury pamięci w produkcji

### 4.1. Warstwy pamięci w agentach

Źródła produkcyjne i papers opisują zgodny model:

- **Semantic memory** – fakty, reguły, relacje, preferencje; często hybryda: vector DB, metadata + knowledge graph.[^1_38][^1_31][^1_33]
- **Episodic memory** – time‑indexed doświadczenia: rozmowy, task runs, tool calls, błędy.[^1_31][^1_33]
- **Procedural memory** – „skills and routines”: prompts, policies, agents code, workflow graphs.[^1_39][^1_33]

Redis i AI Practitioner podkreślają, że w produkcji **semantyczna pamięć jest utrzymywana poza LLM** (persist), a RAG to główny mechanizm zasilania agentów w wiedzę przed planowaniem/akcją.[^1_32][^1_33][^1_31]

### 4.2. Pipeline: od logów do semantic rules

Typowy pipeline (przekładalny na Twoją „Knowledge team”):

1. **Zbieranie episodic memory**
   - logi agentów (plany, akcje, odpowiedzi, token logs),[^1_30][^1_1]
   - wyniki: PR‑y, test results, deployment logs.[^1_40][^1_19]

2. **Retrospektywne przetwarzanie**
   - Retro skills (Retro, Development Retrospective, reviews‑retros‑reflection) wyciągają: „co poszło dobrze, co źle, root cause, akcje”.[^1_28][^1_9][^1_5]
   - Playbook „Lessons Learned” formatuje to w Successes / Problems / Actions / Process Changes / Knowledge transfer.[^1_18]

3. **Konsolidacja do semantic memory**
   - mechanizm „lesson graduation”: ważne lekcje są wynoszone z retro.md do CLAUDE.md lub globalnych reguł (np. `rules/agents.yaml`).[^1_9][^1_18]
   - Mem0‑like pipeline: ekstrakcja insightów z rozmów, klastrowanie, zapis jako facts z priorytetem i typem.[^1_41][^1_32]

4. **Wykorzystanie w planowaniu i wykonaniu**
   - przy każdym planowaniu/epizodzie orchestrator używa RAG na semantic memory, żeby zainjektować aktualne reguły, preferencje i decyzje architektoniczne do promptu.[^1_39][^1_31][^1_32]
   - multi‑agent frameworks oparte o GraphRAG (Narrative Knowledge Weaver, KARMA, GraphAgents, GraphRAG GenAI platform) traktują knowledge graph jako **substrat rozumowania**, po którym chodzą agenci.[^1_42][^1_43][^1_44][^1_45]

### 4.3. Decay i selekcja

Zarówno blogi, jak i papers o continual learning (CER, JitRL) podkreślają, że **brak selekcji w pamięci prowadzi do kosztów i spadku jakości**. Dobre praktyki:[^1_35][^1_36][^1_33]

- inferencja na podstawie **wybranych reprezentatywnych trajektorii** w dynamicznym bufferze doświadczeń,[^1_36][^1_35]
- okresowe summary raw logs → abstrakcyjne lekcje (episodic → semantic),[^1_32]
- mechanizmy zapominania: LRU, score‑based decay, manual pruning w retro („czy ta lekcja nadal obowiązuje?”).[^1_37][^1_33]

### 4.4. Warstwy: personal, project, org

Wzorce z Mem0, Redis, blogów system‑design:

- **Personal/agent‑specific** – preferencje użytkownika/projektu: styl, stack, „don’t do X”.[^1_41][^1_32]
- **Project/team** – CLAUDE.md / AGENTS.md: architektura, konwencje, komponenty, integracje.[^1_7][^1_18]
- **Organization/global** – cross‑project rules, security policies, standard patterns (np. „używaj hierarchical orchestrator w multi‑agent systems”).[^1_46][^1_47][^1_48][^1_33]

Enterprise‑owe systemy typu Gemini Enterprise + GraphRAG platformy integrują to w jeden „mission control”, gdzie multi‑agent system siedzi nad wspólną semantic layer.[^1_49][^1_44][^1_38]

### 4.5. Wnioski dla Octadecimal

Dla MVP:

- **Episodic** – prosty event store (SQLite / Postgres / files + OpenTelemetry): task runs, plany, błędy, PR‑y, metryki.[^1_40][^1_30]
- **Semantic/project** – `CLAUDE.md` / `AGENTS.md` per repo, budowane przez /retro + manualną edycję.[^1_7][^1_5]
- **Semantic/global** – osobne repo z regułami YAML/markdown (bez potrzeby full KG na starcie), ale z myślą, że może ewoluować w knowledge graph.[^1_38][^1_31]
- **Procedural** – definicje skills/agents/flows (OpenHands agent loop, BMAD roles, Retro skills) jako część kodu platformy.[^1_50][^1_30][^1_5]

Scrumowe ceremonie to tylko **triggery pipeline’u pamięciowego**; cała wartość jest w architekturze pamięci i jej konsekwentnym użytku.

---

## 5. Tooling wspierający tę kadencję

### 5.1. Jira/Linear + AI

Rynek już integruje agentów z backlogami:

- AI agenci dla Jira (Aziro, RelevanceAI) robią **predykcyjne planowanie sprintów, detekcję bottlenecków, auto‑triage, velocity reports**.[^1_24][^1_6]
- Atlassian rozwija „agentic AI” w Jira Service Management – agenci wykonują workflowy ITSM na istniejących projektach.[^1_51]
- Scrum.org ostrzega, że Jira historycznie jest bugtrackerem i nie oferuje natively struktur, których potrzebują agenci (pamięć, kontekst, granularne logi), stąd potrzeba dodatkowej warstwy „project knowledge architecture”.[^1_15]

Dla jednoosobowego shopu pełna Jira wygląda na overkill; wystarczy:

- lekki backlog (Linear / GitHub Issues / markdown),
- PR‑y jako outcomes,
- pliki wiedzy w repo (CLAUDE.md, retro.md, rules).

### 5.2. Claude Code skills / retro tools

Ekosystem Claude Code dostarcza klocki bardzo zbliżone do Twojej wizji:

- **„Self‑learning Scrum workflow for Claude Code”** – skillset reklamowany jako „self‑learning scrum workflow” dla zespołów używających Claude Code.[^1_52][^1_25]
- **Retro/lessons skills**:
  - Retro, Development Retrospective, reviews‑retros‑reflection, Sprint Retro Facilitator.[^1_29][^1_27][^1_28][^1_5][^1_9]
  - generują retro.md, lessons.md, mają „lesson graduation” do CLAUDE.md / global rules.[^1_5][^1_9]
- Playbook **„Lessons Learned”** – gotowy schemat dokumentacji lessons learned ze strong naciskiem na action items i process changes.[^1_18]

Sygnał rynkowy: **prawdziwa product‑isation dzieje się wokół retrospektyw i wiedzy, nie wokół standupów.**

### 5.3. Orchestration / observability

- Multi‑agent stacks używają topologii: sequential pipeline, hierarchical decomposition, decentralized consensus; w praktyce **hierarchical orchestrator wygrywa w produkcji** dzięki jasnej odpowiedzialności i łatwemu debugowaniu.[^1_47][^1_48][^1_53][^1_46]
- OpenHands dokumentuje agent loop jako 30‑linijkowy `step()`: drain pending actions, condense, call LLM, classify response, handle tool calls – to jest „mikro‑sprint” z wbudowaną obserwowalnością.[^1_30][^1_40]

Dla Octadecimal:

- orchestrator‑agent (Manager‑of‑Agents) + wyspecjalizowane Code/Test/Docs/Retro agents,[^1_48][^1_46][^1_47]
- event log + traces,
- prosty dashboard epizodów (ile, czas, koszt, interwencje).

### 5.4. Markdown‑first

Pattern promowany m.in. przez AI Engineer Summit i Claude Code:

- specy w markdown (PRD, TASK, ARCHITECTURE), konsumowane przez agentów,[^1_26]
- `.claude/skills`, `CLAUDE.md`, `retro-notes.md`, `session-log*.md` jako knowledge base per repo.[^1_25][^1_7]

To dobrze skaluje się w jednoosobowym shopie – masz Git jako jedyne „źródło prawdy”.

---

## 6. Rekomendowana kadencja Octadecimal MVP

### 6.1. Naturalna długość sprintu

Źródła sugerują:

- w AI‑heavy dev **2–3‑dniowe sprinty** są optymalne – 2 tygodnie to za długo, by utrzymać sensowny feedback i review.[^1_11][^1_10]
- agentic narzędzia typu Devin operują naturalnie na **epizodach „ticket → PR”** z wewnętrzną długą pętlą (plan → execute → debug) – mikro‑sprint per zadanie.[^1_20][^1_19]

Rekomendacja:

- **Sprint = 2–3 dni kalendarzowe**, ale podstawową jednostką jest **epizod (intent → deliverable)**.
- Sprint to „batch epizodów + retro + update wiedzy”.

### 6.2. Founder jako PO + retro uczestnik – skalowalność

Przy jednoosobowym shopie rola Foundera jako **PO + agent manager + architekt** jest nieunikniona i krótkoterminowo skalowalna, jeśli:

- liczba równoległych epizodów jest mała (1–3),
- retro i knowledge propagation są częściowo zautomatyzowane (agent przygotowuje draft, Founder tylko akceptuje).[^1_9][^1_5]

Kadencja stanie się bottleneckiem, jeśli:

- Founder spędza większość czasu na ręcznych ceremoniach zamiast na decyzjach produktowych,
- knowledge pipeline wymaga manualnego przepisywania.

Dlatego już w MVP warto oddać **facylitację retro / lessons / rules update** agentom, a Founder zostaje „approverem”.

### 6.3. Automatyzacja pętli poprawy

Z rynku widać, że **tak, tę pętlę da się częściowo zautomatyzować**:

- Retro / Development Retrospective generują lessons i proponowane zmiany w CLAUDE.md / rules; człowiek tylko je reviewuje.[^1_5][^1_9]
- Continual learning frameworks (CER, JitRL) pokazują, że agent może **sam identyfikować powtarzające się problemy i agregować doświadczenia**, choć w pracach naukowych jest to jeszcze głównie na poziomie benchmarków.[^1_35][^1_36]

Dla Octadecimal:

- RetroAgent:
  - pobiera logi z ostatniego sprintu,
  - generuje retro.md + listę sugestii rules changes (per‑project + global),
  - taguje priorytety,
  - Founder wybiera, co zaakceptować → KnowledgeCurator wprowadza zmiany.

### 6.4. „Velocity” dla agentów

Klasyczne story points + velocity dla botów to prawie na pewno **metrics theatre**. Zamiast tego praktycy proponują:[^1_6][^1_15][^1_1]

- **capacity w tokenach/compute** jako parametryzacja „ile pracy” agent może wykonać w sprincie,[^1_1]
- **throughput epizodów** – `#episodes done / time`, przy ustalonym progu jakości,[^1_24][^1_6]
- **human intervention rate** – ile czasu człowiek spędza na poprawkach / nadzorze per epizod.[^1_47][^1_4]

Dla MVP:

- velocity traktuj wyłącznie jako narzędzie do **skalibrowania planowania**, nie KPI,
- trzy główne liczby per sprint:
  - liczba ukończonych epizodów,
  - minuty interwencji człowieka per epizod,
  - koszt compute (tokens / $$) per epizod.

### 6.5. Proponowana kadencja – tabela

| Element            | Decyzja dla Octadecimal MVP                                       |
|--------------------|-------------------------------------------------------------------|
| Sprint length      | 2–3 dni, batch epizodów                                          |
| Jednostka pracy    | Epizod: intent → PR/testy/docs done                              |
| Planning           | Light sprint planning + strong `/plan` per epizod                |
| Daily              | Brak standupu; daily raport agenta + 5–10 min przegląd Founder   |
| Refinement         | `/groom` / BMAD‑style spec generation (markdown + constraints)   |
| Review             | Episode closure + checklist DoD; często stapiane z retro         |
| Retro              | Co 2–3 dni; RetroAgent + Founder; update retro.md, lessons.md    |
| Knowledge          | Pipeline episodic → retro → CLAUDE.md/rules/global knowledge     |
| Uczestnicy         | Founder + Orchestrator + Code/Test/Docs/Retro/Knowledge agents   |
| Velocity           | #epizodów, interwencje, koszt compute; brak story points         |

---

## 7. Otwarte pytania i czerwone flagi

### 7.1. Otwarte pytania

- **Jak daleko iść w auto‑modyfikację reguł?**
  Papers o continual learning (CER, JitRL) podkreślają, że agresywne modyfikacje bez walidacji mogą psuć zachowanie agenta; potrzebne są guard‑raile (np. tylko lekcje z wysokim zaufaniem, manualne approve).[^1_36][^1_35]
- **Kiedy realnie przechodzić z single‑agent na multi‑agent?**
  Stevo po 19 sprintach sugeruje: multi‑agent dopiero przy dużych repo/flow; inaczej to koordynacyjny dług.[^1_12]
- **Czy budować knowledge graph już teraz, czy później?**
  Blogi o semantic memory i knowledge graphs mówią, że w produkcji KG daje przewagę, ale większość systemów startuje od vector DB + metadata i dopiero potem przechodzi do KG/GraphRAG.[^1_44][^1_31][^1_38]
- **Jak utrzymać spójność reguł przy wielu klientach/projektach?**
  GraphRAG i multi‑agent + KG frameworki sugerują, że w pewnym momencie globalne zasady lepiej trzymać w KG niż w płaskim markdownie.[^1_45][^1_42][^1_44]

### 7.2. Red flags / consensus‑bullshit

- **„Agent Scrum” jako zespół botów odgrywających wszystkie ceremonie jak ludzie** – brak dowodów, że to działa; praktycy raczej ostrzegają przed nadmiarem rytuałów i skupiają się na logach, pipeline’ach i pamięci.[^1_14][^1_12][^1_1]
- **Story points / velocity jako KPI dla agentów** – consensus: vanity metrics; realne są throughput, koszt, poziom interwencji człowieka.[^1_15][^1_6][^1_1]
- **„Więcej agentów = lepiej”** – dane z 19 sprintów mówią odwrotnie; multi‑agent ma sens dopiero przy realnie niezależnych streamach.[^1_12]
- **Kadencja bez architektury pamięci** – bez świadomej semantic/episodic/procedural warstwy lądujesz z toną logów i powtarzającymi się błędami.[^1_33][^1_31][^1_32]

### 7.3. Czy to w ogóle warto robić?

Z jednej strony: BMAD, Claude Code workflows, enterprise agent stacks pokazują, że **lekki, agent‑świadomy Scrum (krótkie sprinty, mocna retro, dobry refinement, pipeline wiedzy) zwiększa przewidywalność, jakość i „documentation by default”.**[^1_16][^1_17][^1_7][^1_5]

Z drugiej: **pełne kopiowanie Scrum dla ludzkich zespołów na agentów jest w dużej mierze teatr.** Kadencja ma sens tylko tam, gdzie pomaga szybciej się uczyć i stabilizować system agentów; wszędzie tam, gdzie służy tylko odgrywaniu ról, będzie przeszkodą.[^1_13][^1_3][^1_1]

---

Jeśli chcesz, kolejnym krokiem może być konkretny szkic repo dla Octadecimal (foldery `.octa/agents`, `CLAUDE.md`, `retro.md`, `rules/` + przykładowe prompty i flows) pod tę kadencję.
<span style="display:none">[^1_100][^1_101][^1_102][^1_103][^1_54][^1_55][^1_56][^1_57][^1_58][^1_59][^1_60][^1_61][^1_62][^1_63][^1_64][^1_65][^1_66][^1_67][^1_68][^1_69][^1_70][^1_71][^1_72][^1_73][^1_74][^1_75][^1_76][^1_77][^1_78][^1_79][^1_80][^1_81][^1_82][^1_83][^1_84][^1_85][^1_86][^1_87][^1_88][^1_89][^1_90][^1_91][^1_92][^1_93][^1_94][^1_95][^1_96][^1_97][^1_98][^1_99]</span>

<div align="center">⁂</div>

[^1_1]: https://briefhq.ai/blog/managing-ai-agents-broken-chain/
[^1_2]: https://www.linkedin.com/pulse/scrum-non-human-teams-managing-ai-agents-s7umf
[^1_3]: https://agileleadershipdayindia.org/blogs/ai-augmented-scrum-framework/ai-augmented-scrum-framework.html
[^1_4]: https://www.elixirclaw.ai/blog/autonomous-agents-project-reporting
[^1_5]: https://mcpmarket.com/tools/skills/session-retrospective-retro
[^1_6]: https://www.aziro.com/blog/boosting-sprint-velocity-with-agentic-ai-and-jira-integration
[^1_7]: https://www.reddit.com/r/ClaudeAI/comments/1sn27yu/claude_code_workflow_tips_after_6_months_of_daily/
[^1_8]: https://www.reddit.com/r/ClaudeAI/comments/1sn33ow/selflearning_loop_for_claude_code_based_on_scrum/
[^1_9]: https://mcpmarket.com/tools/skills/development-retrospective
[^1_10]: https://co-r-e.com/method/ai-sprint-review
[^1_11]: https://www.linkedin.com/posts/kevintholland_dataproducts-productmanagement-agile-activity-7357040042608848897-rJW9
[^1_12]: https://smledbetter.com/what-i-learned-running-19-sprints-with-ai-agents/
[^1_13]: https://scrumexpansion.org/ai-and-scrum/
[^1_14]: https://www.reddit.com/r/ClaudeAI/comments/1sxvotu/3_antipatterns_and_5_patterns_from_building_a/
[^1_15]: https://www.scrum.org/resources/blog/jira-ai-agents-project-management-tool-project-knowledge-architecture
[^1_16]: https://swansoftwaresolutions.com/taming-the-ai-chaos-why-im-all-in-on-the-bmad-method/
[^1_17]: https://bennycheung.github.io/bmad-reclaiming-control-in-ai-dev
[^1_18]: https://www.claudecodehq.com/playbooks/recipe-lessons-learned
[^1_19]: https://cognition.ai/blog/introducing-devin
[^1_20]: https://www.zenml.io/llmops-database/building-an-autonomous-ai-software-engineer-with-advanced-codebase-understanding-and-specialized-model-training-6bnir
[^1_21]: https://docs.sweep.dev/agent
[^1_22]: https://aiagentslist.com/agents/aider
[^1_23]: https://monday.com/blog/rnd/the-different-types-of-scrum-meetings-for-beginners/
[^1_24]: https://marketplace.relevanceai.com/integrations/jira
[^1_25]: https://valuealignmentconsulting.com/skills-observatory.html
[^1_26]: https://jedi.be/blog/2025/talk-2025-the-4-patterns-of-ai-native-development-ai-engineer-summit-edition/
[^1_27]: https://www.azilen.com/learning/semantic-memory/
[^1_28]: https://aipractitioner.substack.com/p/long-term-memory-unlocking-smarter-38d
[^1_29]: https://redis.io/blog/long-term-memory-architectures-ai-agents/
[^1_30]: https://www.emergentmind.com/papers/2305.16291
[^1_31]: https://openreview.net/pdf?id=RXvFK5dnpz
[^1_32]: https://arxiv.org/html/2601.18510v1
[^1_33]: https://kenaz.ai/case-studies/memory-nexus
[^1_34]: https://tianpan.co/blog/long-term-memory-types-ai-agents
[^1_35]: https://dev.to/sreeni5018/the-5-types-of-ai-agent-memory-every-developer-needs-to-know-part-1-52fn
[^1_36]: https://docs.openhands.dev/sdk/arch/agent
[^1_37]: https://dev.to/truongpx396/openhands-deep-dive-build-your-own-guide-1al0
[^1_38]: https://www.aimcp.info/zh/skills/45fbea21-c438-4c4a-a6bd-b847c9f67b6e
[^1_39]: https://www.reddit.com/r/AI_Agents/comments/1r0q4qf/ai_agents_need_better_memory_systems_not_just/
[^1_40]: https://openreview.net/forum?id=P7KtWPDhRz
[^1_41]: https://neurips.cc/virtual/2025/poster/116417
[^1_42]: https://www.nature.com/articles/s41598-026-47145-x
[^1_43]: https://arxiv.org/html/2602.07491v1
[^1_44]: https://www.hcltech.com/blogs/gemini-enterprise-ai-operating-system
[^1_45]: https://github.com/bmad-code-org/BMAD-METHOD
[^1_46]: https://www.atlassian.com/blog/announcements/jira-service-management-agentic-ai
[^1_47]: https://x.com/profemkpop
[^1_48]: https://www.mysecond.ai/skills/sprint-retro-facilitator
[^1_49]: https://playbooks.com/skills/eddiebe147/claude-settings/retrospective-facilitator
[^1_50]: https://aetherlink.ai/en/blog/agentic-ai-development-2026-rag-mcp-multi-agent-orchestration-in-production-helsinki
[^1_51]: https://www.channel.tel/blog/multi-agent-orchestration-patterns-production-2026
[^1_52]: https://www.augmentcode.com/tools/multi-agent-orchestration-platforms-build-vs-buy
[^1_53]: https://redwerk.com/blog/best-multi-agent-ai-frameworks/
[^1_54]: https://www.linkedin.com/pulse/327-growth-multi-agent-workflows-pilot-phase-officially-kanis-patel-kwmic
[^1_55]: https://www.linkedin.com/posts/darren-coxon_ai-agile-bmad-activity-7364663441640308736-XJz7
[^1_56]: https://www.reddit.com/r/softwaredevelopment/comments/1mvvqr6/are_traditional_sdlc_workflows_dead/
[^1_57]: https://www.youtube.com/watch?v=YLGrENURe98
[^1_58]: https://www.linkedin.com/pulse/december-3-2025-daily-scrum-meeting-di-tomas-herda-ceng--nwe4e
[^1_59]: https://www.reddit.com/r/EntrepreneurRideAlong/comments/1r4egun/founders_or_cxos_who_have_scaled_past_20_people/
[^1_60]: https://www.reddit.com/r/cscareerquestions/comments/1j7bcwq/anyone_noticed_that_the_more_pro_ai_someone_is/
[^1_61]: https://news.ycombinator.com/item?id=44026516
[^1_62]: https://stepmark.ai/2025/01/08/company-spotlight-cognition-ai-devin-your-autonomous-software-engineer/
[^1_63]: https://dev.to/linou518/running-10-ai-agents-to-automate-my-life-a-practical-guide-with-openclaw-ki7
[^1_64]: https://fritz.ai/cognition-ai-review/
[^1_65]: https://www.linkedin.com/pulse/deep-dive-cognitions-devin-ai-how-differs-from-microsoft-daley-5ciqf
[^1_66]: https://www.reddit.com/r/ClaudeCode/comments/1py6n4q/weekly_sprint_report_for_team_of_my_agents/
[^1_67]: https://www.youtube.com/watch?v=-0bBQ4BXZ14
[^1_68]: https://www.reddit.com/r/nocode/comments/1sf1ygt/i_built_7_open_source_projects_without_writing_a/
[^1_69]: https://www.reddit.com/r/scrum/comments/1sl5jfs/how_are_you_adjusting_sprint_planning_with_ai_in/
[^1_70]: https://www.reddit.com/r/agile/comments/1std7rh/if_a_retrospective_does_not_change_the_next/
[^1_71]: https://www.linkedin.com/posts/snehamehrin_retro-with-claude-code-activity-7427698032520962048-EeO-
[^1_72]: https://www.reddit.com/user/Irreverant-SaaS/comments/
[^1_73]: https://www.reddit.com/user/GreenArkleseizure/comments/
[^1_74]: https://www.aimcp.info/de/skills/45fbea21-c438-4c4a-a6bd-b847c9f67b6e
[^1_75]: https://lobehub.com/skills/lyndonkl-claude-reviews-retros-reflection
[^1_76]: https://www.facebook.com/groups/DeepNetGroup/posts/1977584239301115/
[^1_77]: https://www.linkedin.com/posts/jasonmlemkin_one-of-our-20-ai-agents-is-momentum-which-activity-7452364832063848448-13PY
[^1_78]: https://www.linkedin.com/posts/mathursrus_aimanager-agenticai-productleadership-activity-7369482637050064896-u-3f
[^1_79]: https://www.unryo.com/manager-of-managers
[^1_80]: https://01.me/en/2025/10/agent-continual-learning/
[^1_81]: https://github.com/zzz47zzz/awesome-lifelong-learning-methods-for-llm
[^1_82]: https://www.semanticscholar.org/paper/Continual-Learning,-Not-Training:-Online-Adaptation-Jaglan-Barnes/4c536542b3931339b30f72b91fce39cc05ff4cd2
[^1_83]: https://www.linkedin.com/posts/rakeshgohel01_building-ai-agents-with-knowledge-graphs-activity-7411391640772206592-12gS
[^1_84]: https://dl.acm.org/doi/10.1007/978-3-032-07638-0_11
[^1_85]: https://aiagentstore.ai/ai-agent/mentat
[^1_86]: https://bestaiagents.ai/agent/aider
[^1_87]: https://github.com/All-Hands-AI/OpenHands/issues/20
[^1_88]: https://directory.composio.dev/listings/sweep/
[^1_89]: https://github.com/AbanteAI
[^1_90]: https://www.youtube.com/playlist?list=PLcfpQ4tk2k0VetQVGT1EqTbcr-qcgbfFs
[^1_91]: https://aipatternbook.com/sweep
[^1_92]: https://leadai.dev/code/mentat
[^1_93]: https://aider.chat
[^1_94]: https://www.latent.space/p/2025-summit
[^1_95]: https://jvsmanagement.com/blog/
[^1_96]: https://www.trentgillespie.live/post/ai-sprint-the-lobster-that-proved-multi-agent-systems-are-here
[^1_97]: https://www.instagram.com/p/DW9JZG0AXyo/
[^1_98]: https://www.linkedin.com/pulse/ai-multi-agent-engineering-teams-reimagining-sprint-zero-amit-pandey-amk8c
[^1_99]: https://www.linkedin.com/posts/saasjet_jira-atlassian-nocode-activity-7439611772912689152-0e_f
[^1_100]: https://www.mean2epsilon.blog/ais-impact-traditional-agile-models
[^1_101]: https://www.reddit.com/r/AI_Agents/comments/1tcj8wo/most_multiagent_setups_have_one_agent_do/
[^1_102]: https://www.linkedin.com/posts/scrum-org_agile-ai-scrum-activity-7330420803152265216-7qZY
[^1_103]: https://lablab.ai/ai-hackathons/deriv-ai-talent-sprint/blinks-labs/ai-powered-multi-agent-enterprise-platform```

