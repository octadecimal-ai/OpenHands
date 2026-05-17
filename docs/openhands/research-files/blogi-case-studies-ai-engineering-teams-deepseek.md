## 1. Executive summary

Inżynieria oprogramowania w 2025–2026 przeszła fundamentalną zmianę: zespoły nie tyle „piszą kod z pomocą AI”, ile **orchestrują zespoły agentów**, które piszą kod za nich. Liderzy techniczni powinni wynieść z tej analizy pięć kluczowych wniosków:

1. **Agent to nie narzędzie, lecz członek zespołu.** Najbardziej dojrzałe organizacje (Rakuten, OpenAI, Brex, Goldman Sachs) traktują agentów jak równoprawnych uczestników procesu deweloperskiego — z przypisanymi rolami, uprawnieniami i odpowiedzialnością. Inżynierowie przesuwają się z roli „kierowcy” do roli „recenzenta i architekta”, a ich kluczową kompetencją staje się definiowanie intencji i nadzór, nie implementacja.

2. **Agent Control Plane to warunek sine qua non skali.** Żaden z analizowanych wdrożeń produkcyjnych nie działa bez warstwy kontrolnej, która zarządza dostępami, politykami, audytem i kosztami. GitHub, OpenHands, Coder i MuleSoft dostarczają (lub rozwijają) rozwiązania w tym obszarze. Bez tego agentów nie da się bezpiecznie wdrożyć na większą skalę.

3. **Metryki throughputu są mylące — liczy się jakość współpracy.** Thoughtworks ostrzega przed „pułapką szybkości” — linie kodu i liczba PR-ów nie przekładają się na realną produktywność. Kluczowe stają się wskaźniki takie jak *first-pass acceptance rate* (udział zmian, które przeszły bez poprawek), *iteration cycles per task* i *review burden*, mierzone na poziomie zespołu, a nie jednostki.

4. **AI wzmacnia, nie naprawia.** DORA AI Capabilities Model pokazuje, że AI działa jak amplifikator: w zespołach o wysokiej dojrzałości przyspiesza dostawy, w słabych pogłębia dysfunkcje (np. zalew słabej jakości kodu, który przeciąża recenzentów). Organizacje, które nie mają uporządkowanych procesów CI/CD, bezpieczeństwa i code review, nie powinny skakać do agentów.

5. **Nadzór człowieka jest warstwowy, nie binarny.** Rzeczywiste systemy produkcyjne stosują 3–4 poziomy kontroli: od agentów-walidatorów, przez agentów strażników („AI guardians”), po meta-agentów koordynujących i eskalacje do człowieka. „Człowiek w pętli” to nie przycisk approve, tylko zestaw mechanizmów prewencji, wykrywania i korekty.

---

## 2. Case studies

