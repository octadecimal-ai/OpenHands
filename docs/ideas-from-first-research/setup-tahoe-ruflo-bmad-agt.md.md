# Setup środowiska Octadecimal 2026 – macOS Tahoe + Ruflo + BMAD + AGT

_Data: 2026-05-14_

## 0. Założenia

Docelowy stack Octadecimal (wg raportu Frameworks.md):[file:95]

- **Infrastruktura**: macOS 26 „Tahoe”, Apple Silicon (M1/M5), natywne Apple Container (VM-per-container).[file:95][web:43]
- **Orkiestracja**: **Ruflo v3.5** (dawniej Claude-Flow) jako silnik multi-agent i MCP server.[file:95]
- **Metodyka**: **BMAD-METHOD v6** jako obowiązkowy workflow Spec-Driven Development.[file:95]
- **Bezpieczeństwo**: **Microsoft Agent Governance Toolkit / Agent OS (AGT)** jako warstwa governance / OWASP Agentic Top 10.[file:95]
- **Interfejs**: Claude Code (Agent Teams, hooks, MCP).[file:95]

Instrukcja zakłada czysty macOS Tahoe i prowadzi krok po kroku do gotowego środowiska dev.

---

## 1. Bazowy system i narzędzia

### 1.1 System i Xcode CLI

1. Zaktualizuj macOS do **26 „Tahoe”** (Settings → General → About → Software Update). Wymagane dla natywnej konteneryzacji Apple.[file:95][web:42][web:43]
2. Zainstaluj narzędzia deweloperskie:

   ```bash
   xcode-select --install
   ```

### 1.2 Homebrew, Git, Node, Python

1. Zainstaluj Homebrew (jeśli nie masz):

   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. Zainstaluj podstawowe narzędzia:

   ```bash
   brew update
   brew install git node pnpm python@3.12
   ```

- Node + pnpm przydadzą się do Ruflo, hooków governance i ewentualnych narzędzi TS.[file:95]
- Python dla skryptów pomocniczych i integracji AGT.

---

## 2. Konteneryzacja: Apple Container (i opcjonalnie Docker)

### 2.1 Instalacja Apple `container`

1. Przez Homebrew:

   ```bash
   brew install container
   container --version
   ```

   Powinieneś zobaczyć coś w stylu `container 0.10.0`.[web:80]

2. Start runtime’u:

   ```bash
   container system start
   container system status
   ```

   Status powinien raportować, że system działa (np. `system is running`).[web:63][web:80]

3. Przy pierwszym starcie zaakceptuj instalację domyślnego kernela i rootfs (`Install the recommended default kernel? [Y/n]`).[web:67][web:90]

4. Dodaj automatyczny start runtime’u przy logowaniu (Login Item / LaunchAgent) wywołujący:

   ```bash
   container system start
   ```

### 2.2 Testowy kontener (sanity check)

1. Uruchom prostego nginx:

   ```bash
   container run --name test-nginx \
     --cpus 2 --memory 2g \
     -p 8080:80/tcp \
     nginx:latest
   ```

2. Sprawdź:

   ```bash
   curl http://localhost:8080
   ```

   Jeśli widzisz stronę nginx, kontenery Apple działają.[web:80]

3. Jeżeli macOS pyta o **Local Network** dla `container-runtime-linux`, terminala lub przeglądarki, włącz dostęp w System Settings → Privacy & Security → Local Network.[web:80]

### 2.3 Opcjonalnie: Docker Desktop

1. Pobierz Docker Desktop z https://www.docker.com/products/docker-desktop i zainstaluj.
2. Włącz tryb natywnego ARM64 dla Apple Silicon.[web:86]

Docker pozostaje runtime’em kompatybilnym z całym ekosystemem (Compose, CI), Apple Container będzie natywnym runtime’em dla izolowanych agentów.[file:95][web:72]

---

## 3. Claude Code + Agent Teams + hooks

### 3.1 Instalacja Claude Code

1. Zainstaluj VS Code.
2. W marketplace znajdź i zainstaluj rozszerzenie **Claude Code**.
3. Skonfiguruj klucz Anthropic (wg dokumentacji rozszerzenia / Claude platform).[file:95]

### 3.2 Włączenie Agent Teams i hooks

