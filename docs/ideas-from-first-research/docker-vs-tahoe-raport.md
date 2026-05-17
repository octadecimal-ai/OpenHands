# Docker vs Apple Container (macOS Tahoe) – raport dla Octadecimal

_Data: 2026-05-14_

## 1. Kontekst i założenia

Octadecimal rozwija wielo‑agentową platformę uruchamianą lokalnie na Macach z Apple Silicon (MacBook Pro M1 16 GB RAM oraz MacBook Pro M5 24 GB RAM). System team działa na hoście macOS i zarządza kontenerami uruchamiającimi poszczególne zespoły agentów.

Na macOS Tahoe (26) pojawiło się natywne narzędzie **Apple `container`** oraz framework **Containerization**, pozwalające uruchamiać obrazy OCI (np. Docker) jako lekkie VM‑kontenery bez Docker Desktop.[web:63][web:65][web:80] Celem raportu jest porównanie:

- **Docker Desktop na macOS** (klasyczne rozwiązanie),
- **Apple `container` (macOS Tahoe)**,

pod kątem lokalnego developmentu i uruchamiania zespołów agentów w Octadecimal.

---

## 2. Jak działają oba runtime’y

### 2.1 Docker Desktop na macOS

Docker Desktop na macOS uruchamia kontenery **wewnątrz jednej wspólnej VM z Linuxem** (LinuxKit), korzystając z Virtualization.framework / Hypervisor.framework jako backendu.[web:79][web:86] Kontenery współdzielą kernel, używając mechanizmów namespaces/cgroups dokładnie tak, jak na natywnym Linuksie.[web:79] Komunikacja z hostem odbywa się przez warstwę sieciową i filesystemową tej VM.

Konsekwencje:

- Jeden „gruby” Linux VM trzyma w pamięci jądro i podstawowe usługi, niezależnie od liczby kontenerów.[web:79][web:86]
- Docker API (daemon) udostępnia pełny ekosystem: **Docker CLI, Docker Compose, integracje z IDE, lokalny Kubernetes, pluginy itd.**[web:72][web:86]
- Z perspektywy narzędzi (CI, IDE) macOS jest „prawie jak Linux”, ale z dodatkową warstwą abstrakcji.

### 2.2 Apple `container` na macOS Tahoe

Apple wprowadził natywny **Containerization framework** i CLI `container`, który uruchamia obrazy OCI jako **lekkie, dedykowane mikro‑VM‑y Linux**.[web:63][web:67][web:80] Kluczowe cechy:

- **VM-per-container**: każdy kontener to osobna VM z własnym kernelem.[web:68][web:69] Izolacja nie opiera się na przestrzeniach nazw, ale na granicy VM.
- Wykorzystanie **Virtualization.framework** i Containerization, napisane w Swift, **zoptymalizowane pod Apple Silicon** – brak dużego, stałego daemona w tle.[web:63][web:67][web:80]
- Obsługa **OCI‑compatible images** – można używać obrazów z Docker Hub / GitHub Container Registry.[web:63][web:74][web:80]

Różnica koncepcyjna:

- Docker Desktop: _„wiele kontenerów w jednej VM”_.
- Apple `container`: _„jeden kontener = jedna mikro‑VM”_.[web:68][web:79]

---

## 3. Porównanie techniczne Docker vs Apple `container`

### 3.1 Wydajność i zużycie zasobów

Różne benchmarki (blogi, testy społeczności, raporty firm trzecich) wskazują na istotne różnice w **czasie startu** i **zużyciu zasobów**.[web:74][web:78][web:80]

#### 3.1.1 Startup i idle footprint

- Zestawienie z KubeAce pokazuje, że kontenery Apple startują **sub‑second**, podczas gdy Docker Desktop potrzebuje typowo 3–5 s na start kontenera i 10–30 s na rozruch VM.[web:74]
- W tym samym źródle idle footprint Docker Desktop to zwykle **500 MB–2 GB RAM** i 5–15% CPU, podczas gdy `container` utrzymuje się **< 200 MB RAM i < 2% CPU** przy braku aktywności.[web:74]
- Inne benchmarki (RepoFlow) potwierdzają, że Apple Container już w wersji 0.6.0 oferuje **konkurencyjne zużycie CPU/memory**, mimo że nie zawsze wygrywa z alternatywami (np. OrbStack) w każdej metryce.[web:76][web:78]

Wnioski dla Octadecimal:

- Na MacBooku M1 16 GB RAM, gdzie każdy GB pamięci się liczy, **Apple `container` znacząco ograniczy „tłusty” idle overhead** w porównaniu z Docker Desktop.[web:74][web:80]
- Na MacBooku M5 24 GB RAM zysk jest mniejszy, ale wciąż odczuwalny przy wielu równoległych agentach.

#### 3.1.2 CPU i IO

- Apple `container` jest zoptymalizowany dla ARM64, co daje przewagę przy natywnych obrazach arm64 – mniej warstw translacji i lepsze wykorzystanie rdzeni M‑series.[web:74][web:80]
- Docker Desktop może być odpowiednio skonfigurowany (VirtioFS, natywne ARM64 images, Rosetta dla x86_64), ale nadal niesie overhead warstwy LinuxKit.[web:86]
- RepoFlow zwraca uwagę, że choć Apple Container jest mocny w CPU/memory, inne runtime’y mogą być lepsze przy operacjach na wielu małych plikach (FS performance) – ważne dla buildów.[web:76][web:78]

Wnioski dla Octadecimal:

- Dla **CPU‑bound agentów** (ML, przetwarzanie tekstu, enumeracja kodu) natywny runtime Apple da lepszy stosunek performance/watt.[web:74][web:80]
- Dla **buildów z dużą ilością małych plików** Docker Desktop lub specjalizowane rozwiązania (np. OrbStack) nadal mogą wygrywać w FS throughput.[web:76][web:78]

### 3.2 Model izolacji i bezpieczeństwo

#### Docker Desktop

- Wszystkie kontenery współdzielą jeden kernel Linux w VM; kompromitacja kernela potencjalnie daje dostęp do wszystkich kontenerów.[web:79]
- W praktyce większość zagrożeń jest i tak zamknięta w VM, ale przy wielu kontenerach to wciąż **„shared fate”**.

#### Apple `container`

- Każdy kontener ma **własny kernel i VM**, podobnie jak w Kata Containers / Firecracker.[web:61][web:68]
- Atakujący musiałby wyjść z jednej mikro‑VM i wejść do innej, zamiast atakować wspólny kernel.

Dla Octadecimal (agenci LLM wykonujący narzędzia, pluginy, potencjalnie nieufny kod z internetu):

- Apple `container` zapewnia naturalnie **silniejszą izolację między zespołami agentów**, co dobrze się wpisuje w architekturę „każdy agent / team = osobny kontener”.[web:68][web:61]

### 3.3 Networking

#### Docker Desktop

- Jeden VM zapewnia typowy **bridge networking** z port mapping, `host.docker.internal` jako alias hosta, wsparcie Compose dla sieci między usługami.[web:79][web:86]
- Dla architektury „agenci w kontenerach → System team na hoście” typowy pattern to HTTP/gRPC na `host.docker.internal:PORT`, co dobrze działa z Compose.[web:79]

#### Apple `container`

- Apple wykorzystuje **vmnet** i przydziela **dedykowane IP dla każdej mikro‑VM**; advanced networking (IP‑per‑container, bridge) działa w pełni dopiero na macOS 26 Tahoe.[web:69][web:71][web:80]
- Raporty wskazują, że na macOS 15 inter‑container networking był ograniczony – kontenery w tej samej sieci nie widziały się wzajemnie, co jest blockerem dla multi‑service setupów.[web:68]

Konsekwencje dla Octadecimal:

- Dla prostego scenariusza „kontener agenta → System team na hoście” Apple `container` jest wystarczający, jeśli System team nasłuchuje na IP hosta z poprawnie skonfigurowanym dostępem (Local Network permission).[web:80]
- Dla większych stosów dev (agenci + bazy + serwisy pomocnicze) **Docker Desktop ma dojrzały model Compose‑networks**, Apple jeszcze nie.[web:68][web:85]

### 3.4 Orkiestracja i ekosystem narzędzi

#### Docker Desktop

- Dojrzały, szeroko adoptowany ekosystem:
  - **Docker Compose** dla multi‑service stacks,[web:72][web:86]
  - Integracje z IDE (VSCode, JetBrains),
  - Narzędzia monitoringu, debugowania, lokalny Kubernetes,
  - Szerokie wsparcie w CI/CD.

#### Apple `container`

- CLI jest młode (pre‑1.0); blogi i testy z 2025–2026 jasno mówią o **braku Compose, braku zaawansowanej orkiestracji, braku integracji z Kubernetes**.[web:68][web:85][web:76]
- Obsługuje podstawowe operacje: pull, run, stop, logi, proste sieci; „glue tooling” trzeba napisać lub wygenerować samodzielnie (Makefile, skrypty, własny orchestrator).[web:68][web:80]
- Pojawiają się pierwsze GUI/integrowane narzędzia (np. Podman Desktop Apple Container extension), ale to wciąż nisza.[web:71][web:77]