| Organizacja / Projekt | Problem | Rozwiązanie | Narzędzia | Governance | Mierniki sukcesu | Link(i) |
|---|---|---|---|---|---|---|
| **Rakuten** (70+ biznesów, e‑commerce/fintech) | Skalowanie AI przy tysiącach deweloperów bez utraty jakości i bezpieczeństwa | Redesign workflow wokół automation assistant, parallelizacja zadań (5 równoległych zadań agenta) | automation assistant | Nie opisane wprost, ale działanie w skali enterprise | 79% redukcji time‑to‑market (24 dni → 5 dni), 7 godzin autonomous coding, 99.9% accuracy |  |
| **OpenAI (Frontier Product Exploration)** | Zbudowanie systemu >1M linii kodu bez żadnej ręcznie pisanej linii i bez ręcznego code review | Harness engineering — agent‑first design: cały kod pisany przez OpenHands, żadnej ręcznej interwencji | OpenHands, Symphony („ghost library”) | Agent działa w pętli zamkniętej; awarie diagnozowane przez brakujące capabilities, nie przez „lepszy prompt” | Zero human‑written code, zero human code review, system w pełni produkcyjny |  |
| **Goldman Sachs** (12 tys. inżynierów) | Automatyzacja rutynowych zadań (migracje legacy code, refaktoring, debugging) w bezpieczny sposób | Hybrydowy model workforce: setki instancji Devina pracujących pod stałym nadzorem człowieka | Devin (Cognition) | Ciągły nadzór człowieka; inżynier przekształca problem w prompt i weryfikuje output; DevOps w pętli | 3–4x poprawa vs poprzednie AI tools; 13.9% GitHub issues rozwiązywanych autonomicznie (powyżej średniej) |  |
| **Brex** | Włączenie nietechnicznych członków zespołu (content designer) do procesu deweloperskiego i demokratyzacja dostępu do danych | Code review as primary mode: inżynierowie nie piszą, tylko recenzują zmiany wprowadzone przez automation assistant | automation assistant, MCP servers, Brex Explorer (text‑to‑SQL) | Architektura i kierunek definiowane przez człowieka; implementacja przez agenta | 3–4x poprawa w konkretnych zadaniach; content designer zrealizował projekt z backlogu (tygodnie/miesiące → kilka dni) |  |
| **Zapier** | Rozproszone eksperymenty agentowe bez kontroli i standardów | Wdrożenie 800+ agentów wewnętrznych z 89% adopcją AI w całej organizacji | Własna platforma agentowa | Centralne zarządzanie agentami na poziomie całej firmy | 89% adopcji, 800+ agentów, zintegrowani z codziennym workflow |  |
| **TELUS** | Przyspieszenie developmentu bez wzrostu headcountu | 13 tys. customowych rozwiązań AI, integracja agentów z istniejącym workflow | LLM (custom solutions) | — | 30% szybszy development, 500k+ godzin zaoszczędzonych |  |
| **Asana (AI Teammates)** | Fragmentacja agentów i brak kontroli nad ich działaniem | Specjalistyczni agenci wbudowani w workflow (Campaign Brief Writer, Compliance Specialist, itd.) + context engineering jako podstawa | Asana AI Studio | Agenci działają w ramach istniejących kontroli Asany; dostęp do danych organizacji ograniczony politykami | Redukcja czasu planowania → delivery; pełna przejrzystość działań agentów |  |

---

## 3. Human oversight — jak zespoły kontrolują agentów

### Warstwowy model kontroli

Analiza wdrożeń produkcyjnych pokazuje, że skuteczny nadzór nad agentami nie jest binarny („człowiek vs. autonomia”), lecz warstwowy. Praktycy wykształcili trzy główne poziomy:

**Poziom 1: Agent‑as‑guardian (walidacja automatyczna).** Zamiast człowieka sprawdzającego każdy output, deployuje się agentów specjalizujących się w walidacji — sprawdzających bezpieczeństwo, jakość, zgodność ze standardami. „AI guardians” działają jako pierwsza linia obrony, zanim jakikolwiek kod trafi do człowieka.

**Poziom 2: Progressive oversight (nadzór dostosowany do ryzyka).** Zup (w artykule z kwietnia 2026) wdrożył warstwowe zabezpieczenia bezpieczeństwa, które okazały się skuteczniejsze niż samo prompt engineering, wraz z progresywnymi trybami nadzoru, które napędzały organiczną adopcję bez wymuszania zaufania. W praktyce: dla zadań niskiego ryzyka agent działa autonomicznie; dla średniego ryzyka wymaga korekty przed kontynuacją; dla wysokiego ryzyka angażuje człowieka.

**Poziom 3: Agent‑initiated stops (agent sam prosi o pomoc).** LLM provider udokumentowało, że w najbardziej złożonych zadaniach automation assistant *sam* zatrzymuje się, aby zapytać o wyjaśnienia, ponad dwa razy częściej niż człowiek go przerywa. To nie jest oznaka słabości — to zaprojektowana cecha systemu, która zapobiega kosztownym błędom.

### Mechanizmy operacyjne nadzoru

