# **Strategie i Architektury Autonomicznych Zespołów Agentów AI w Inżynierii Oprogramowania: Raport Badawczy 2025-2026**

## **TL;DR**

Transformacja inżynierii oprogramowania w latach 2025–2026 oznacza przejście od prostych asystentów uzupełniających kod do w pełni autonomicznych, wieloagentowych zespołów (Multi-Agent Teams), zdolnych do samodzielnego planowania i egzekucji złożonych zadań.1 Dominującym wzorcem architektonicznym stał się model hierarchiczny Coordinator-Subagent, w którym nadrzędny "Architekt" zarządza wyspecjalizowanymi rolami, takimi jak Planner, Coder, Tester i Reviewer.3 Kluczowym elementem infrastruktury jest Model Context Protocol (MCP), który standaryzuje komunikację między agentami a zewnętrznymi narzędziami i bazami wiedzy.1 Nowoczesne systemy, takie jak OpenHands i Coder Agents, kładą nacisk na izolację wykonawczą w kontenerach Docker/OCI oraz rygorystyczną kontrolę kosztów poprzez budżetowanie tokenów i wielopoziomowe bramki zatwierdzeń (Human Approval Gates).6 Powstanie standardu AGENTS.md oraz metodyki Spec-Driven Development (SDD) pozwala na zredukowanie długu technicznego generowanego przez AI i przywrócenie specyfikacji jako "jedynego źródła prawdy".9

## **Top repositories**

Poniższa tabela przedstawia najbardziej wpływowe projekty i repozytoria open source z lat 2025-2026, stanowiące wzorce dla budowy zaawansowanych systemów agentowych.

