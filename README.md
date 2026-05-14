# System multiagentów Octadecimal

## TL;DR

Obecny stan inżynierii agentowej (maj 2026) charakteryzuje się dominacją podejścia Spec-Driven Development (SDD), gdzie kod jest postrzegany jako pochodna ustrukturyzowanej specyfikacji.8 Framework Ruflo (dawniej LLM-Flow) pozostaje najbardziej zaawansowanym technicznie rozwiązaniem open-source dla użytkowników terminala, oferując oszczędność tokenów rzędu 75-80% dzięki silnikowi napędzanemu przez Rust i WASM.10 Jednocześnie BMAD-METHOD v6 dostarcza najbardziej ustrukturyzowaną metodykę pracy, pozwalając założycielowi Octadecimal na symulację 19 specjalistycznych ról inżynieryjnych.12 Krytycznym sygnałem rynkowym jest wyłączenie produktów Roo Code zaplanowane na 15 maja 2026 r., co wymusza natychmiastową migrację do platformy Cline lub natywnego automation assistant.14 W obszarze governance jedynym rozwiązaniem zapewniającym pełne pokrycie ryzyka OWASP Agentic Top 10 jest Microsoft Agent Governance Toolkit, oferujący deterministyczne egzekwowanie polityk z latencją poniżej 1ms.5

---

## STACK

### OpenHands (dawniej OpenDevin)

OpenHands v1.7 to obecnie najpoważniejszy konkurent automation assistant w kategorii autonomii.78

- **Architektura:** Event-stream architecture, gdzie każda interakcja jest niezmiennym zdarzeniem w logu.80
- **Model-agnostic:** Wspiera ponad 100 dostawców przez LiteLLM, co pozwala Octadecimal na używanie LLM Opus 4.6 do planowania i lokalnej Llamy do pisania testów.80
- **Docker story:** Wymaga demona Docker, uruchamiając agentów w sandboxed containers z wyciętymi uprawnieniami cap-drop ALL.80
- **Wada:** Brak natywnego wsparcia dla protokołu MCP (stan na kwiecień 2026), co utrudnia integrację z ekosystemem narzędzi Octadecimal.84

### Microsoft Agent Governance Toolkit (Agent OS): Jądro strażnicze

W kwietniu 2026 roku Microsoft wydał AGT (Agent Governance Toolkit), który stał się fundamentem dla wszystkich systemów wymagających rygorystycznego egzekwowania rulebooka.5
**Architektura bezpieczeństwa:** AGT wprowadza „Agent OS” – bezstanowy silnik polityk działający jako jądro, które przechwytuje każdą akcję agenta przed jej wykonaniem.5

- **Latencja:** Silnik zapewnia deterministyczne egzekwowanie reguł (YAML, Rego, Cedar) z latencją p99 poniżej 0.1ms.5
- **Agent Mesh:** Każdy agent Octadecimal otrzymuje unikalną tożsamość kryptograficzną opartą na DIDs (Decentralized Identifiers). Komunikacja między agentami (np. przekazanie zmiennych środowiskowych) wymaga „uścisku dłoni” Trust Handshake.5
- **Execution Rings:** Inspirowane poziomami przywilejów CPU, AGT izoluje agentów w pierścieniach. Agent deweloperski może działać w pierścieniu bez dostępu do sieci, podczas gdy agent deployment-manager ma dostęp do zewnętrznych endpointów.5

**Zastosowanie w Octadecimal:** Toolkit ten integruje się z automation assistant poprzez callback handlers i middleware, pozwalając na wdrożenie 3-level escalation bez modyfikacji kodu agentów.5 Jest to jedyny system w 2026 r., który w pełni adresuje wszystkie 10 zagrożeń OWASP dla autonomicznych agentów.5

### BMAD-METHOD v6: Inżynieria precyzyjna i rygor SDLC

BMAD (Breakthrough Method for Agile AI-Driven Development) ewoluowało w 2026 roku w kompletny ekosystem do industrializacji możliwości AI.12 Jest to framework szczególnie ceniony w branżach regulowanych, takich jak finanse i ochrona zdrowia, ze względu na wbudowaną auditowalność.12
**Metodyka i modelowanie zespołów:** BMAD definiuje 19 specjalistycznych agentów, z których każdy posiada unikalny system prompt i restrykcyjne uprawnienia do kontekstu.12 System „Story-File Architecture” rozwiązuje problem degradacji jakości LLM Opus 4.7 przy dużym zapełnieniu okna kontekstowego.12 Zamiast ładować całe repozytorium, agenci deweloperscy otrzymują atomowe pliki historii (story.md), które zawierają jedynie niezbędne fragmenty architektury i kryteria akceptacji.12
**Integracja i party mode:** Unikalną cechą BMAD jest „Party Mode”, który pozwala na zwołanie sesji dyskusyjnej między wieloma personami (np. Architect, PM i QA) w celu rozstrzygnięcia sprzeczności w specyfikacji przed rozpoczęciem implementacji.27 Framework integruje się z automation assistant poprzez slash commands, mapując np. /bmad.prd na pełny proces generowania dokumentacji wymagań.12
**Governance fit:** BMAD wymusza proces „Adversarial Review”, w którym agent QA jest zobligowany do znalezienia błędów; brak uwag przy jednoczesnym braku pokrycia testami skutkuje wstrzymaniem orkiestracji.37 Wszystkie artefakty są wersjonowane w Git, co tworzy „docs-as-code” governance layer idealnie pasujący do wymogów Octadecimal.29