- **Outcomes / grading.** LLM Managed Agents wprowadza oddzielnego „gradera”, który w osobnym kontekście ocenia każdy output względem zdefiniowanego rubryki i odsyła agenta do poprawki, dopóki nie spełni standardu. W benchmarkach LLM provider podniosło to skuteczność tasków nawet o 10 punktów procentowych na najtrudniejszych problemach.

- **Meta‑agents orchestrujący.** GitLab opisuje warstwę „meta‑agentów”, którzy koordynują pracę, eskalują problemy i komunikują się z ludźmi przez istniejące kanały (e‑mail/Slack/tickets), utrzymując człowieka w pętli dla zatwierdzeń i odpowiedzialności.

- **Cross‑agent memory.** GitHub Copilot wprowadził pamięć między agentami, która pozwala agentom uczyć się na doświadczeniach bez polegania na bezpośrednich instrukcjach użytkownika. Agent korekcyjny może wykorzystać wiedzę zgromadzoną przez agenta kodującego.

- **Granice agentów (Agent Boundaries / Agent Firewall).** Coder wprowadza polityki wykonawcze, które ograniczają, do czego agent może mieć dostęp — działa to jak „dedykowana zapora dla agenta”. Jeśli agent nie może uzyskać dostępu do określonego źródła, ryzyko znacząco spada.

### Kluczowa lekcja dla Octadecimal

**Nie projektuj nadzoru jako jednego „przycisku zatwierdzenia”.** Zaprojektuj warstwę agentów‑walidatorów, którzy *sprawdzają* pracę innych agentów (agents auditing agents), zanim zostanie ona pokazana człowiekowi. To zmniejsza obciążenie człowieka i pozwala mu skupić się na decyzjach architektonicznych i strategicznych, nie na drobiazgach.

> *„Effective oversight of agents requires more than putting a human in the approval chain.”* — LLM provider

---

## 4. Operating model — jak wygląda dzień pracy, backlog, review, retry, escalation

### Struktura zespołu agentowego

Najbardziej dojrzałe organizacje przechodzą od „jednego agenta na jednego dewelopera” do *specjalistycznych zespołów agentów*, wzorowanych na zespołach ludzkich. Octoco.ai opisuje ewolucję w trzech generacjach: (1) accelerated autocomplete (2021–2023), (2) synchronous agents (2023–2025), (3) autonomous agent teams (2025–2026).

W praktyce oznacza to architekturę, w której:

- **Lead agent / orchestrator** otrzymuje zadanie od człowieka, rozkłada je na podzadania i deleguje.
- **Specialist sub‑agents** (frontend, backend, database, reviewer, DevOps) pracują równolegle na współdzielonym filesystemie, każdy z własnym modelem, promptem i narzędziami.
- **Reviewer agent** sprawdza output przed pokazaniem człowiekowi.
- **Grader agent** ocenia jakość względem zdefiniowanych rubryk i wymusza poprawki (pętla retry).

### Typowy dzień pracy inżyniera w modelu agentowym

Rakuten i Brex dostarczają najbardziej konkretnych obrazów:

1. **Planowanie i specyfikacja (30% czasu).** Inżynier nie pisze kodu, tylko definiuje intencję, architekturę i kryteria akceptacji. W Brex: „I refine the problem itself much more. You can try three approaches for the same problem during the same amount of time”.

2. **Delegacja i równoległa praca agentów (agent pracuje w tle).** Rakuten: „You can have five tasks running in parallel by delegating four to automation assistant while focusing on the remaining one”. OpenAI: wewnętrzna pętla (inner loop) ma górny limit jednej minuty — jeśli agent nie osiągnie postępu w tym czasie, coś jest nie tak z taskiem lub kontekstem.

3. **Review i korekta (40% czasu).** Inżynier przegląda zmodyfikowany kod — w trybie przeglądu, nie tworzenia. Jeśli zmiana nie przechodzi, agent dostaje feedback i poprawia.

4. **Eskalacja i troubleshooting (20% czasu).** Gdy agent ugrzęźnie, inżynier diagnozuje: czy brakuje capability, contextu, czy struktury — nie tylko „popraw prompt”. Agent‑initiated stops są tu kluczowe.

