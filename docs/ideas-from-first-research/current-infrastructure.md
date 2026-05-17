# Bieąca Infrastruktura Octadecimal

Srodowisko firmowe, które było rozwijane od stycznia 2026 - raczej do wyciągniecia wnioskow, z popełnionych tam błędów, niz jako wskazowka dla nowej architektury.

---

## Hardware

### Stanowisko foundera

- **MacBook Pro M5**, 24 GB RAM, macOS Tahoe 26.4.1.
- Codzienne, mobilne urządzenie pracy foundera.
- Telefon: **Android** (połączony przez KDE Connect; brak iPhone).
- Drugi ekran (TBD: model, charakterystyka).
- z M1 i PC łączy się poprzez ssh na localhoscie, gdy user jest poza lokalną siecią poprzez Tailscale.

### Home server M1

- **MacBook Pro M1**, 16 GB RAM, macOS Tahoe 26.4.1.
- Działający 24/7
- **Kandydat na hosta dla zespołów AI w Dockerze**

### Home server PC

- **PC z Ubuntu** w sieci lokalnej (TBD: spec — RAM, dysk, procesor).
- Działa 24/7.
- Już zintegrowany z **Cloudflare Tunnel** — usługi self-hosted dostępne na zewnątrz pod cloudflare-managed domeną. Domeny są wykupione na OVH.
- **Zainstalowany Docker** a w nim serwisy:
  - **n8n** — nieudana orkestracja agentów businesowych, posiadajacych konta na rocket.chat, łącząca się z zespołami dev poprzez wilson-bridge
  - **Twenty CRM** — aktywnie uzywane narzędzie do planowania z zespołami STORY, podzielonych na subtaski
  - **LangFuse** — zainstalowany, nigdy nie uzywany
  - **Grafana** — podobnie
  - **Rocket.chat** — w pierwszej fazie rozwoju, były próby zarządzania zespołem businessowym, poprzez to narzędzie, ale z powodu duzych problemow, cale zarzadzanie zostalo ostatecznie, jedynie oparte o mój research w internecie, a następnie dostarczenie wiedzy, konkretnym zespołom developerskim i zaplanowanie dla nich zadań
  - **Wiki.js** — w pierwszej fazie projektu, mocno uzywane, później wyczyszczone bardzo mocno, ze względu na ryzyko, zawierania wrazliwych danych.
- **Serwisy dostępne na zewnątrz** — działające bezpośrednio w środowisku Ubuntu, dostępne w publicznym internecie z pomocą Cloudflare Tunnel:
  - **octadecimal.pro** — demo agentów pracujących w Scrum, opartych na Claude Code brak zewnętrznych uytkowników
  - **octadecimal.pl** — strona z przestarzałym portfolio firmy, z czasów vibe coding — brak zewnętrznych uytkowników
  - **octadecimal.cloud** — zaczety projekt SaaS oparty o Laravel — brak zewnętrznych uytkowników
  - **octadecimal.studio** — CMS oparty o Laravela, Filament, Tailwind — brak zewnętrznych uytkowników
- **Zespoły oparte o Claude Code**: automation, client-kamil, crisis-team, devops, frontend, innovation-lab, mobile-macos, open-team, security, system-improvements - zespoły podczas wdrazania tej inicjatywy, ich umiejętności i dane zawarte w w ich narzędziach, mogą słuzyć do czerpania wiedzy, jednak priorytetem jest, zbudowanie lepszego zespołu, na bazie najnowszych paradygmatów programowania. Podczas wdrozenia, zespoły muszą zostać nietknięte, gdyz nadal są wykorzystywane produkcyjnie.
- **Zespoły posiadają umiejętności wykorzystywania narzędzi**:  n8n, Twenty CRM, LangFuse, Grafana, Rocket.chat, Wiki.js, OVH API, Cloudflare API, Doppler (poprzedni secret menager do zastapienia przez Bitwarden)
- **Archiwum wiedzy zespołów** jest dostępne w repozytorium https://github.com/octadecimal-agents/agents-knowledge.git
- **Security** - poniewaz zespoły oparte o Claude Code, były tworzone jeszcze w czasach, gdy wiedza o bezpieczeństwie systemów multi-agents dopiero powstawała, istnieje ryzyko, ze istnieja na nim niebezpieczne pliki - mimo ciaglego nadzoru systemu. Ryzykowne jest równiez to, ze zespoły pracują bezpośrednio w systemie a nie w kontenerach.

## Konta i dostępy (CLI gotowe)

| Serwis | Stan dostępu | Charakter |
|---|---|---|
| **Bitwarden** | `bw` CLI zalogowany; primary secret + password manager | Krytyczne — jedyne źródło sekretów. |
| **GitHub** | `gh` CLI zalogowany | Główne repo home + repozytoria klienckie. |
| **OVH** | API keys dostępne | VPS, domeny, S3-compat, mail. |
| **Cloudflare** | API keys dostępne | DNS, Workers, Pages, R2, Tunnels. |

---

## Granice bezpieczeństwa

| Granica | Polityka |
|---|---|
| Sekrety → kod | Nigdy. Wyłącznie przez Bitwarden CLI w czasie wykonania. |
| Sekrety → log | Maskowane przed zapisem. |
| Repo klienckie → ten repo | Nigdy. Klient ma własne repo, agenci wchodzą tam z dedykowanymi credentials. |
| Founder data (Calendar, Mail, Notes) → cloud | Tylko za jawną zgodą foundera per integracja. |
| Kontener → host | Wąskie API (System gateway), token-bearer auth. Nigdy bezpośredni mount /Users. |
| Internet → kontener | Filtrowany. Whitelistowanie domen TBD. |
