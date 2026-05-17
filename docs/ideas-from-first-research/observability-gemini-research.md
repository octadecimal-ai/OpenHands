# Nowoczesne systemy obserwacji i governance w platformach wieloagentowych: Raport rekonesansowy dla Octadecimal

W połowie maja 2026 roku inżynieria systemów wieloagentowych przechodzi z fazy "vibe coding" do fazy rygorystycznego **Agentic Governance**. Dla Octadecimal przejście z automation assistant na **OpenHands (v1.7)** w połączeniu z **Microsoft Agent Governance Toolkit (AGT)** oraz metodologią **BMAD-METHOD v6** stanowi fundament do budowy systemów klasy Enterprise na natywnej infrastrukturze **macOS Tahoe 26.4.1**. Raport ten analizuje synergię tych narzędzi w kontekście pełnej obserwacji, kontroli kosztów i trwałości decyzji.

## TL;DR

* **Fundament operacyjny:** OpenHands v1.7 jako silnik egzekucyjny wykorzystujący natywny stos container w macOS Tahoe dla sprzętowej izolacji (micro-VMs).
* **Warstwa Governance:** Microsoft Agent Governance Toolkit (AGT) jako "kernel" systemu, wprowadzający sub-milisekundową egzekucję polityk (YAML/OPA) i pierścienie przywilejów (Execution Rings).
* **Metodologia i Artefakty:** BMAD-METHOD v6 do strukturyzacji procesu (Analyst → Architect → Dev) i generowania żywej dokumentacji w formacie Markdown.
* **Analityka Kosztów:** Hybrydowy model wykorzystujący LiteLLM (proxy) zintegrowany z AGT RateLimiting, uwzględniający specyfikę Prompt Caching w modelach LLM 4.6/4.7.
* **Trwałość Danych:** Wykorzystanie OpenTelemetry (OTel) natywnie wspieranego przez OpenHands i AGT, z backendem w Laminar lub MLflow.

## Layer-by-layer recommendation: Rekomendacje warstwowe

### 1. Conversation Log (Log konwersacji z founderem)

OpenHands v1.7 opiera się na **Event Stream** jako jedynym źródle prawdy (single source of truth). Każda interakcja jest zapisywana jako MessageEvent w append-only logu.

* **Narzędzie:** OpenHands EventLog (JSONL).
* **Zaleta:** Pozwala na pełny replay sesji i rekonstrukcję stanu konwersacji.

### 2. Inter-team communication log (Komunikacja między agentami)

Komunikacja w systemach wieloagentowych BMAD v6 wymaga śledzenia rozproszonego.

* **Narzędzie:** **OpenLLMetry** zintegrowane z OpenHands SDK.
* **Zaleta:** Automatyczna instrumentacja agent.step i wywołań narzędzi (tool calls) z przesyłaniem śladów do backendu OTLP (np. Laminar).

### 3. Decision Registry (Rejestr decyzji i rationale)

Decyzje są rozproszone między intencją (BMAD) a egzekucją (AGT).

* **Narzędzie:** **AGT AuditLogger** (JSONL z łańcuchem skrótów/hash-chain) + **BMAD ARCHITECTURE.md**.
* **Zaleta:** AGT zapewnia kryptograficzną niezaprzeczalność decyzji (HMAC-signed), a BMAD czytelne dla człowieka uzasadnienie biznesowe.

### 4. Team Observations (Logi usprawnień)

BMAD v6 wprowadza **Continuous Learning Loop**, gdzie agenci QA i Architect analizują artefakty po każdym sprincie.

* **Narzędzie:** BMAD **Step-File System**.
* **Zaleta:** Agenci zapisują stan w drobnoziarnistych plikach kroków, co pozwala na analizę błędów bez utraty kontekstu długich zadań.

### 5. Cost and Time Tracking (Koszty i czas)

* **Narzędzie:** **LiteLLM Proxy** (backend dla OpenHands) + **AGT Agent SRE** (monitoring SLO i budżetów błędów).
* **Zaleta:** Precyzyjne śledzenie tokenów (w tym Cache Hits) na poziomie każdego spanu w OTel.

---

**Architecture: Tahoe Native Security Stack**

Rekomendowana architektura dla Octadecimal wykorzystuje unikalne cechy macOS Tahoe 26.4.1.

### Komponenty:

1. **Runtime:** macOS Tahoe container CLI. W przeciwieństwie do Docker Desktop, Tahoe uruchamia każdy kontener w dedykowanej micro-VM (Virtualization.framework), zapewniając izolację sprzętową.
2. **Agent Core:** OpenHands v1.7. Wykorzystuje DockerWorkspace (skonfigurowany pod Tahoe CLI) do egzekucji akcji.
3. **Governance Kernel:** Microsoft AGT (Agent OS). Interceptuje każde wywołanie narzędzia (ToolCallInterceptor) i sprawdza je z polityką YAML przed wykonaniem w kontenerze.
4. **Process:** BMAD-METHOD v6. Definiuje role (Analyst, PM, Architect, Dev, QA) i wymusza przejście przez fazy: Analysis → Planning → Solutioning → Implementation.

| Cecha | Apple Native Containers (Tahoe) | Docker Desktop |
| :---- | :---- | :---- |
| **Startup Speed** | < 1s (micro-VMs) | 3-10s (shared VM) |
| **Isolation** | Hardware-level per container | Software-level in shared VM |
| **Resource Usage** | Zero overhead w spoczynku | Stały pobór RAM przez daemon |

*Źródło:*

---

**Cost-tracking deep dive: Prompt Caching w LLM 4.6/4.7**

W systemie OpenHands, który przesyła cały log zdarzeń (EventLog) przy każdym kroku, **Prompt Caching** jest krytyczny dla opłacalności.