### Infrastruktura: Apple Silicon M5 i macOS Tahoe (v26)

Jako software house działający na macOS, Octadecimal musi wykorzystać przełom w konteneryzacji, jaki przyniósł system Tahoe w połączeniu z procesorem M5.6

#### Procesor M5: Super Cores i Neural Accelerators

Układ M5 wprowadza nową nomenklaturę rdzeni: Super Cores.6 Każdy z nich posiada 1MB prywatnej pamięci cache L2, co drastycznie przyspieszają operacje na bazach wektorowych takich jak AgentDB w Ruflo.6

- **MLX i Metal 4:** macOS Tahoe 26.2 odblokowuje pełny dostęp do akceleratorów neuronowych w każdym rdzeniu GPU M5.42 Pozwala to Octadecimal na 4-krotny wzrost wydajności lokalnego przetwarzania modeli (np. Ollama Llama 3.2), które mogą pełnić rolę lokalnych weryfikatorów (gatekeepers) przed wysłaniem zapytania do chmury LLM provider.42
- **Thunderbolt 5 Clustering:** Thunderbolt 5 (80Gb/s) umożliwia klastrowanie wielu urządzeń Mac w jedną jednostkę obliczeniową do orkiestracji, co pozwala na obsługę 1M tokenów okna kontekstowego z natywną prędkością.10

#### Native Containerization Framework vs Docker

Tahoe wprowadza natywny framework konteneryzacji oparty na Swift, który eliminuje potrzebę stosowania Docker Desktop w wielu scenariuszach.43

- **VM-per-container:** Każdy kontener Linux działa w swojej własnej, lekkiej maszynie wirtualnej, zapewniając izolację na poziomie sprzętowym.43 Jest to kluczowe dla Octadecimal, chroniąc hosta przed błędami agentów pracujących w trybie „YOLO”.43
- **Startup time:** Dzięki binariom statycznym (Swift Static Linux SDK) i optymalizacji pod M5, kontenery Tahoe startują w ułamku sekundy, podczas gdy Docker Desktop nadal zmaga się z narzutem VM.43
- **Networking:** Każdy kontener otrzymuje własny adres IP, eliminując potrzebę port-forwardingu, co ułatwia budowę rozproszonych systemów federacji Ruflo przez WireGuard.21

## Zarządzanie wiedzą: Strategia 4-warstwowa (Knowledge Propagation)

Aby uniknąć degradacji inteligencji agentów (context poisoning), Octadecimal musi wdrożyć hierarchiczną strukturę wiedzy.50

1. **Warstwa 1: Pamięć osobista (Local Memory):** Wykorzystuje SQLite WAL (Write-Ahead Logging) do przechowywania specyficznych preferencji założyciela i krótkoterminowej pamięci sesji.63 Dane te są wstrzykiwane dynamicznie poprzez plik `~/.llm/settings.json`.65
2. **Warstwa 2: Pamięć projektu (Repo Standards):** Plik project-context.md i folder .llm/skills/. BMAD v6 generuje te pliki automatycznie po fazie Architecture, zapewniając, że deweloperzy AI zawsze wiedzą, jaki tech-stack jest aktualnie używany i jakie są reguły Monorepo.37
3. **Warstwa 3: Pamięć zespołowa (Role-based Boundaries):** Ustrukturyzowane handoffy dokumentacji. Deweloper AI nie ma dostępu do całego PRD, a jedynie do fragmentów story.md odpowiednich dla jego zadania. Każdy zespół (Frontend, Backend, Security) posiada własną „osobowość” zdefiniowaną w plikach .chatmode.md.12
4. **Warstwa 4: Pamięć firmowa (Knowledge Catalog):** Bramka IBM ContextForge lub Google Knowledge Catalog jako centralny hub wiedzy.69 Pozwala to na federację wiedzy między różnymi projektami Octadecimal – np. biblioteka walidacji stworzona w Projekcie A staje się dostępna jako „skill” dla agentów w Projekcie B poprzez uniwersalny endpoint MCP.70

## Standardy Governance Octadecimal (Rulebook 2026)

Governance w Octadecimal musi opierać się na systemie „Compliance-as-Code”.5

- **Saga Orchestration:** Dla wieloetapowych zadań zmieniających stan (np. migracja DB + update kodu + deploy), Octadecimal musi używać wzorca Saga wspieranego przez Microsoft AGT.5 Jeśli agent zawiedzie na etapie 3, system AGT musi automatycznie wywołać akcje kompensacyjne zdefiniowane w rulebooku.5
- **Circuit Breakers:** Należy wdrożyć progi odcięcia na poziomie orkiestratora. Jeśli agent wykona więcej niż 5 nieudanych prób wywołania narzędzia pod rząd, sesja musi zostać natychmiast zescalowana do L3 (Notify-user).

### Links

- **BMAD-METHOD:** [github.com/TheDarkSkyXD/BMAD-METHOD-AI-Vibe-Planning-v6](https://github.com/TheDarkSkyXD/BMAD-METHOD-AI-Vibe-Planning-v6)
- **OpenHands:** [github.com/All-Hands-AI/OpenHands](https://github.com/All-Hands-AI/OpenHands)