Wnioski:

- Docker Desktop jest nadal **lepszym wyborem dla złożonych środowisk dev**, gdzie potrzebujesz Compose, wielu usług, standaryzacji zespołowej.[web:72][web:85]
- Apple `container` jest obecnie **świetnym narzędziem do izolowanych, pojedynczych kontenerów** (single service, single agent), co wielu testów i relacji użytkowników wprost rekomenduje.[web:68][web:85]

### 3.5 Dojrzałość, stabilność i wersje macOS

- Apple `container` wymaga macOS Tahoe (26) dla pełni funkcji, z ograniczonym wsparciem na macOS 15 (problemy z networkingiem, brak niektórych usprawnień).[web:68][web:69][web:82]
- Docker Desktop jest dojrzały i wspierany na kilku generacjach macOS; jego backend (Docker VMM) jest aktywnie rozwijany, a Docker jest świadomy Apple Containers i analizuje ewentualną integrację backendową.[web:81][web:79]

Dla Octadecimal, gdzie docelowo oba laptopy mogą być na Tahoe, Apple `container` jest dostępny, ale trzeba założyć **częstsze zmiany i możliwość breaking changes** w kolejnych minor release’ach.

---

## 4. Specyficzne skutki dla architektury Octadecimal

### 4.1 System team i IPC

Obecna rekomendacja architektury przewiduje System team jako hostowy daemon (Hammerspoon + Swift helper) wystawiający HTTP/gRPC na `localhost`/`127.0.0.1`.[web:45][web:53] Agenci w kontenerach łączą się z nim przez:

- `host.docker.internal` (Docker Desktop),
- odpowiednie IP hosta / vmnet + Local Network permission (Apple `container`).[web:80][web:79]

Z tej perspektywy:

- **O ile System team nie zakłada nic Docker‑specyficznego**, tylko zwykłe HTTP/gRPC, przełączenie agenta z Dockera na Apple `container` jest kwestią konfiguracji endpointu.
- Można zbudować małą warstwę abstrakcji („backend kontenerów”) w System team, która decyduje, czy wywołać `docker`, `podman` czy `container` CLI do uruchomienia danego agenta.[web:63][web:74]

### 4.2 Izolacja zespołów agentów

Wieluagentowe środowisko Octadecimal naturalnie dzieli się na:

- „zaufane” komponenty (System team na hoście),
- „pół‑zaufane” zespoły agentów (różne modele, narzędzia, pluginy),
- „niezaufane” payloady od użytkownika / internetu.

Apple `container` zapewnia mocniejszą izolację między tymi warstwami, co jest szczególnie wartościowe przy:

- wykonywaniu kodu generowanego przez modele,
- odpalaniu zewnętrznych CLI/SDK w kontenerze,
- pracy z danymi, które nie powinny „przeciekać” między agentami.

Docker Desktop nadal daje izolację, ale w granicy jednej VM Linux; kompromitacja tej VM potencjalnie dotyka wszystkie kontenery, choć nie host.

### 4.3 Wielkość stosów i zużycie RAM

- Dla **pojedynczych agentów / pojedynczych kontenerów** Apple `container` ma dużą przewagę: sub‑second start, brak stale działającego daemona, mały footprint.[web:74][web:80]
- Dla **zestawów kilku usług** (agent + Postgres + Redis + kolejny serwis) Docker Desktop jest bardziej efektywny pamięciowo, bo wszystkie kontenery współdzielą jedną VM; w Apple `container` każdy kontener = osobna VM, więc kernel overhead sumuje się.[web:68][web:82]

W praktyce:

- Do „lightweight teams” (np. pojedynczy agent + minimalny tooling) Apple `container` na M1/M5 będzie bardzo atrakcyjny.
- Do większych środowisk dev/test (np. cały stack aplikacji klienta) Docker Desktop nadal jest rozsądniejszy.

---

## 5. Rekomendacje dla Octadecimal

### 5.1 Nie zastępuj Dockera – użyj hybrydy

W roku 2026, przy obecnym stanie ekosystemu, **Apple `container` nie jest jeszcze „killerem” Docker Desktop**, ale jest **świetnym uzupełnieniem do izolowanych, jedno‑kontenerowych workflowów**.[web:68][web:80][web:60]