### Backlog i planowanie

- **Zadania agentowe** są oznaczane w backlogu i mogą być przypisywane agentom (GitHub pozwala przypisać issue do @llm lub @openhands, a agent otwiera draft PR).
- **Workflows definiowane raz, uruchamiane wielokrotnie.** OpenHands Automations pozwala zdefiniować workflow (np. „vulnerability remediation”) i uruchamiać go na schedule lub trigger z systemów.
- **Agent wykonuje w trybie asynchronicznym** — inżynier nie czeka, tylko wraca do wyników, gdy webhook powiadomi o zakończeniu.

### Retry i pętle korekcyjne

- **Outcomes framework** (LLM Managed Agents): agent może przejść wiele iteracji, zanim output spełni rubric. Na wewnętrznych benchmarkach LLM provider lift skuteczności o 10 punktów na najtrudniejszych taskach.
- **First‑pass acceptance rate** jako kluczowy wskaźnik: im wyższy, tym mniej iteracji. Thoughtworks zaleca mierzenie tego na poziomie zespołu i łączenie z DORA.
- **Failures diagnozowane przez brakujące capability**, nie przez „lenistwo agenta”. OpenAI: gdy agent zawodzi, team pyta: „Jakiej zdolności, kontekstu lub struktury brakuje?”.

### Escalacja

- **Agent‑initiated stop** → agent prosi o wyjaśnienie (automation assistant robi to 2x częściej, niż człowiek go przerywa).
- **Human‑initiated stop** → inżynier przerywa agenta przy widocznych błędach.
- **Meta‑agent escalation** → agent nadrzędny wykrywa konflikt między agentami i przekazuje go człowiekowi przez Slack/ticket.
- **Ręczny override** → dla zadań wysokiego ryzyka (produkcja, bezpieczeństwo) wymagany jest zatwierdzenie przez człowieka przed merge.

---

## 5. Metrics — jakie metryki są sensowne, a jakie są teatrem

### Teatr (metrics that lie)

| Metryka | Dlaczego to teatr |
|---|---|
| **Lines of code generated** | „A flood of poorly aligned code that slows reviews, harms delivery throughput and introduces security risks” |
| **Time to first output** | Mierzy szybkość rozpoczęcia, nie szybkość ukończenia wartościowej zmiany |
| **Number of PRs** | Nie oddaje jakości ani złożoności; może prowadzić do inflacji małych, słabych PR-ów |
| **Agent sessions / day** | Mierzy aktywność, nie efekt — można mieć wiele sesji bez produktywności |
| **Adoption % w oderwaniu od głębokości** | 85% adopcji nie znaczy nic, jeśli acceptance rate wynosi 5% |

Faros AI udokumentowało, że w 2025 roku volume PR-ów wzrósł o 98% na dewelopera, **bez wymiernej poprawy w DORA metrics**. W 2026 roku trend się utrzymał, z poszerzającą się luką jakościową.

### Metryki sensowne (co naprawdę warto mierzyć)

**Warstwa współpracy (Collaboration Quality) — zalecane przez Thoughtworks:**

| Metryka | Definicja | Dlaczego wartościowa |
|---|---|---|
| **First‑pass acceptance rate** | % zmian agenta przyjętych bez (lub z minimalnymi) poprawkami | Ujawnia ukryty wysiłek; poprawa przez lepsze prompty i specyfikacje |
| **Iteration cycles per task** | Liczba rund agent ↔ korekta | Niższa = lepsza specyfikacja i kontekst |
| **Review burden** | Czas spędzony przez człowieka na przeglądzie kodu agenta | Rosnący burden = agent generuje zbyt dużo słabej jakości kodu |
| **Post‑merge rework** | % zmian wymagających poprawek po merge | Wczesny wskaźnik narastającego długu technicznego |
| **Failed builds (AI‑touched)** | % nieudanych buildów z kodem od agenta vs. human baseline | Oddziela jakość agenta od ogólnej stabilności |

