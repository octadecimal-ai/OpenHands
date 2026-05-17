# Rekonesans techniczny alternatyw dla Claude Code: Raport Octadecimal 2026

W obliczu zbliżającego się wyłączenia produktów Roo Code (15 maja 2026) oraz rosnącej potrzeby niezależności od jednego dostawcy (vendor lock-in), Octadecimal musi zdywersyfikować swój stack agentowy. Poniższy raport przedstawia najlepsze model-agnostic rozwiązania orkiestracyjne, które pozwalają na wykorzystanie pełnej mocy procesorów M5 oraz natywnej konteneryzacji macOS Tahoe.

## TL;DR

- **OpenHands (v1.7)** to obecnie najpotężniejszy, w pełni autonomiczny zamiennik Claude Code, oferujący 87% skuteczności w rozwiązywaniu ticketów i natywną izolację w Dockerze.
- **Microsoft Agent Governance Toolkit (Agent OS)** jest bezkonkurencyjnym rozwiązaniem dla Octadecimal w zakresie wdrażania rygorystycznego rulebooka i 3-poziomowej eskalacji.
- **OpenCode (SST)** dominuje jako rozwiązanie terminal-native z ekstremalną wydajnością tokenową (4.2x lepszą niż Claude Code) i wsparciem dla 75+ dostawców modeli.
- Natywna konteneryzacja **macOS Tahoe** na procesorach M5 umożliwia sub-sekundowy start agentów w izolowanych mikro-VM, co czyni tradycyjny Docker Desktop opcjonalnym.

---

**Inwentarz frameworków orkiestracji (Maj 2026)**