Rekomendacja:

- Utrzymaj **Docker (lub Podman) jako główny runtime** dla:
  - CI/CD,
  - złożonych stacków dev (Compose),
  - środowisk zbliżonych do Linux produkcji.
- Dodaj **Apple `container` jako drugi runtime na MacBookach** dla:
  - pojedynczych agentów / teamów,
  - lekkich narzędzi pomocniczych (np. kontener do migracji DB, krótkie joby),
  - sytuacji, gdy zależy ci na izolacji i minimalnym idle overhead na baterii.

### 5.2 Wzorzec „runtime pluggable” w System team

Zaplanuj System team tak, aby „kontenery” były tylko transportem dla agentów, a nie twardo powiązane z Dockerem:

- Zdefiniuj kontrakt „uruchom agenta X w runtime Y” z parametrami:
  - obraz (OCI reference),
  - komenda wejściowa,
  - zmienne środowiskowe (np. URL System team),
  - limity zasobów.
- Zaimplementuj dwa backendy:
  - `docker_backend` – `docker run`, Compose, itp.,
  - `apple_container_backend` – `container run`, z mapowaniem portów/IP zgodnie z vmnet.

To pozwala:

- na M1/M5 wybierać runtime per agent (np. „security‑sensitive tool” → Apple `container`, „stack dev” → Docker),
- później wpiąć dodatkowe backendy (np. K8s, remote runner).

### 5.3 Strategia adopcji

1. **Pilot na MacBooku Pro M5 (24 GB, macOS Tahoe)**:
   - zainstaluj Apple `container` (Homebrew lub oficjalny installer), uruchom `container system start` i przetestuj kilka obrazów OCI (np. istniejące obrazy agentów Octadecimal).[web:80][web:82][web:74]
   - zmierz startup times i RAM/CPU vs Docker Desktop dla typowych workflowów agentów.

2. **Wyselekcjonuj 1–2 zespoły agentów o profilu „single container”**:
   - np. narzędzia do refaktoryzacji kodu, proste ETL,
   - przepnij je na Apple `container` w środowisku lokalnym, zachowując możliwość powrotu do Dockera przez config.

3. **Zbuduj minimalne narzędzia do orkiestracji po swojej stronie**:
   - proste skrypty/makefile, które „wiedzą”, jak startować kontenery w `container`,
   - integrację w Dev tooling (np. VSCode tasks), by zminimalizować friction.

4. **Pozostań przy Docker Desktop dla Compose i multi‑service**:
   - do czasu, aż Apple doda pierwszy‑klasowy odpowiednik Compose lub pojawią się stabilne narzędzia community, **Compose + Docker** powinien zostać głównym rozwiązaniem przy złożonych stackach.[web:68][web:76][web:85]

### 5.4 Kryteria sukcesu

Warto zdefiniować wewnętrzne KPI, po których uznasz, że Apple `container` „zdał egzamin” dla częśći workflowów:

- **Redukcja idle RAM/CPU** na M1/M5 względem Docker Desktop przy typowym zestawie agentów.[web:74][web:78]
- **Brak istotnych regresji** w stabilności (crashe, zawieszające się kontenery, problemy z siecią).[web:80][web:68]
- **Akceptowalna ergonomia** – czy CLI i minimalne własne narzędzia są wystarczające, czy developer experience jest zbyt bolesne vs Docker Desktop.

---

## 6. Podsumowanie

- Apple `container` na macOS Tahoe to **silnie izolowany, lekki runtime kontenerów** oparty o mikro‑VM‑y, zapewniający sub‑second start i niski idle overhead, szczególnie korzystny na Macach z Apple Silicon.[web:63][web:74][web:80]
- Docker Desktop pozostaje **bardziej kompletną platformą** – bogaty ekosystem, Compose, integracje IDE, lepsze wsparcie multi‑service/multi‑container developmentu.[web:72][web:76][web:79]
- Dla Octadecimal optymalna jest **strategia hybrydowa**: Docker (lub Podman) jako główny runtime, Apple `container` jako natywny backend dla izolowanych agentów i lekkich workflowów na MacBookach.
- Kluczem jest zbudowanie **warstwy abstrakcji runtime** w System team, tak aby wybór między Docker a Apple `container` był kwestią konfiguracji, a nie przebudowy architektury.

_Dokument przygotowany z myślą o długofalowym rozwoju platformy Octadecimal w ekosystemie macOS Tahoe, z uwzględnieniem realistycznych ograniczeń młodego runtime’u Apple._