**Warstwa dostawy (DORA + rozszerzenia):**

| Metryka | Benchmark / Uwagi |
|---|---|
| **Deployment Frequency** | Lift 18–45% przy wysokiej adopcji AI |
| **Lead Time for Changes** | Redukcja 20–45%; median PR cycle time spadł o 24% |
| **Change Failure Rate** | Kluczowa — Thoughtworks: niższy acceptance rate → wyższy CFR |
| **Time to Restore Service (MTTR)** | Bez zmian lub poprawa; AI może pomóc w diagnostyce incydentów |
| **Rework rate** | DORA dodała to jako piątą metrykę w 2025 |

**Warstwa adopcji i głębokości (6‑layer framework od Exceeds AI):**

| Warstwa | Metryka | Benchmark (2026) |
|---|---|---|
| 1: Adopcja | DAU/WAU % | Mature: 60%, Emerging: 30% |
| 1: Adopcja | Tool Diversity Index | 2–3 tools per engineer |
| 2: Głębokość | Acceptance rate | 25–30% |
| 2: Głębokość | AI Lines/Commit % | 41% global average |
| 3: Produktywność | AI PR Cycle Time | -20% to -45% |
| 4: Quality/Risk | Rework rate | Monitor vs. human baseline |
| 4: Quality/Risk | 30‑day incidents (AI‑touched code) | <5% |
| 5: Business Impact | Cost savings / engineer / week | 3.6 hours average |
| 6: Scaling | Trust score | >85% for autonomous workflows |

### Kluczowa lekcja dla Octadecimal

**Nie mierz throughputu — mierz jakość współpracy.** Połącz DORA (lead time, change failure rate) z first‑pass acceptance rate i review burden. Mierz na poziomie *zespołu*, nie jednostki. Wprowadź cotygodniowy przegląd tych metryk na retrospektywie, aby iteracyjnie poprawiać prompty, dokumenty primingowe i design conversations.

> *„Most evaluation metrics still focus too heavily on coding throughput… Measuring collaboration quality helps teams avoid falling into the speed trap.”* — Thoughtworks

---

## 6. Implications for Octadecimal — co warto zastosować w pierwszym dokumencie projektowym

Na podstawie analizy wdrożeń z 2025–2026, oto konkretne rekomendacje dla pierwszego dokumentu projektowego agentowego zespołu w Octadecimal:

### 6.1 Architektura: Agent Control Plane jako fundament

Nie projektuj agentów jako odizolowanych narzędzi. Od pierwszego dnia załóż **warstwę kontrolną**, która zapewnia:

- **Centralne zarządzanie dostępami i politykami** (co agent może robić, do jakich repozytoriów, jakie narzędzia).
- **Audyt i śledzenie kosztów** — każda akcja agenta logowana, każde wywołanie modelu rozliczane.
- **Sandboxed execution** — każdy agent działa w izolowanym środowisku (OpenHands: „sandboxed runtime”).
- **Model‑agnostic flexibility** — nie wiąż się z jednym dostawcą; Coder pokazuje, że oddzielenie *how agents run* od *which models they use* jest kluczowe dla długoterminowej elastyczności.

### 6.2 Struktura zespołu agentowego: specjalizacja i orchestracja

Zaprojektuj zespół agentów jako **hierarchię ról**, nie zbiór identycznych instancji:

- **Orchestrator (lead agent)** — otrzymuje zadanie od człowieka, rozkłada na podzadania, deleguje do subagentów, zbiera wyniki. LLM Managed Agents dostarcza reference implementation.
- **Specialist sub‑agents** — każdy z własnym promptem, modelem i zestawem narzędzi: frontend, backend, database, reviewer, DevOps, test writer, documentation.
- **Reviewer / grader agent** — działa w oddzielnym kontekście, ocenia output względem rubryki, wymusza poprawki. Outcomes framework LLM provider to gotowy wzorzec.
- **Guardian agents** — specjalizują się w walidacji bezpieczeństwa, compliance, jakości, zanim kod trafi do człowieka.