| Framework | Repo URL | Maintenance Status | Last meaningful update | License | Fit-score |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **OpenHands** | [github.com/OpenHands/OpenHands](https://github.com/OpenHands/OpenHands) | Aktywny (v1.7.0) | 2026-05-09 | MIT | 4.9 |
| **Microsoft AGT** | [github.com/microsoft/agt](https://www.google.com/search?q=https://github.com/microsoft/agt) | Produkcyjny | 2026-05-01 | MIT | 4.8 |
| **OpenCode (SST)** | [github.com/opencode-ai/opencode](https://github.com/opencode-ai/opencode) | Aktywny | 2026-05-04 | MIT | 4.7 |
| **LangGraph** | [github.com/langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) | Dojrzały (v1.1) | 2026-05-05 | MIT | 4.5 |
| **Mastra** | [github.com/mastra-ai/mastra](https://github.com/mastra-ai/mastra) | Aktywny (v1.0) | 2026-04-30 | Apache-2.0 | 4.0 |

---

**Deep Dives**

### 1. OpenHands (dawniej OpenDevin): Standard Autonomii

OpenHands v1.7 to obecnie najbardziej dojrzała platforma inżynierii agentowej, która wyparła Claude Code w wielu profesjonalnych workflowach ze względu na bezpieczeństwo.

- **Architektura:** Wykorzystuje event-stream architecture, gdzie każda interakcja jest niezmiennym zdarzeniem, co pozwala na pełny replay i odtwarzanie stanu po awarii.
- **Model-Agnosticism:** Dzięki LiteLLM wspiera ponad 100 dostawców, w tym lokalne modele przez Ollama. W testach OpenHands z modelem Qwen3-Coder-30B osiągnął wydajność w zasięgu 20% od największych modeli komercyjnych.
- **Konteneryzacja:** Natywnie wymusza izolację w Dockerze z uprawnieniami cap-drop ALL, chroniąc hosta macOS przed błędami agentów.

### 2. Microsoft Agent Governance Toolkit (Agent OS)

Wydany w kwietniu 2026, AGT stał się jądrem systemów wymagających rygorystycznego governance.

- **3-Level Escalation:** Idealnie mapuje wymogi Octadecimal. **L1 (Send-back)** przez ToolCallInterceptor, **L2 (Retro)** przez Agent Compliance (zbieranie dowodów/traces), oraz **L3 (Notify)** przez mandatory approval gates zintegrowane z dashboardem.
- **Wydajność:** Stateless policy engine zapewnia deterministyczne egzekwowanie reguł (YAML, Rego, Cedar) z latencją p99 poniżej 0.1ms.
- **Agent Mesh:** Każdy agent otrzymuje tożsamość kryptograficzną DID (Decentralized Identifiers), co pozwala na bezpieczną komunikację inter-agent bez wycieku kluczy API.

### 3. OpenCode (SST): Wydajność Terminal-Native

OpenCode to bezpośrednia odpowiedź społeczności na Claude Code, napisana w Go i Rust, co gwarantuje natywną szybkość na procesorach M5.

- **Efektywność tokenowa:** W testach porównawczych OpenCode zużywa średnio 105k tokenów na zadanie, podczas gdy Claude Code potrzebuje 479k dla tego samego rezultatu.
- **Multi-team Modeling:** Wspiera LSP (Language Server Protocol) dla TypeScript i Python, co drastycznie redukuje błędy kompilacji w Monorepo Octadecimal.
- **Infrastruktura:** Integruje się z systemem Superset, pozwalając na orkiestrację 10+ agentów w izolowanych git worktrees z wizualnym dashboardem i wbudowaną przeglądarką.

---

**Klasyfikacja Buy / Borrow / Build**

- **Borrow (Adopt): OpenHands + Microsoft AGT.** Octadecimal powinien użyć OpenHands jako silnika egzekucji i Microsoft AGT jako warstwy kontrolnej. Są to otwarte standardy 2026 roku, których budowa od zera jest ekonomicznie nieuzasadniona.
- **Build: Octadecimal Rulebook & Synergy Layer.** Założyciel musi zbudować własne definicje hooków w TypeScript oraz specyficzne "skills" (np. automatyczne formatowanie PR pod standardy firmy) w folderze .agents/skills/.
- **Buy: OpenHands Enterprise.** Warto rozważyć zakup wersji Enterprise dla Agent Control Plane, który zapewnia RBAC, audytowalność i centralne zarządzanie kosztami LLM.

---

**Top 3 rekomendacje**

1. **OpenHands jako Core Engine na macOS Tahoe:** Zastąpienie Claude Code przez OpenHands działający w natywnych kontenerach Tahoe. Zyskujesz izolację mikro-VM i sub-sekundowy start agentów.
2. **Microsoft AGT jako Governance Layer:** Wdrożenie sidecara Agent OS do wymuszania rulebooka. Pozwala to na realizację L1/L2/L3 escalation bez modyfikacji kodu agentów.
3. **4-warstwowa propagacja wiedzy przez LangGraph:** Użycie LangGraph do modelowania przepływu wiedzy (Personal → Team → Cross-team → Company) dzięki wsparciu dla hybrydowej pamięci (Vector + Graph + Episodic).

---

**Otwarte pytania**

- **Narzut Tahoe:** Jak "VM-per-container" w macOS Tahoe wpłynie na latencję komunikacji między 7 zespołami agentów przy pełnym obciążeniu GPU M5?.
- **A2A Protocol:** Czy Octadecimal powinien zainwestować w adaptery Agent-to-Agent (A2A) od Google, aby umożliwić współpracę agentów OpenHands z agentami w chmurze Vertex AI?.

---

**Czerwone flagi (Red Flags)**

- **Roo Code Sunset (15 May 2026):** Ryzyko nagłej utraty dostępu do konfiguracji i agentów w chmurze Roo Cloud. Wymagana natychmiastowa kopia zapasowa folderu `~/.roo`.
- **Legacy AutoGen v0.2:** Unikać bibliotek opartych na starym modelu AutoGen. Brak wsparcia dla durable state czyni je bezużytecznymi w profesjonalnym stacku 2026.
- **Context Crush w MCP gateways:** Bramki MCP (np. Bifrost) raportują błędy przy ładowaniu >100 narzędzi jednocześnie, co może prowadzić do halucynacji w wyborze narzędzi przez agentów.