### Model kosztów LLM provider (Maj 2026):

* **Cache Write (5 min):** 1.25x ceny Input (np. $3.75/MTok dla Sonnet 4.6).1
* **Cache Write (1 h):** 2x ceny Input ($6.00/MTok dla Sonnet 4.6). Optymalny dla sesji developerskich.2
* **Cache Read (Hit):** 0.1x ceny Input ($0.30/MTok). **90% oszczędności**.1

**Strategia dla Octadecimal:**
Wykorzystanie funkcji LanguageModelSession.prewarm() w macOS Tahoe, która natywnie wspiera cachowanie instrukcji i prefixów promptów, redukując Time to First Token (TTFT).

---

**Decision Registry & Schema Sketches**

### Propozycja formatu rejestru (AGT Evidence)

Każda decyzja w AGT jest zapisywana jako AuditEntry.

```json
{
  "entry_id": "uuid-v4-1234",
  "timestamp": "2026-05-14T20:00:00Z",
  "agent_did": "did:web:octadecimal.ai:dev-agent",
  "action": "allow",
  "resource": "shell_command",
  "data": {
    "command": "rm -rf ./temp",
    "rationale": "Cleanup after successful build as per BMAD story #42",
    "bmad_phase": "Implementation"
  },
  "policy_decision": "Permitted",
  "matched_rule": "allow-cleanup-commands",
  "previous_hash": "sha256-abc123..."
}
```

*Źródło:*

### Zdarzenie: Team Observation (BMAD v6)

```json
{
  "observation_id": "obs_998",
  "agent_role": "QA_Architect",
  "type": "STUCK_DETECTION",
  "content": "Agent próbował edytować plik konfiguracyjny 3 razy bez sukcesu. Brak uprawnień w AGT Ring 3.",
  "proposal": "Podnieś uprawnienia dla kontenera 'deploy-worker' w pliku governance-policies.yaml",
  "metadata": {
    "otel_trace_id": "trace-887",
    "step_file": "./bmad/steps/step_04_fix.json"
  }
}
```

*Źródło:*

---

**Retention Strategy (Retencja danych)**

Dla jednoosobowego software house'u rekomenduje się model **Zero-Ops Analytics**:

1. **Hot (0-14 dni):** JSONL na dysku (OpenHands EventLog + AGT AuditLog). Bezpośredni dostęp dla agentów.3
2. **Warm (14-90 dni):** DuckDB. Kompresja kolumnowa logów konwersacji i telemetrii. Pozwala na szybkie zapytania SQL o koszty i błędy.4
3. **Cold (90+ dni):** Parquet na S3/Object Storage. Wykorzystanie formatu ASIF (Apple Sparse Image Format) dla wydajnego składowania obrazów kontenerów i ich stanów.

---

**Open Questions and Red Flags**

* **Networking w Tahoe:** macOS 26.4.1 wciąż posiada ograniczenia w orkiestracji sieci między kontenerami (brak natywnego compose). Skomplikowane topologie wymagają ręcznej konfiguracji mostków sieciowych.
* **Memory Overhead:** Model "VM per container" zużywa więcej RAM niż tradycyjny Docker (każda micro-VM ma własny kernel). Przy systemach z 10+ agentami zalecane jest minimum 32GB RAM.
* **AGT Maturity:** Microsoft Agent Governance Toolkit jest w fazie Public Preview. Należy monitorować stabilność integracji z OpenHands, która obecnie wymaga niestandardowych adapterów ToolCallInterceptor.
* **Zależność od Apple Silicon:** Stos Tahoe Containers nie wspiera procesorów Intel, co wyklucza starsze stacje robocze z floty Octadecimal.

## Dodatkowe rekomendacje (Suggested Tools)

1. **Laminar:** Najlepszy backend dla śladów OpenHands, oferujący "Session Replay" z przeglądarki agenta.
2. **MLflow:** Jeśli planujesz ewaluację modeli "LLM-as-a-judge" na dużą skalę, MLflow posiada gotowe integracje z OpenHands.
3. **Hodoscope:** Narzędzie do analizy trajektorii agentów (identyfikacja zapętleń i luk w logice), które ujawniło podatności w benchmarkach agentów kodujących.

#### Cytowane prace

1. LLM API Pricing 2026: Full LLM provider Cost Breakdown \- MetaCTO, otwierano: maja 14, 2026, [https://www.metacto.com/blogs/llm-provider-api-pricing-a-full-breakdown-of-costs-and-integration](https://www.metacto.com/blogs/llm-provider-api-pricing-a-full-breakdown-of-costs-and-integration)
2. LLM provider API Pricing: What Every LLM Model Costs in 2026 \- PE Collective, otwierano: maja 14, 2026, [https://pecollective.com/tools/llm-provider-api-pricing/](https://pecollective.com/tools/llm-provider-api-pricing/)
3. What is data retention? Rules, Compliance, and Strategies Across Industries \- RDS Data, otwierano: maja 14, 2026, [https://rdsolutionsdata.io/what-is-data-retention-rules-compliance-and-strategies-across-industries/](https://rdsolutionsdata.io/what-is-data-retention-rules-compliance-and-strategies-across-industries/)
4. Top Open Source LLM Observability Tools in 2026 \- OpenObserve, otwierano: maja 14, 2026, [https://openobserve.ai/blog/llm-observability-tools/](https://openobserve.ai/blog/llm-observability-tools/)
5. Tracellm: A lightweight Logging Framework for LLM Applications | by ..., otwierano: maja 14, 2026, [https://medium.com/@manu.k81/tracellm-a-lightweight-logging-framework-for-llm-applications-873f87996436](https://medium.com/@manu.k81/tracellm-a-lightweight-logging-framework-for-llm-applications-873f87996436)