| Nazwa Projektu | URL / Lokalizacja | Stars/Aktywność (2026) | Stack Techniczny | Model Pracy / Architektura | Co warto skopiować? | Czerwone flagi / Ograniczenia |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **OpenHands** | [github.com/OpenHands/OpenHands](https://github.com/OpenHands/OpenHands) | Najwyższa (standard branżowy) 12 | Python, React, Docker, Kubernetes | **CodeAct 1.0**: Zintegrowana pętla rozumowania i akcji w sandboksie.6 | Izolacja Daytona, obsługa długich zadań (30h+), integracja z CI/CD.6 | Wysokie koszty inferencji przy braku lokalnych modeli.6 |
| **Spec Kit** | [github.com/github/spec-kit](https://github.com/github/spec-kit) | 96k+ stars 9 | Python (CLI), Markdown (Templates) | **Spec-Driven Development (SDD)**: Spec → Plan → Tasks → Implement.13 | "Konstytucja" projektu, wymuszone bramki walidacyjne, niezależność od modelu.14 | Ryzyko nadmiernej sztywności procesu (Waterfall AI).14 |
| **Coder Agents** | [coder.com/blog/introducing-coder-agents](https://coder.com/blog/introducing-coder-agents) | Dynamiczna (Enterprise focus) 16 | Go, TypeScript, OCI Containers | **Self-hosted Control Plane**: Centralne zarządzanie promptami i modelami.7 | Całkowita izolacja sieciowa, provisionowanie workspace per zadanie.16 | Zamknięta część enterprise; wymaga infrastruktury Coder.16 |
| **Metaswarm** | [github.com/dsifry/metaswarm](https://github.com/dsifry/metaswarm) | Aktywny wzorzec multi-agent 17 | Python, Playwright, SQLite | **Hierarchical Swarm**: Orchestrator sterujący rolami PM, Architect, Security.17 | Adversarial review, PR Shepherd, wizualna inspekcja przez Playwright.17 | Złożoność komunikacji przy dużej liczbie agentów.17 |
| **Mercury Agent** | [github.com/cosmicstack-labs/mercury-agent](https://github.com/cosmicstack-labs/mercury-agent) | 2.2k stars (Stable v1.1.6) 8 | TypeScript, Node.js, SQLite | **Persistence-First**: System "Second Brain" i budżetowanie tokenów.8 | Rygorystyczny Token FinOps, mechanizm "Ask Me" przed akcją powłoki.8 | Interfejs TUI może być ograniczający dla dużych projektów.8 |
| **Everything Copilot CLI** | [github.com/drvoss/everything-copilot-cli](https://github.com/drvoss/everything-copilot-cli) | Community-driven (2025/2026) 18 | Shell, Markdown, MCP Servers | **Multi-AI Orchestration**: Copilot CLI jako hub dla Claude/OpenHands/Gemini.18 | 11 wzorców orkiestracji (Fan-Out, Agent Council), baza SQL sesji.18 | Wysoka zależność od specyficznych wersji protokołu MCP.18 |
| **POG Task** | [enjtorian.github.io/pog-task/](https://enjtorian.github.io/pog-task/) | Nowatorski standard (2026) 19 | YAML, Markdown, Git | **Governance-First**: Strukturalny zapis rozumowania w record.md.19 | Deterministyczny format zadań, audytowalny ślad decyzji (Reasoning Trace).19 | Wymaga dużej dyscypliny w definiowaniu "Intent".19 |

## **Ewolucja Architektoniczna: Od Jednoagentowych Asystentów do Autonomicznych Zespołów**

W latach 2025–2026 inżynieria oprogramowania przeszła fundamentalną zmianę paradygmatu, porzucając model prostej predykcji kodu na rzecz autonomicznej orkiestracji zadań.20 O ile tradycyjne narzędzia typu "Copilot" działały w pętli reaktywnej (propozycja następnej linii kodu), o tyle nowoczesne systemy agentowe operują w trybie zadaniowym, obejmującym pełny cykl od analizy zgłoszenia (Issue) do otwarcia Pull Requestu.1

### **Paradygmat Hierarchiczny: Coordinator-Subagent**

Najskuteczniejszym wzorcem architektonicznym dla złożonych przepływów pracy stał się model hierarchiczny, imitujący strukturę profesjonalnego zespołu programistycznego.3 W centrum tego układu znajduje się agent koordynujący (często definiowany w pliku architect.agent.md lub coordinator.agent.md), który pełni rolę "dyrygenta" systemu.3 Jego zadaniem nie jest bezpośrednie pisanie kodu, lecz dekompozycja celu nadrzędnego na atomowe jednostki pracy i delegowanie ich do wyspecjalizowanych sub-agentów.3  
Model ten rozwiązuje krytyczny problem "szumu kontekstowego". Zamiast zmuszać pojedynczy model do przetwarzania całej wiedzy o projekcie, każda jednostka otrzymuje jedynie wycinek kontekstu niezbędny do wykonania swojej roli.4 Przykładowo, sub-agent typu Researcher analizuje dokumentację i API, Coder implementuje logikę, a Tester weryfikuje ją w izolowanym środowisku.3 Nowoczesne środowiska IDE, takie jak Visual Studio Code (wersja 1.110+), wspierają natywną równoległość w tym modelu, co pozwala na jednoczesną pracę nad logiką i testami jednostkowymi, znacząco zwiększając przepustowość zespołu.4

### **Spec-Driven Development (SDD): Przywrócenie Rygoru**

W odpowiedzi na zjawisko "vibe coding" (kodowania opartego na intuicji modelu, a nie precyzyjnych wymaganiach), w 2026 roku standardem stała się metodyka Spec-Driven Development (SDD).9 Projekt Spec Kit, zainicjowany przez inżynierów GitHub, promuje podejście, w którym specyfikacja jest centralnym "źródłem prawdy", a kod jest jedynie jej pochodną.9  
Proces SDD w systemach agentowych dzieli się na cztery główne fazy, z których każda produkuje trwały artefakt Markdown służący jako kontekst dla kolejnego kroku 9:

1. **Specify**: Definiowanie "co" i "dlaczego" bez wchodzenia w szczegóły techniczne.  
2. **Plan**: Wybór architektury, stosu technologicznego i kontraktów API.  
3. **Tasks**: Generowanie listy zadań z uwzględnieniem zależności i markerów równoległości.  
4. **Implement**: Autonomiczna egzekucja zadań przez agenta kodującego.13

Fundamentem tego podejścia jest "konstytucja" projektu (constitution.md), która zawiera nienegocjowalne zasady jakości, bezpieczeństwa i konwencji, do których każdy agent musi się odwołać przed podjęciem jakiejkolwiek akcji.14 Dzięki temu unika się sytuacji, w której AI wprowadza zmiany sprzeczne z długofalową architekturą systemu.14

## **Szczegółowa Analiza Ról w Zespołach Agentowych**

Budowa skutecznego zespołu agentów wymaga precyzyjnego zdefiniowania person, które posiadają unikalne zestawy narzędzi (skills) i ograniczenia systemowe.3

### **Planner i Architekt**

Rola Plannera ewoluowała z prostego generatora list "to-do" w zaawansowany system przewidywania ryzyka i zależności.17 Architekt agentowy operuje w trybie "Plan Mode" (np. Ctrl+P w Mercury Agent), tworząc strukturę modyfikacji plików przed dotknięciem kodu.8 Kluczową funkcją Plannera w 2026 roku jest "Cross-artifact consistency check" – mechanizm sprawdzający, czy plan techniczny nie narusza wymagań zawartych w specyfikacji.25

### **Implementer i Coder**

Agenci typu Implementer (np. coder.agent.md) są optymalizowani pod kątem "instrumentalnego" rozumowania – szybkiej egzekucji zmian przy użyciu narzędzi edycji plików i wywołań powłoki.4 W nowoczesnych architekturach Implementer nie pracuje bezpośrednio na głównej gałęzi kodu, lecz w odizolowanych "worktrees", co pozwala na bezpieczne testowanie wielu wariantów rozwiązania jednocześnie.10

### **Tester i Reviewer**

Współczesne systemy (np. Metaswarm) wprowadzają rolę "Adversarial Reviewer".17 W przeciwieństwie do standardowego recenzenta, jego zadaniem jest aktywna próba "zepsucia" propozycji kodu poprzez generowanie brzegowych przypadków testowych i sprawdzanie odporności na ataki typu prompt injection w wygenerowanym kodzie.17 Z kolei rola "Testera" jest ściśle powiązana z pętlą "self-healing test loop", gdzie agent autonomicznie naprawia błędy wykryte przez lintery i testy jednostkowe przed zgłoszeniem PR.6

### **Security Reviewer i Governance**

W związku z incydentami takimi jak "Replit DROP DATABASE" (lipiec 2025), rola Security Reviewera stała się krytyczna.31 Agenci ci działają w trybie "deny-first", analizując każdą komendę powłoki pod kątem ryzykownych operacji (np. rm \-rf, chmod, modyfikacje .env).8 Modele governance, takie jak Decision Evidence Maturity Model (DEMM), wymagają od agentów dostarczania "dowodów decyzji" – zapisu rozumowania wyjaśniającego, dlaczego dana akcja została podjęta i pod jaką polityką została autoryzowana.31

### **Knowledge Curator (Kustosz Wiedzy)**

Zupełnie nową rolą, która zyskała na znaczeniu w 2026 roku, jest Knowledge Curator.17 Wykorzystuje on metodologię "ARCHETYPAL\_WEAVE" do systematycznego odkrywania i analizowania wiedzy w rozproszonych repozytoriach.33 Jego głównym zadaniem jest ekstrakcja nauczek z zamkniętych PR-ów i aktualizacja "pamięci projektowej" (MEMORY.md lub .ai/state.json), co zapobiega re-wyjaśnianiu tych samych koncepcji nowym sesjom agentowym.3

## **Mechanizmy Operacyjne i Infrastruktura**

Sukces wdrożenia agentów w organizacji zależy od solidności warstwy operacyjnej, która zarządza cyklem życia zadań, bezpieczeństwem i kosztami.27

### **Izolacja Środowiska i Git Worktrees**

Bezpieczeństwo egzekucji kodu przez agentów jest realizowane poprzez wielowarstwową izolację 6:

* **Sandboxing kontenerowy**: Każdy agent uruchamia swoje procesy w efemerycznym kontenerze Docker lub Kubernetes. Integracja z platformą Daytona pozwala na pełną kontrolę terminala i przechwytywanie telemetrii.6  
* **Git Worktrees**: Agenci tworzą dedykowane drzewa robocze dla każdego zadania, co pozwala na izolację zmian w systemie plików i równoległą pracę wielu agentów bez konfliktów w lokalnym repozytorium.10  
* **Network Isolation**: W systemach takich jak Coder Agents, pętla agenta działa w "Control Plane", a workspace nie posiada bezpośredniego dostępu do internetu, co uniemożliwia exfiltrację kodu do zewnętrznych modeli bez nadzoru.16

### **Orkiestracja przez Git Issues i Pull Requests**

W roku 2026 GitHub przekształcił się w "system operacyjny" dla agentów.18 Orkiestracja zadań odbywa się natywnie przez mechanizmy platformy:

* **Issue-to-PR Flow**: Przypisanie Issue do agenta (np. Copilot Coding Agent) inicjuje autonomiczny proces analizy repozytorium, pisania testów i generowania poprawki.1  
* **Agent HQ**: Scentralizowany panel zarządzania flotą agentów różnych dostawców (Anthropic, OpenAI, Google), pozwalający na definiowanie polityk dostępu na poziomie organizacji.1  
* **PR Shepherd**: Specjalistyczny agent monitorujący status CI, naprawiający błędy lintowania w locie i odpowiadający na komentarze recenzentów w sposób uporządkowany.17

### **Kontrola Kosztów i Token FinOps**

Eskalacja kosztów inferencji w długotrwałych sesjach agentowych (często trwających ponad 30 godzin) wymusiła powstanie praktyk Token FinOps.6

* **Daily Token Budgets**: Mercury Agent wprowadza rygorystyczne limity dziennego zużycia tokenów, z automatycznym przejściem w tryb "auto-concise" (streszczanie kontekstu) po przekroczeniu 70% limitu.8  
* **Multi-Model Routing**: Systemy takie jak everything-copilot-cli stosują routing modeli oparty na trudności zadania. Przykładowo, Claude 4.5 jest używany do planowania architektury, podczas gdy tańsze modele typu "flash" obsługują triaż zgłoszeń i generowanie powtarzalnego boilerplate'u.18  
* **Context Compaction**: Claude Code implementuje pięciowarstwową rurę zagęszczania, która zastępuje historyczne wiadomości ich streszczeniami, aby utrzymać wydajność rozumowania w granicach okna kontekstowego.32

### **Human Approval Gates**

Mimo rosnącej autonomii, systemy klasy produkcyjnej wprowadzają krytyczne punkty kontrolne 32:

* **Permission Modes**: Mercury Agent oferuje tryby "Ask Me" (potwierdzenie każdej akcji) i "Allow All" (pełna autonomia w sesji).8  
* **Approval Checkpoints**: Narzędzia typu LangGraph wspierają natywne przerwania (interrupts), wymagające zgody człowieka przed wykonaniem operacji o wysokim ryzyku, takich jak migracje baz danych czy wdrożenia na produkcję.38  
* **Dual Review Areas**: W obszarach wrażliwych (płatności, tożsamość) wymuszane jest zatwierdzenie kodu przez co najmniej dwóch różnych agentów recenzujących oraz jednego człowieka.30

## **Analiza Najważniejszych Projektów i Standardów**

### **Claude Code: Architektura Pętli Agentowej**

Claude Code, wydany przez Anthropic, jest obecnie punktem odniesienia dla efektywnego "agentic loop".29 Jego architektura opiera się na funkcji queryLoop(), która realizuje wzorzec ReAct (Reasoning and Acting) w cyklu "while-true".32 Co istotne, tylko 1,6% bazy kodu Claude Code odpowiada za samą logikę rozumowania – pozostałe 98,4% to infrastruktura operacyjna zarządzająca bezpieczeństwem, uprawnieniami, persystencją sesji i zarządzaniem kontekstem.36  
System ten wprowadza mechanizm "continue sites" – siedem punktów w pętli, w których stan jest zapisywany w całości jako niemutowalny obiekt, co pozwala na bezpieczne wznawianie pracy agenta po błędach lub przerwach w komunikacji.32

### **OpenHands: CodeAct i Control Plane**

OpenHands (wcześniej OpenDevin) wyróżnia się architekturą CodeAct 1.0, która integruje rozumowanie LLM bezpośrednio z płaszczyzną sterowania kodem.6 Zamiast polegać na zewnętrznych narzędziach, agent OpenHands operuje bezpośrednio na sesjach powłoki wewnątrz kontenera, co pozwala mu na "samoleczenie" (self-healing) środowiska programistycznego – np. samodzielną instalację brakujących zależności systemowych wykrytych podczas kompilacji.6  
Platforma ta oferuje "Agent Control Plane" dla przedsiębiorstw, umożliwiający audytowanie każdej akcji agenta w czasie rzeczywistym oraz centralne zarządzanie uprawnieniami do repozytoriów.12

### **Coder Agents: Izolacja Sieciowa i Bezpieczeństwo**

Projekt Coder Agents adresuje potrzeby sektorów o najwyższych wymaganiach bezpieczeństwa (finanse, rząd).7 Jego unikalność polega na całkowitym oddzieleniu warstwy orkiestracji od egzekucji 7:

* **Control Plane**: Działa w infrastrukturze klienta, przechowuje klucze API modeli i zarządza promptami.  
* **Isolated Workspaces**: Workspace'y agentów są dynamicznie tworzone na żądanie i mogą być całkowicie odcięte od internetu (Air-gapped).16  
* **Network Policies**: Platforma wymusza polityki egress, ograniczając dostęp agenta wyłącznie do lokalnego serwera Git i specyficznych endpointów MCP.16

### **Spec Kit: Powrót do Rygoru Specyfikacji**

Spec Kit jest "antidotum na vibe coding".24 Jego siła tkwi w prostocie i technologicznym agnosticyzmie – wspiera ponad 30 różnych agentów (Claude Code, Copilot, Gemini CLI) poprzez standaryzowane komendy typu /speckit.plan czy /speckit.implement.9 Narzędzie to promuje tworzenie "żywych dokumentów", które ewoluują wraz z kodem, zapewniając, że każda zmiana jest śledzona od poziomu wymagania biznesowego do konkretnej linii kodu.14

## **Standardy Konfiguracyjne: AGENTS.md i MCP**

W 2026 roku kluczowe dla interoperacyjności stały się dwa standardy:

1. **AGENTS.md**: Pełni rolę "README dla agentów".10 Jest to plik Markdown w korzeniu repozytorium, który zawiera instrukcje nieoczywiste dla modelu (np. specyficzne komendy builda, konwencje nazewnictwa, których nie da się wywnioskować z kodu).11 Standard ten został donacjonowany do Agentic AI Foundation (AAIF) i jest respektowany przez większość nowoczesnych agentów.10  
2. **Model Context Protocol (MCP)**: To otwarty protokół pozwalający agentom na bezpieczny dostęp do zewnętrznych danych i narzędzi (Slack, Jira, bazy SQL, Notion) bez konieczności pisania dedykowanych integracji dla każdego modelu.1 Każdy serwer MCP publikuje "Capability Manifest" (capabilities.json), który opisuje dostępne funkcje, co pozwala koordynatorowi na dynamiczne budowanie logiki routingu zadań.5

## **Antywzorce w Inżynierii Agentowej**

Na podstawie doświadczeń z lat 2025-2026 zidentyfikowano szereg praktyk, których należy unikać:

* **Piecemeal Vibe Coding**: Przeskakiwanie bezpośrednio do implementacji bez fazy planowania i specyfikacji, co prowadzi do narastania długu technicznego, którego żaden agent nie jest w stanie później zrefaktoryzować.14  
* **Type Casting Shortcuts**: Pozwalanie agentom na uciszanie linterów poprzez rzutowanie typów (as any) zamiast naprawy definicji, co skutkuje niestabilnością runtime'u.41  
* **Unreviewed Agent Spam**: Wysyłanie przez deweloperów Pull Requestów wygenerowanych przez AI bez ich wcześniejszego przeczytania i przetestowania, co jest uznawane za nieprofesjonalne i obniża zaufanie w zespole.42  
* **Token Over-consumption**: Brak warstwy zarządzania kontekstem, co prowadzi do wysyłania zbędnych danych (np. całych binariów czy plików logów) do modelu, generując ogromne koszty przy marginalnym zysku jakościowym.34  
* **Over-privileged Agents**: Przyznawanie agentom bezpośredniego dostępu do sekretów produkcyjnych lub gałęzi main bez bramek zatwierdzeń, co stwarza ryzyko katastrofalnych awarii (np. usunięcia bazy danych).30

## **Rekomendacje dla Octadecimal**

Wdrażając własny ekosystem agentowy, Octadecimal powinien rozważyć następujące kroki:

1. **Adopcja Spec-Driven Development**: Wprowadzenie Spec Kit jako obowiązkowego elementu workflow, aby wymusić rygorystyczne definiowanie zadań przed ich egzekucją.9  
2. **Budowa Hierarchicznego Zespołu**: Zdefiniowanie co najmniej trzech ról: Architekta (koordynacja), Codera (implementacja) i Adversarial Reviewera (weryfikacja bezpieczeństwa i jakości).4  
3. **Inwestycja w Infrastrukturę Izolacji**: Wykorzystanie OpenHands lub Coder Agents do zapewnienia bezpiecznego, kontenerowego środowiska pracy agentów z pełnym audytem logów.6  
4. **Wdrożenie Persystencji Długoterminowej**: Zastosowanie wzorca MEMORY.md oraz agentmemory (MCP) w celu zachowania wiedzy architektonicznej między sesjami.4  
5. **Rygorystyczny Token FinOps**: Implementacja limitów kosztowych na poziomie zadania i stosowanie routingu modeli w celu optymalizacji wydatków na inferencję.8

## **Pytania Decyzyjne**

Po lekturze raportu, Octadecimal musi rozstrzygnąć następujące kwestie strategiczne:

* **Autonomia vs Kontrola**: Czy decydujemy się na pełną autonomię agentów (Full-autonomy agent z trybem "Allow All"), czy wdrażamy wymuszone bramki zatwierdzeń (Human-in-the-loop) dla każdej zmiany w systemie plików?.6  
* **Suwerenność Danych**: Czy dopuszczamy orkiestrację w chmurze dostawcy (np. GitHub Agent HQ), czy budujemy w pełni self-hosted control plane (np. Coder Agents) dla ochrony własności intelektualnej?.7  
* **Unifikacja Modelu**: Czy optymalizujemy system pod konkretną rodzinę modeli (np. Claude ze względu na przewagę w tool-calling), czy budujemy architekturę całkowicie agnostic przy użyciu protokołu MCP?.18  
* **Standardy Dokumentacji**: Czy przyjmujemy standard AGENTS.md jako jedyny format instrukcji projektowych, czy rozszerzamy go o własne, strukturalne formaty typu capabilities.json?.5  
* **Mierniki Sukcesu**: Jakie KPI będą kluczowe dla oceny efektywności agentów: liczba zamkniętych Issues, czas od zgłoszenia do PR, czy może containment rate (procent zadań rozwiązanych bez interwencji człowieka)?.27

#### **Cytowane prace**

1. Agentic AI, MCP, and spec-driven development: Top blog posts of 2025 \- The GitHub Blog, otwierano: maja 14, 2026, [https://github.blog/developer-skills/agentic-ai-mcp-and-spec-driven-development-top-blog-posts-of-2025/](https://github.blog/developer-skills/agentic-ai-mcp-and-spec-driven-development-top-blog-posts-of-2025/)  
2. The AI Revolution in 2026: Top Trends Every Developer Should Know \- DEV Community, otwierano: maja 14, 2026, [https://dev.to/jpeggdev/the-ai-revolution-in-2026-top-trends-every-developer-should-know-18eb](https://dev.to/jpeggdev/the-ai-revolution-in-2026-top-trends-every-developer-should-know-18eb)  
3. Best practices for orchestrating multiple agents/skills in Copilot Chat (VS Code) · community · Discussion \#192232 \- GitHub, otwierano: maja 14, 2026, [https://github.com/orgs/community/discussions/192232](https://github.com/orgs/community/discussions/192232)  
4. Orchestrating AI Agents: Elevate Your Dev Workflow with GitHub Copilot Chat \- devActivity, otwierano: maja 14, 2026, [https://devactivity.com/posts/development-integrations/orchestrating-ai-agents-elevate-your-dev-workflow-with-github-copilot-chat/](https://devactivity.com/posts/development-integrations/orchestrating-ai-agents-elevate-your-dev-workflow-with-github-copilot-chat/)  
5. Orchestrating AI Agents: Elevate Your Dev Workflow with GitHub Copilot Chat, otwierano: maja 14, 2026, [https://dev.to/devactivity/orchestrating-ai-agents-elevate-your-dev-workflow-with-github-copilot-chat-8ga](https://dev.to/devactivity/orchestrating-ai-agents-elevate-your-dev-workflow-with-github-copilot-chat-8ga)  
6. OpenHands: Advanced Autonomous Engineering \- How to create an AI agent, otwierano: maja 14, 2026, [https://createaiagent.net/tools/openhands/](https://createaiagent.net/tools/openhands/)  
7. Coder Sets a New Standard for AI Coding with Self-Hosted, AI Model Agnostic Coder Agents, otwierano: maja 14, 2026, [https://coder.com/blog/self-hosted-ai-model-agnostic-coder-agents](https://coder.com/blog/self-hosted-ai-model-agnostic-coder-agents)  
8. GitHub \- cosmicstack-labs/mercury-agent: Soul-driven AI agent with permission-hardened tools, token budgets, and multi-channel access. Runs 24/7 from CLI or Telegram., otwierano: maja 14, 2026, [https://github.com/cosmicstack-labs/mercury-agent](https://github.com/cosmicstack-labs/mercury-agent)  
9. Spec Kit Documentation \- GitHub Pages, otwierano: maja 14, 2026, [https://github.github.com/spec-kit/](https://github.github.com/spec-kit/)  
10. How to Build Your AGENTS.md (2026): The Context File That Makes AI Coding Agents Actually Work, otwierano: maja 14, 2026, [https://www.augmentcode.com/guides/how-to-build-agents-md](https://www.augmentcode.com/guides/how-to-build-agents-md)  
11. AGENTS.md, otwierano: maja 14, 2026, [https://agents.md/](https://agents.md/)  
12. Introducing the OpenHands Index | Jan 28, 2026, otwierano: maja 14, 2026, [https://openhands.dev/blog/openhands-index](https://openhands.dev/blog/openhands-index)  
13. GitHub \- github/spec-kit: Toolkit to help you get started with Spec-Driven Development, otwierano: maja 14, 2026, [https://github.com/github/spec-kit](https://github.com/github/spec-kit)  
14. GitHub's Spec Kit Puts the Spec Back in Software Development \- DevOps.com, otwierano: maja 14, 2026, [https://devops.com/githubs-spec-kit-puts-the-spec-back-in-software-development/](https://devops.com/githubs-spec-kit-puts-the-spec-back-in-software-development/)  
15. Diving Into Spec-Driven Development With GitHub Spec Kit \- Microsoft for Developers, otwierano: maja 14, 2026, [https://developer.microsoft.com/blog/spec-driven-development-spec-kit](https://developer.microsoft.com/blog/spec-driven-development-spec-kit)  
16. Introducing Coder Agents \- Blog \- Coder, otwierano: maja 14, 2026, [https://coder.com/blog/introducing-coder-agents](https://coder.com/blog/introducing-coder-agents)  
17. metaswarm/USAGE.md at main · dsifry/metaswarm · GitHub, otwierano: maja 14, 2026, [https://github.com/dsifry/metaswarm/blob/main/USAGE.md](https://github.com/dsifry/metaswarm/blob/main/USAGE.md)  
18. drvoss/everything-copilot-cli: The definitive guide ... \- GitHub, otwierano: maja 14, 2026, [https://github.com/drvoss/everything-copilot-cli](https://github.com/drvoss/everything-copilot-cli)  
19. AI-Native Task Governance Model \- POG Task \- Prompt Orchestration Governance Task, otwierano: maja 14, 2026, [https://enjtorian.github.io/pog-task/](https://enjtorian.github.io/pog-task/)  
20. What is a Coding Agent? Comparing Agents to AI Code Assistants \- OpenHands, otwierano: maja 14, 2026, [https://openhands.dev/blog/agentic-coding-vs-code-completion](https://openhands.dev/blog/agentic-coding-vs-code-completion)  
21. Streamlining AI Agent Orchestration in Copilot Chat: A Software Developer Overview, otwierano: maja 14, 2026, [https://devactivity.com/insights/streamlining-ai-agent-orchestration-in-copilot-chat-a-software-developer-overview/](https://devactivity.com/insights/streamlining-ai-agent-orchestration-in-copilot-chat-a-software-developer-overview/)  
22. 2026 Agentic Coding Trends Report \- Anthropic, otwierano: maja 14, 2026, [https://resources.anthropic.com/hubfs/2026%20Agentic%20Coding%20Trends%20Report.pdf](https://resources.anthropic.com/hubfs/2026%20Agentic%20Coding%20Trends%20Report.pdf)  
23. Did GitHub Agent HQ Quietly Show Up in Microsoft VS Code 1.110? \- Futurum Research, otwierano: maja 14, 2026, [https://futurumgroup.com/insights/did-github-agent-hq-quietly-show-up-in-microsoft-vs-code-1-110/](https://futurumgroup.com/insights/did-github-agent-hq-quietly-show-up-in-microsoft-vs-code-1-110/)  
24. GitHub Spec Kit Takes Off as Antidote to Piecemeal 'Vibe Coding', otwierano: maja 14, 2026, [https://visualstudiomagazine.com/articles/2026/05/12/github-spec-kit-takes-off-as-antidote-to-piecemeal-vibe-coding.aspx](https://visualstudiomagazine.com/articles/2026/05/12/github-spec-kit-takes-off-as-antidote-to-piecemeal-vibe-coding.aspx)  
25. Meet GitHub Spec-Kit: An Open Source Toolkit for Spec-Driven Development with AI Coding Agents : r/AIDeveloperNews \- Reddit, otwierano: maja 14, 2026, [https://www.reddit.com/r/AIDeveloperNews/comments/1t7ua3c/meet\_github\_speckit\_an\_open\_source\_toolkit\_for/](https://www.reddit.com/r/AIDeveloperNews/comments/1t7ua3c/meet_github_speckit_an_open_source_toolkit_for/)  
26. AGENTS.md Specification: A Research-Backed Guide \- ASDLC.io, otwierano: maja 14, 2026, [https://asdlc.io/practices/agents-md-spec/](https://asdlc.io/practices/agents-md-spec/)  
27. GitHub Agent HQ: Multi-Agent Platform Guide 2025 \- Digital Applied, otwierano: maja 14, 2026, [https://www.digitalapplied.com/blog/github-agent-hq-multi-agent-platform](https://www.digitalapplied.com/blog/github-agent-hq-multi-agent-platform)  
28. How LLM Reasoning Powers the Agentic AI Revolution | by Arash Nicoomanesh | Medium, otwierano: maja 14, 2026, [https://medium.com/@anicomanesh/how-llm-reasoning-powers-the-agentic-ai-revolution-cbefd10ebf3f](https://medium.com/@anicomanesh/how-llm-reasoning-powers-the-agentic-ai-revolution-cbefd10ebf3f)  
29. Top 2% Agentic Engineering \- Roadmap for 2026, otwierano: maja 14, 2026, [https://agenticengineer.com/top-2-percent-agentic-engineering](https://agenticengineer.com/top-2-percent-agentic-engineering)  
30. Agentic engineering, a new model for software development in 2026 \- WPPoland, otwierano: maja 14, 2026, [https://wppoland.com/en/agentic-engineering-new-model-software-development-2026/](https://wppoland.com/en/agentic-engineering-new-model-software-development-2026/)  
31. Decision Evidence Maturity Model for Agentic AI: A Property-Level Method Specification \- arXiv, otwierano: maja 14, 2026, [https://arxiv.org/pdf/2605.04093](https://arxiv.org/pdf/2605.04093)  
32. Dive into Claude Code: The Design Space of Today's and Future AI Agent Systems \- arXiv, otwierano: maja 14, 2026, [https://arxiv.org/html/2604.14228v1](https://arxiv.org/html/2604.14228v1)  
33. The ARCHETYPAL\_WEAVE: Multi-Persona AI Knowledge Management Paradigm \- A systematic methodology for AI-assisted knowledge discovery, analysis, and preservation using composite archetypal intelligence \- Github-Gist, otwierano: maja 14, 2026, [https://gist.github.com/SoMaCoSF/c00f7a598a63c225483e11c0ed3c8421](https://gist.github.com/SoMaCoSF/c00f7a598a63c225483e11c0ed3c8421)  
34. GitHub \- rohitg00/agentmemory: \#1 Persistent memory for AI coding agents based on real-world benchmarks, otwierano: maja 14, 2026, [https://github.com/rohitg00/agentmemory](https://github.com/rohitg00/agentmemory)  
35. Coder Agents Enable Running AI Coding Workflows on Self-Hosted Infrastructure \- InfoQ, otwierano: maja 14, 2026, [https://www.infoq.com/news/2026/05/coder-agents-self-hosted-ai/](https://www.infoq.com/news/2026/05/coder-agents-self-hosted-ai/)  
36. Dive into Claude Code: The Design Space of Today's and ... \- arXiv, otwierano: maja 14, 2026, [https://arxiv.org/pdf/2604.14228](https://arxiv.org/pdf/2604.14228)  
37. Three tiers of Agentic AI \- and when to use none of them | Microsoft Community Hub, otwierano: maja 14, 2026, [https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/three-tiers-of-agentic-ai---and-when-to-use-none-of-them/4510377](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/three-tiers-of-agentic-ai---and-when-to-use-none-of-them/4510377)  
38. AI Agent Architecture Patterns: Single & Multi-Agent Systems \- Redis, otwierano: maja 14, 2026, [https://redis.io/blog/ai-agent-architecture-patterns/](https://redis.io/blog/ai-agent-architecture-patterns/)  
39. gh-aw Intelligence Report — 2026-04-16 · zircote github-agentic-workflows · Discussion \#24, otwierano: maja 14, 2026, [https://github.com/zircote/github-agentic-workflows/discussions/24](https://github.com/zircote/github-agentic-workflows/discussions/24)  
40. AGENTS.md, {admiral}, and the AI-Assisted Programmer – pharmaverse blog, otwierano: maja 14, 2026, [https://pharmaverse.github.io/blog/posts/2026-03-31-agents-md-admiral-a/agents-md-admiral-and-the-ai-assisted-programmer.html](https://pharmaverse.github.io/blog/posts/2026-03-31-agents-md-admiral-a/agents-md-admiral-and-the-ai-assisted-programmer.html)  
41. Vibe Destroyer: Agent Anti-Patterns | by Tim Sylvester | Medium, otwierano: maja 14, 2026, [https://medium.com/@TimSylvester/vibe-destroyer-agent-anti-patterns-beb90bafb3de](https://medium.com/@TimSylvester/vibe-destroyer-agent-anti-patterns-beb90bafb3de)  
42. Anti-patterns: things to avoid \- Agentic Engineering Patterns \- Simon Willison's Weblog, otwierano: maja 14, 2026, [https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/)  
43. Beyond Human-Readable: Rethinking Software Engineering Conventions for the Agentic Development Era \- arXiv, otwierano: maja 14, 2026, [https://arxiv.org/html/2604.07502v1](https://arxiv.org/html/2604.07502v1)  
44. No-Code AI Agent Builders: 2026 Comparison Guide \- MindStudio, otwierano: maja 14, 2026, [https://www.mindstudio.ai/blog/no-code-ai-agent-builders](https://www.mindstudio.ai/blog/no-code-ai-agent-builders)  
45. Salesforce Agentforce Implementation: Step-by-Step Guide for Autonomous AI Agents in Business \- Innovadel Technologies, otwierano: maja 14, 2026, [https://www.innovadeltech.com/salesforce-agentforce-implementation-guide/](https://www.innovadeltech.com/salesforce-agentforce-implementation-guide/)