1. W ustawieniach projektu (np. `.claudesettings.json`) włącz:
   - Agent Teams / multi-agent,
   - hooks (PreToolUse/PostToolUse), zgodnie z dokumentacją „Hooks reference”.[file:95][web:7]

2. W repo Octadecimal utwórz:

   ```bash
   mkdir -p .claudeskills
   touch CLAUDE.md
   ```

3. W `CLAUDE.md` opisz wysokopoziomowy setup (Ruflo, BMAD, AGT, Apple Container) jako kontekst dla Claude Code.[file:95]

---

## 4. Instalacja i integracja Ruflo v3.5

### 4.1 Pobranie i build Ruflo

1. Sklonuj repozytorium Ruflo:[file:95]

   ```bash
   git clone https://github.com/ruvnet/ruflo.git
   cd ruflo
   ```

2. Zainstaluj zależności i zbuduj:

   ```bash
   pnpm install
   pnpm build
   ```

3. Zainstaluj CLI (zależnie od instrukcji w README, przykładowo):

   ```bash
   pnpm link --global
   # albo
   pnpm dlx ruflo@latest --help
   ```

### 4.2 Start demona Ruflo i MCP

1. Uruchom daemon Ruflo:

   ```bash
   ruflo daemon start
   ```

   Ruflo wystawi lokalny MCP server z setkami narzędzi (RuVector Intelligence, AgentDB itd.).[file:95]

2. Sprawdź logi / help, aby poznać port MCP (np. 8710). Zanotuj ten port.

### 4.3 Integracja Ruflo z Claude Code (MCP)

1. W konfiguracji Claude Code dodaj serwer MCP Ruflo:
   - host: `localhost`,
   - port: `PORT_RUFLO` (np. 8710),
   - schema z pliku konfiguracyjnego Ruflo (np. `mcp-config.json`).[file:95]

2. Skopiuj z repo Ruflo pliki integracyjne `CLAUDE.md`, ewentualne przykłady skills, do swojego repo Octadecimal (.claudeskills i/lub opis w głównym `CLAUDE.md`).[file:95]

### 4.4 Ruflo w kontenerach Apple (opcjonalnie)

Jeśli chcesz izolować Ruflo w kontenerze Apple:

```bash
container run --name ruflo-agent \
  --cpus 2 --memory 4g \
  -p 8200:8200/tcp \
  ghcr.io/ruvnet/ruflo:3.5.0
```

Następnie w Claude Code skonfiguruj MCP na `localhost:8200`.[file:95]

---

## 5. BMAD-METHOD v6 – metodyka SDD

### 5.1 Pobranie BMAD

1. Sklonuj rdzeń metodyki BMAD:[file:95]

   ```bash
   git clone https://github.com/bmad-code-org/BMAD-METHOD.git
   ```

2. Przeczytaj przewodniki (`GUIDE`, `docs/`) opisujące 19 ról, Party Mode, story files itd.[file:95]

### 5.2 Integracja BMAD z Claude Code

1. Sklonuj integrację BMAD‑AT‑CLAUDE:[file:95]

   ```bash
   git clone https://github.com/24601/BMAD-AT-CLAUDE.git
   ```

2. Skopiuj skille/konfiguracje BMAD do swojego repo Octadecimal:
   - pliki `.chatmode.md` / `.skill.json` / inne z BMAD‑AT‑CLAUDE do `.claudeskills`.

3. W `.claudesettings.json` / `CLAUDE.md` ustaw, że:
   - każde zadanie > prosty bug-fix **musi przejść przez BMAD workflow** (role `Analyst`, `Architect`, `Dev`, `QA`),
   - dostępne są komendy/skróty BMAD (np. `bmad.prd`, `bmad.arch`).[file:95]

### 5.3 Struktura plików projektu

W repo Octadecimal:

```bash
mkdir -p docs/stories
mkdir -p .claudeskills

touch project-context.md
```

Konwencja:

- `project-context.md` – opis stacku, reguł monorepo, standardów.[file:95]
- `docs/stories/FEATURE-ID-story.md` – atomowe „story files” z minimalną specyfikacją i kryteriami.[file:95]
- `.claudeskills/frontend.chatmode.md`, `backend.chatmode.md`, `security.chatmode.md` – definicje ról BMAD.[file:95]

---

## 6. Microsoft Agent Governance Toolkit (AGT / Agent OS)

