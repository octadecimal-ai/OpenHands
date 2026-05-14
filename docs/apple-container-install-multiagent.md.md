# Instalacja i konfiguracja Apple Container (macOS Tahoe) dla środowiska multi‑agentowego

_Data: 2026-05-14_

## 1. Wymagania wstępne

1. **Sprzęt i system**:
   - Mac z Apple Silicon (M1/M2/M3/M5).[web:63][web:89]
   - macOS 26 „Tahoe” lub nowszy (pełne wsparcie Apple Container).[web:80][web:89]
2. **Narzędzia**:
   - Zainstalowany Homebrew (rekomendowane).[web:88][web:80]
   - Konto administratora z dostępem do `sudo`.

Jeśli nie masz Homebrew, zainstaluj go wg instrukcji na https://brew.sh (jedna linia w Terminalu).[web:88]

---

## 2. Instalacja Apple `container`

Masz dwie główne ścieżki instalacji: przez Homebrew (najprostsza) lub przez signed PKG z GitHuba.

### 2.1 Instalacja przez Homebrew (rekomendowana)

W Terminalu:

```bash
# upewnij się, że brew jest aktualne

brew update

# instalacja container CLI

brew install container
```

Homebrew jest rekomendowaną drogą w wielu przewodnikach (Oracle, blogi dev), bo dostajesz aktualną wersję CLI i łatwe aktualizacje.[web:88][web:80]

Sprawdzenie wersji:

```bash
container --version
```

Powinieneś zobaczyć numer wersji (np. `container 0.10.0`), co potwierdza poprawną instalację.[web:80]

### 2.2 Instalacja signed PKG z GitHuba (alternatywa)

1. Wejdź na repo: `https://github.com/apple/container` → zakładka **Releases**.[web:63][web:81]
2. Pobierz **signed installer** (`container-<version>-installer-signed.pkg`).[web:63]
3. W Terminalu wykonaj:

```bash
export CONTAINER_VERSION="0.4.1"  # sprawdź aktualną wersję w Releases
curl -LO https://github.com/apple/container/releases/download/${CONTAINER_VERSION}/container-${CONTAINER_VERSION}-installer-signed.pkg
sudo installer -pkg container-${CONTAINER_VERSION}-installer-signed.pkg -target /
```

Signed PKG jest notarizowany, co minimalizuje problemy z Gatekeeperem.[web:63]

---

## 3. Uruchomienie i weryfikacja systemu `container`

### 3.1 Start systemowego runtime

Po instalacji wystartuj runtime:

```bash
container system start
```

To uruchamia usługę w tle (`container-runtime-linux`), odpowiedzialną za pobieranie obrazów, zarządzanie mikro‑VM‑ami, sieć i storage.[web:63][web:67][web:80]

Sprawdzenie statusu:

```bash
container system status
```

Powinieneś zobaczyć informację, że system jest uruchomiony (np. „system is running”).[web:63][web:80]

### 3.2 Pierwsze uruchomienie kernela i rootfs

Przy pierwszym `container system start` lub pierwszym uruchomieniu kontenera CLI zwykle zobaczysz prompt w stylu:

```text
No default kernel configured.
Install the recommended default kernel from ... ?
[Y/n]: y
```

Wybierz `Y`, aby pobrać domyślny, rekomendowany kernel i rootfs.[web:67][web:90]

---

## 4. Podstawowe komendy i sanity‑check

### 4.1 Sprawdzenie dostępnych subkomend

Wyświetlenie pomocy:

```bash
container
```

Powinieneś zobaczyć m.in.:

- `run`, `create`, `start`, `stop`, `logs`, `exec`,
- podkomendy obrazów: `image`, `images`, `build`,
- `system` (`system start`, `system status`, `system dns`, itd.).[web:93]

### 4.2 Testowy kontener (np. nginx)

Dla sanity‑check uruchom prosty serwer nginx:

```bash
container run --name test-nginx \
  --cpus 2 --memory 2g \
  -p 8080:80/tcp \
  nginx:latest
```

Parametry:[web:80]

- `--name test-nginx` – nazwa kontenera.
- `--cpus 2` – 2 vCPU dla tej mikro‑VM.
- `--memory 2g` – limit RAM na 2 GB.
- `-p 8080:80/tcp` – port 8080 hosta → 80 w kontenerze.
- `nginx:latest` – standardowy obraz OCI.

Sprawdź w przeglądarce lub curl:

```bash
curl http://localhost:8080
```

Jeśli widzisz stronę powitalną nginx, runtime działa poprawnie.[web:80]

---

## 5. Uprawnienia sieciowe i firewall macOS

Przy pierwszym uruchomieniu kontenera oraz próbie dostępu przez przeglądarkę/CLI macOS może zapytać o **dostęp do Local Network** dla:

- `container-runtime-linux`,
- przeglądarki (Safari/Chrome/Edge),
- terminala (Terminal/iTerm).[web:80]

Jeśli port mapping nie działa:

1. Otwórz **System Settings → Privacy & Security → Local Network**.[web:80]
2. Upewnij się, że wymienione powyżej procesy mają włączony dostęp (toggle ON).
3. Zamknij i ponownie uruchom przeglądarkę/terminal.

To ważne dla scenariusza, w którym kontenerowy agent komunikuje się z hostowym System team przez HTTP/gRPC.[web:80][web:90]

---

## 6. Przygotowanie pod środowisko multi‑agentowe

### 6.1 Konwencja obrazów agentów

Przyjmij, że każdy zespół agenta to osobny obraz OCI, np.:

- `ghcr.io/octadecimal/agent-planner:latest`,
- `ghcr.io/octadecimal/agent-executor:latest`.

System team na hoście będzie startował te obrazy przez `container run`, pilnując nazw, portów i zasobów.

### 6.2 Wzorcowe uruchamianie agenta

Przykład uruchomienia pojedynczego agenta:

```bash
container run --name agent-planner \
  --cpus 2 --memory 4g \
  -p 8101:8080/tcp \
  -e SYSTEM_TEAM_URL="http://127.0.0.1:9000" \
  ghcr.io/octadecimal/agent-planner:latest
```

Założenia:[web:80]

- System team nasłuchuje na `127.0.0.1:9000` na hoście.
- Agent wewnątrz kontenera rozmawia z System team przez `SYSTEM_TEAM_URL` (wskazujący na hosta/port zmapowany przy `-p`).

### 6.3 Limity zasobów per agent

Ponieważ Apple `container` tworzy mikro‑VM per kontener, warto świadomie ustawiać limity CPU/RAM:

- **MBP M1 16 GB RAM**:
  - typowy agent: `--cpus 2 --memory 3g`,
  - równoległe 3–4 takie kontenery pozostawiają komfortowy zapas dla macOS i System team.[web:80][web:88]
- **MBP M5 24 GB RAM**:
  - możesz uruchomić 4–6 agentów z `--cpus 2 --memory 3–4g` każdy, w zależności od obciążenia.[web:80]

Limity są egzekwowane na poziomie VM, więc „zbuntowany” agent nie powinien zabić całego hosta.

### 6.4 Nazewnictwo i inspekcja kontenerów

Przy wielu agentach zadbaj o spójne nazwy:

- `agent-planner-1`,
- `agent-executor-1`,
- `agent-observer-1`, itd.

Przydatne komendy administracyjne:

```bash
# lista kontenerów

container list

# logi konkretnego agenta

container logs agent-planner-1

# interaktywny shell w działającym kontenerze

container exec -it agent-planner-1 /bin/bash

# szczegóły (IP, limity zasobów, config)

container inspect agent-planner-1
```

API `container` jest zbliżone do Dockera/Podmana, więc mentalny model jest podobny.[web:93][web:80]

---

## 7. Konfiguracja „na stałe” (daemon + integracja z toolchainem)

### 7.1 Automatyczny start `container system`

Aby runtime działał po każdym logowaniu/reboocie:

1. Sprawdź dostępne opcje:

   ```bash
   container system --help
   ```

   W nowszych wersjach pojawia się instrukcja typu „To start container now and restart at login, run …”.[web:80][web:92]

2. Alternatywnie, dodaj prosty skrypt shell uruchamiany jako Login Item / LaunchAgent, który wykonuje `container system start` i loguje status.

### 7.2 Abstrakcja runtime (Docker vs Apple `container`)

Aby później łatwo wybierać między Docker a Apple `container` dla agentów Octadecimal:

- Zdefiniuj prosty wrapper (np. `octa-run-agent`), który:
  - czyta config agenta (obraz, porty, zasoby),
  - na podstawie zmiennej `RUNTIME=docker|apple-container` wywołuje `docker run` albo `container run` z odpowiednimi parametrami.
- Utrzymuj jednolity kontrakt z perspektywy System team:
  - System team nie musi „wiedzieć”, czy agent siedzi w Docker czy Apple `container` – wystarczy, że zna jego adres HTTP/gRPC.

Taki wzorzec pozwoli ci eksperymentować z Apple `container` na MBP M1/M5 bez rezygnowania z całego ekosystemu Dockera.

---

## 8. Co dalej?

Po przejściu powyższych kroków masz:

- działający runtime Apple `container` na czystym macOS Tahoe,[web:63][web:80]
- skonfigurowane podstawowe uprawnienia sieciowe,[web:80]
- przetestowany prosty kontener z port mappingiem,
- wzorce CPU/RAM/nazewnictwa kontenerów zgodne z potrzebami multi‑agentów.

Kolejne kroki integracyjne z platformą Octadecimal:

- spięcie System team (HTTP/gRPC) z kontenerami Apple jako jednym z backendów runtime,
- przygotowanie plików konfiguracyjnych (YAML/JSON) opisujących profile agentów (obraz, zasoby, porty),
- stopniowa migracja pojedynczych zespołów agentów na Apple `container` tam, gdzie izolacja i niski overhead są szczególnie ważne.