### 6.3 Nadzór: trzy poziomy, nie jeden przełącznik

Zaprojektuj **warstwowy model oversight**, nie binarny:

1. **Auto‑validation** — guardian agents sprawdzają każdy output zanim zostanie pokazany człowiekowi.
2. **Progressive oversight** — dla niskiego ryzyka agent działa autonomicznie; dla wysokiego ryzyka wymaga zatwierdzenia.
3. **Agent‑initiated stops** — agent ma pełne prawo i obowiązek zatrzymać się i zapytać, gdy czegoś nie rozumie (automation assistant: 2x częściej niż człowiek przerywa).

### 6.4 Workflow i integracja z istniejącymi systemami

- **Integracja z istniejącym backlogiem** — zadania dla agentów oznaczone w Jira/Linear/GitHub Issues, możliwość przypisania agenta.
- **Draft PR jako domyślny output** — agent otwiera draft PR, człowiek recenzuje, zatwierdza lub odsyła do poprawki (wzorzec z GitHub).
- **Asynchroniczność i webhooki** — agent pracuje w tle, webhook powiadamia o zakończeniu.
- **Workflows definiowane raz, uruchamiane wielokrotnie** — nie „ręcznie triggerowany agent”, tylko automatyzacje na schedule lub trigger (OpenHands Automations).

### 6.5 Metryki sukcesu dla pierwszych 90 dni

| Obszar | Metryka | Target (pierwsze 90 dni) |
|---|---|---|
| Adopcja | DAU (członkowie zespołu używający agentów dziennie) | >60% |
| Głębokość | Acceptance rate (first‑pass) | >25% |
| Jakość | Change failure rate (zmiany od agentów) | nie wyższy niż baseline ludzki |
| Efektywność | Lead time for changes (zmiany agentowe vs. ludzkie) | -20% |
| Koszt | $/task | ustal baseline i monitoruj |

### 6.6 Czego unikać (anty‑wzorce z rynku)

1. **Nie zaczynaj od „naprawiania starej infrastruktury”** — OpenAI, Rakuten i Brex projektowali workflow *od nowa* wokół agentów, nie adaptowali starych procesów.
2. **Nie mierz LoC ani liczby PR-ów** — to prowadzi do inflacji słabej jakości kodu i przeciążenia recenzentów.
3. **Nie zakładaj, że agent zastąpi inżyniera** — badania LLM provider pokazują, że inżynierowie mogą w pełni delegować tylko 0–20% zadań; reszta wymaga nadzoru i walidacji.
4. **Nie uruchamiaj agentów na laptopach** — Coder: „Agents根本无法在笔记本电脑上并发运行” (agenci po prostu nie mogą działać równolegle na laptopach). Potrzebujesz scentralizowanej, skalowalnej infrastruktury.

### 6.7 Inspiracje do dalszej lektury (do załącznika w dokumencie)

- **OpenHands Enterprise** — referencyjna implementacja agent control plane z sandboxingiem i automations
- **LLM Managed Agents (Outcomes, Multiagent orchestration)** — gotowe wzorce do zaadaptowania
- **DORA AI Capabilities Model** — 7 capabilities do diagnozy gotowości organizacji
- **Thoughtworks: Measuring collaboration quality with coding agents** — framework metryk
- **Coder AI Governance Add‑On (AI Gateway + Agent Firewall)** — wzór dla bezpiecznego wdrożenia w regulowanym środowisku

---

*Podsumowując: kluczowym przejściem nie jest „kupno lepszego narzędzia”, lecz przeprojektowanie modelu operacyjnego zespołu. Octadecimal ma szansę zbudować agent‑native engineering team od zera, bez balastu legacy. Źródła z 2025–2026 wskazują, że warunkiem sukcesu jest: Agent Control Plane + warstwowy nadzór + metryki jakości współpracy (nie throughputu) + specjalistyczna struktura zespołu agentów.*