### 6.1 Pobranie i build AGT

1. Sklonuj AGT:[file:95]

   ```bash
   git clone https://github.com/microsoft/agent-governance-toolkit.git
   cd agent-governance-toolkit
   ```

2. Zainstaluj zależności i zbuduj:

   ```bash
   pnpm install
   pnpm build
   ```

3. Uruchom Agent OS (policy kernel):

   ```bash
   pnpm run agent-os
   ```

Agent OS będzie nasłuchiwał na lokalnym porcie HTTP/gRPC i egzekwował reguły w czasie < 0.1 ms.[file:95][web:5]

### 6.2 Integracja AGT z Claude Code (hooks)

1. W repo Octadecimal dodaj hook `preToolUse` (np. `hooks/preToolUse.ts`), który:
   - serializuje planowaną akcję narzędzia (MCP call, write-file, shell, HTTP),
   - wysyła ją do AGT (np. `http://127.0.0.1:PORT/agent-os/evaluate`),
   - na podstawie odpowiedzi (`allow`/`deny`/`escalate`) albo przepuszcza, albo blokuje, albo wstrzymuje sesję.[file:95][web:7]

2. W konfiguracji AGT załaduj gotowe reguły OWASP Agentic Top 10 z `docs/OWASP-COMPLIANCE.md`.[file:95]

3. Ustal polityki:
   - `write_external`, `execute` domyślnie `deny`, wymagające L3 human approval,[file:95]
   - pozostałe operacje (np. `read-only`, `local-refactor`) z `allow` po walidacji.

---

## 7. Warstwy pamięci Octadecimal

### 7.1 Warstwa 1 – pamięć osobista (Local Memory)

1. Utwórz katalog i bazę SQLite:

   ```bash
   mkdir -p ~/.octadecimal
   sqlite3 ~/.octadecimal/memory.db "VACUUM;"
   ```

2. Dodaj mały serwis (Node/Python), który:
   - zapisuje preferencje i krótkoterminowe fakty (key/value) do `memory.db`,
   - wystawia MCP/REST jako narzędzie „PersonalMemory” dla Claude Code.[file:95]

### 7.2 Warstwa 2 – pamięć projektu

- `project-context.md` – wypełnij opisem tech‑stacku, standardów, głównych reguł.
- `.claudeskills` – trzymaj tam skille BMAD, Ruflo, governance.[file:95]

### 7.3 Warstwa 3/4 – pamięć zespołowa i firmowa

- `docs/stories/*-story.md` – per feature, per zespół (front/back/security).[file:95]
- (Etap 2) integracja z zewnętrznym **MCP gateway / Knowledge Catalog**, jeżeli zdecydujesz się na ContextForge lub podobne rozwiązanie.[file:95]

---

## 8. Test end-to-end – pierwszy przepływ multi-agentowy

1. **Uruchom infrastrukturę**:

   ```bash
   container system start         # Apple Container
   ruflo daemon start             # Ruflo MCP
   pnpm --dir agent-governance-toolkit run agent-os  # AGT
   ```

   Otwórz VS Code z aktywnym Claude Code (Agent Teams + hooks).

2. **Odpal testowego agenta w Apple Container** (przykładowy obraz twojego agenta):

   ```bash
   container run --name agent-planner \
     --cpus 2 --memory 3g \
     -p 8101:8080/tcp \
     -e SYSTEM_TEAM_URL="http://127.0.0.1:9000" \
     ghcr.io/octadecimal/agent-planner:latest
   ```

3. **W Claude Code**:
   - otwórz repo Octadecimal z BMAD (`project-context.md`, `.claudeskills`, `docs/stories/`),
   - uruchom workflow BMAD (np. komendą typu `bmad.prd`) i wygeneruj specyfikację dla prostej funkcji,[file:95]
   - poproś Ruflo swarm (MCP) o plan zmian i wykonanie części kroków,
   - spróbuj wykonać „ryzykowną” akcję (np. modyfikację `.env`) i upewnij się, że AGT ją blokuje / wymaga approvalu L3.[file:95]

Jeżeli powyższy przepływ działa, masz skonfigurowane rekomendowane środowisko Octadecimal: macOS Tahoe + Apple Container, Ruflo jako silnik multi-agent, BMAD jako metodyka SDD, AGT jako policy kernel oraz Claude Code jako główne IDE.
