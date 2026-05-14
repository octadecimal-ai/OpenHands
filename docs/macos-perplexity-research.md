# Raport rozpoznawczy: System team dla macOS jako pomost dla agentów w Dockerze

_Data: 2026-05-14_

## 1. TL;DR

- **System team powinien być jednym procesem hostowym z kilkoma modułami (MCP servers + Hammerspoon + mały serwis Swift)**, a nie zbiorem luźnych binarek wywoływanych ad‑hoc.[^1][^2]
- **Powiadomienia: poziom 1 – `terminal-notifier`/AppleScript, poziom 2 – `alerter` lub nowszy CLI z reply, poziom 3 – macOS powiadomienie + „Find my phone” przez `kdeconnect-cli --ring`.**[^3][^4][^5]
- **Krytyczne Alerts (UNAuthorizationOptionCriticalAlert) są w praktyce poza zasięgiem solo‑foundera bez dedykowanego case’u i entitlements; zamiast tego użyj KDE Connect, ntfy/Pushbullet itd. jako obejście DND.**[^6][^7][^8][^9]
- **Dane systemowe, klawiatura, focus, clipboard itp. najstabilniej realizować przez Hammerspoon (daemon) z API HTTP/WebSocket dla System team; reszta to cienkie MCP‑serwery lub CLI wrappers.**[^10][^2][^1]
- **IPC między Docker a hostem: HTTP po `localhost` / `host.docker.internal` (plus ew. Unix socket) jest najczytelniejszym kompromisem między prostotą, debugowalnością i izolacją; MCP‑over‑stdio sensownie zostawić do komunikacji wewnątrz jednego host‑procesu.**[^11][^12]

## 2. Capability matrix

### 2.1 Powiadomienia i akceptacje użytkownika

| Capability | Rekomendowana ścieżka | Alternatywy | Dojrzałość / uwagi |
|-----------|-----------------------|-------------|--------------------|
| Banners (zwykłe powiadomienia) | `terminal-notifier` (Homebrew) jako prosty CLI z tytuł/tekst/URL + AppleScript przez `osascript 'display notification'` jako fallback.[^4][^13] | MCP server typu `macos-notification-mcp` lub „Notifications MCP Server” (LLM MCP) spięty z System team.[^11][^12] | `terminal-notifier` jest aktywnie utrzymywany w Homebrew, prosty, ale bez reply.[^14][^4] AppleScript via `osascript` korzysta z natywnego `UNUserNotificationCenter` pośrednio przez Script Editor; wymaga raz przyznać Notification permission dla `Script Editor`/Terminal.[^13][^15] |
| Interaktywne powiadomienia (przyciski/Reply) | `alerter` (Swift CLI) – historycznie de‑facto standard: alerty zostają na ekranie, akcje i reply są zwracane na stdout.[^3] | Nowe CLI typu „NotifiCLI” (współczesny fork z obsługą reply i przycisków) – warto rozważyć jeśli ma aktywne commity i wydania dla Apple Silicon.[^16] MCP Notifications server z obsługą buttons/reply i prostym protokołem JSON nad stdio/HTTP.[^12] | Repo `alerter` na GitHub dalej jest dostępne; nie ma częstych commitów, ale narzędzie jest samodzielne, bez sandboxu i działa na współczesnych macOS (w tym Apple Silicon przez Rosetta lub natywny build).[^3] Nowe narzędzia typu NotifiCLI są tworzone właśnie jako bardziej utrzymywalne zamienniki terminal-notifier/alerter (obsługa reply na STDOUT, persistent alerts).[^16] |
| Critical alerts (bypass DND) | Brak realistycznej ścieżki „czysto lokalnej” – `UNAuthorizationOptions.criticalAlert` wymaga entitlements `com.apple.developer.usernotifications.critical-alerts` wydawanych selektywnie po review Apple.[^9][^17][^7] | Hack: dwustopniowe żądanie uprawnień i prowadzenie użytkownika do ręcznego włączenia Critical Alerts w ustawieniach, jak opisano w blogu (dalej wymaga entitlementu na poziomie kodu, więc nie działa w pełni dla zwykłych deweloperów).[^6] Obejścia: KDE Connect `--ring` do telefonu (ignoruje tryb cichy na Androidzie), web‑push ntfy/Pushbullet, osobna aplikacja z Time Sensitive Notifications (łatwiejsze niż Critical Alerts) itp.[^8][^18][^5] | Apple wyraźnie dokumentuje, że Critical Alerts wymagają specjalnego entitlementu; dyskusje w HN/issue trackerach ntfy potwierdzają, że bez tego uprawnienia nie da się legalnie omijać DND.[^9][^8][^7] Dla solo‑foundera bez „public safety/health” use‑case’u jest to praktycznie niedostępne. |
| Trwałość przy sleep/wake | Zostawić scheduling / retry po stronie System team (daemon) – powiadomienie wysyłane po wybudzeniu, z rejestracją „pending questions” w lokalnej kolejce (np. SQLite/plik JSON). | Wykorzystanie `UNUserNotificationCenter` z triggerami czasowymi/kalendarzowymi; wymaga natywnej appki z background delivery i ewentualnie launchd agent do utrzymania procesu.[^19] | Samo powiadomienie lokalne nie „przetrwa” zamknięcia pokrywy, jeśli zostało wysłane gdy system zasypiał; potrzebna jest warstwa retry w logice System team i zdarzenia wake (Hammerspoon `hs.caffeinate.watcher`).[^2] |
| Omijanie DND dla krytycznych powiadomień | Brak bezpośredniego rozwiązania, patrz Critical Alerts. Rekomendacja: poziom 3 = powiadomienie + KDE Connect `--ring` + ew. dodatkowy kanał (e‑mail/SMS/ntfy) jeśli laptop śpi. | Możliwe wykorzystanie Time Sensitive Notifications (iOS/macOS Focus) w osobnej appce, ale to wymaga App Store i review; nadal nie jest to pełny Critical Alert.[^19][^8] | Strategicznym obejściem jest przerzucenie „głośnego” alertu na urządzenie mobilne, które ma własne reguły DND, np. telefon z Androidem sterowany przez KDE Connect.[^20][^18] |

### 2.2 Integracja z natywnymi aplikacjami (Calendar, Mail, Notes, Contacts, Reminders, Shortcuts)

| Capability | Rekomendowana ścieżka | Alternatywy | Dojrzałość / uwagi |
|-----------|-----------------------|-------------|--------------------|
| Calendar – read/write | AppleScript/JXA lub Shortcuts z akcjami Calendar wywoływanymi przez `shortcuts run` z System team.[^21][^22] | Natywna appka w Swift z `EventKit` używana jako backend (MCP server) – większa inwestycja, ale lepsze typowanie i performance.[^19] | AppleScript dla Calendar ma wieloletnie API i dużo przykładów (tworzenie eventów z Mail, Reminders itd.).[^23] AppleScript jako technologia jest „w stagnacji”, ale wciąż szeroko stosowana i wspierana przez OS.[^24][^25] |
| Mail – read/search/draft/send | AppleScript do Mail (pobranie zaznaczonej wiadomości, tworzenie drafta, wysyłka).[^23] | IMAP/SMTP bezpośrednio z platformy backendowej (np. Python/Go) – wymaga konfiguracji kont, ale uniezależnia się od Apple Mail. | Automatyzacja Mail przez AppleScript jest powszechnie stosowana (np. skrypty tworzące Calendar events z e‑maili).[^23] Należy brać pod uwagę TCC dla Mail (Automation + Full Disk jeśli dotykamy załączników). |
| Notes – read/write | Shortcuts z akcjami Notes (create/find note) wywoływane z CLI, plus AppleScript gdzie dostępne.[^22][^21] | Dedykowana appka w Swift z `Notes` frameworks (brak publicznego pełnego API; w praktyce wiele osób używa Automation/AppleScript/Shortcuts). | Shortcuts jest „oficjalną” drogą automatyzacji dla Notes, choć społeczność narzeka na luki i bugi („automation gap”).[^26][^22] |
| Contacts – lookup | AppleScript do Contacts / `contacts` CLI (gdzie dostępny), lub Shortcuts z akcją „Find Contacts”.[^22] | Bezpośredni dostęp do CardDAV/LDAP, jeśli kontakty są synchronizowane z zewnętrznymi usługami. | Apple nie rozwija intensywnie AppleScript, ale Contacts ma stabilne słowniki AppleScript.[^24][^25] |
| Reminders – create/list | Shortcuts akcje „Add New Reminder”, „Find Reminders” wywoływane z CLI; Reminders są ściśle powiązane z Calendar/Notes.[^21][^27] | AppleScript dla Reminders (bardziej ograniczony niż Calendar). | Shortcuts jest głównym narzędziem automatyzacji Reminders, sporo tutoriali opisuje np. generowanie reminders z Notes/Calendar.[^27][^28] |
| Shortcuts – invoke | `shortcuts run "Name" --input ...` z System team; może być opakowane jako MCP server/CLI tool.[^22] | Hammerspoon oferuje wywoływanie shell scripts, więc może agregować Shortcuts wywoływane z CLI; można też zbudować natywny launcher w Swift z UI. | Shortcuts jest wspierane na macOS, choć nadal są znane ograniczenia (np. brak w pełni bezobsługowych automations na Mac w porównaniu z iOS, niektóre workflow wymagają interakcji).[^29][^26] |
| Shortcuts – bycie wywołanym | Utworzyć Shortcuts, który jako akcję ma wywołanie HTTP/Webhook do System team (np. `curl localhost:port/...`) lub odpalenie skryptu shell, który gada z System team.[^22][^21] | MCP server przyczepiony do jakiejś aplikacji MCP‑aware (np. LLM/VSCode), ale to obok głównego systemu. | Shortcuts ma akcję „Run Shell Script” oraz integrację z URL Schemes, więc łatwo spiąć z lokalnym HTTP endpointem System team.[^22] |

### 2.3 System / process metrics

| Capability | Rekomendowana ścieżka | Alternatywy | Uwagi |
|-----------|-----------------------|-------------|-------|
| CPU/memory/energy/network per process (Activity Monitor‑like) | `ps`, `top`, `powermetrics` i `nettop` zebrane w Hammerspoon/Swift daemon i wystawione przez API.[^30][^31] | `iostat`, `vm_stat`, `sysctl` dla bardziej surowych danych; istnieją biblioteki Swift/Go korzystające z IOKit i innych frameworków. | Activity Monitor sam korzysta z standardowych frameworków; Apple dokumentuje koncepcje (CPU System/User/Idle, Memory Pressure) ale nie wystawia „jednego” CLI.[^30][^31] Hammerspoon ma moduły do odczytu baterii, CPU, sieci, ale nie pełny klon Activity Monitor; można go połączyć z zewnętrznymi CLI.[^2][^1] |
| Battery status, thermal pressure | Hammerspoon: `hs.battery` (poziom baterii, cykle, stan ładowania) oraz `hs.host.thermalState`/powiązane API, gdzie dostępne.[^2][^1] | Natywna appka w Swift używająca IOKit/`NSProcessInfo.thermalState`. | Hammerspoon deklaruje dostęp do baterii i hardware info (ekstensje host, battery), co jest wygodne z Lua i nie wymaga budowy własnego wrappera Swift.[^2][^10] |
| Wolne miejsce na dysku | Zwykłe `df -h` / `stat` wywołane z System team lub Hammerspoon (`hs.fs`), plus ewentualne API Swift (`URLResourceValues.volumeAvailableCapacityForImportantUsage`). | – | To wymaga tylko Full Disk Access, jeśli chcesz widzieć niektóre pathy/volumes; inaczej TCC może ograniczyć widoczność z poziomu procesu bez FDA.[^32][^33] |

### 2.4 Cross‑device (KDE Connect)

| Capability | Rekomendowana ścieżka | Uwagi |
|-----------|-----------------------|-------|
| Połączenie z Android (powiadomienia, pliki, clipboard) | `kdeconnect-cli` jako główny interfejs, wywoływany z System team/Hammerspoon: wysyłanie plików, clipboard sync, komendy custom.[^20][^34] | KDE Connect dla macOS oferuje podobne funkcje jak na Linux – przesył plików, powiadomienia, sterowanie mediami itp.[^34][^20] |
| „Find my phone” / bypass silent | `kdeconnect-cli -d <deviceId> --ring` lub `kdeconnect-cli -n <deviceName> --ring`.[^5][^18] | Idealny jako poziom 3 w eskalacji powiadomień – telefon dzwoni niezależnie od DND macOS. |

### 2.5 Secrets – Bitwarden CLI

| Capability | Rekomendowana ścieżka | Uwagi |
|-----------|-----------------------|-------|
| Dostęp do haseł / API keys | `bw` CLI instalowane z Homebrew, logowanie `bw login`, odblokowanie sejfu i przechowywanie `BW_SESSION` jako env w System team; pobieranie secrets przez `bw get item`/`bw list items`.[^35][^36][^37] | CLI jest pełnoprawne, wspierane przez oficjalną dokumentację Bitwarden (help center, GitHub).[^35][^38] Należy zadbać o to, aby System team nie logował wrażliwych danych. |

### 2.6 Inne: clipboard, focus, input

| Capability | Rekomendowana ścieżka | Uwagi |
|-----------|-----------------------|-------|
| Clipboard read/write | Hammerspoon `hs.pasteboard` lub prosty Swift helper z `NSPasteboard`; Hammerspoon jest szybszy do wdrożenia.[^2][^1] | Wymaga Accessibility/Automation w TCC jeśli automatyzacja wkleja tekst do okien innych aplikacji. |
| Window/app focus state, „czy użytkownik właśnie pisze” | Hammerspoon: `hs.window`, `hs.application`, `hs.eventtap` (monitor klawiatury, focus aplikacji, aktywne okno).[^2][^1][^39] | Hammerspoon jest de facto standardem dla tego typu automatyzacji – ma dostęp do Accessibility API i reaguje na eventy bez polling.[^10][^1] |

## 3. Rekomendowana architektura System team

### 3.1 Jeden proces hostowy, modułowy wewnętrznie

Architektura powinna opierać się o **jeden główny proces System team (daemon)** uruchamiany przez `launchd` przy logowaniu użytkownika i utrzymujący długotrwałe połączenia/IPCs. Wewnątrz:[^2][^39]

- Moduł „Orchestrator” – przyjmuje żądania z agentów w Dockerze (HTTP/MCP), decyduje o typie interakcji (powiadomienie, akcja kalendarza, dostęp do secrets itd.).
- Moduł Hammerspoon – Hammerspoon działa jako osobny daemon (jak zwykle) z plikiem `init.lua`, wystawia HTTP/WebSocket (np. przez `hs.http.server`) lub prosty protokół lokalny; System team komunikuje się z nim po lokalnym porcie. Hammerspoon odpowiada za: focus, clipboard, key events, część powiadomień, odczyt hardware.[^1][^2]
- Moduły MCP servers (osobne procesy/komendy) dla powiadomień, system metrics, integracji z natywnymi aplikacjami – uruchamiane z System team lub hostowane w nim w zależności od implementacji.[^12][^11]
- Adaptery CLI (kdeconnect-cli, bw, terminal-notifier, alerter, shortcuts run), wywoływane synchronicznie lub asynchronicznie z kolejką zadań.

Z punktu widzenia Octadecimal to jeden „System team endpoint” dla agentów, z wewnętrznym routingiem do poszczególnych capabilities.

### 3.2 Dlaczego nie „każda capability = osobny daemon”?

- TCC i permissions (Full Disk Access, Automation, Accessibility, Notifications) przyznaje się per‑app/binary. Jeśli capabilities rozproszyć na wiele binarek, trzeba klikać wielokrotnie lub używać MDM/PPPC do ich ustawiania.[^32][^33]
- Jeden podpisany binarny (np. główna appka Swift bądź uniwersalny launcher Hammerspoon + mały helper) upraszcza FDA i Automation.[^33]
- Debugowanie IPC jest prostsze: logi z jednego serwisu, jedna konfiguracja portów/sockets.

### 3.3 Rola Hammerspoon

Hammerspoon jest naturalnym kandydatem na **„automation runtime”**:

- Jest demonem z event‑driven architekturą, startuje przy logowaniu użytkownika i reaguje na zdarzenia systemowe (Wi‑Fi, sleep/wake, USB, klawiatura).[^40][^2]
- Ma głęboki dostęp do macOS APIs: okna, aplikacje, klawiatura, mysz, baterie, dostępność, clipboard.[^10][^2]
- Wymaga jednorazowego przyznania Accessibility/Automation (i ewentualnie FDA dla niektórych akcji).[^2][^10]

Rekomendacja: **Hammerspoon jako wewnętrzny „agent lokalny”**, a System team jako gateway dla agentów AI. System team może do części zadań w ogóle nie dotykać Hammerspoon (np. powiadomienia przez CLI), ale dla bardziej zaawansowanej automatyzacji używa jego API.

### 3.4 Natywny komponent Swift/Obj‑C

Dla funkcji, których nie da się wiarygodnie osiągnąć przez CLI/AppleScript (zaawansowane powiadomienia, background `UNUserNotificationCenter`, lepsza integracja z TCC), warto mieć **mały helper w Swift**:

- Rejestracja `UNUserNotificationCenter` delegate w aplikacji bez UI (agent) dla lepszej obsługi interaktywnych powiadomień, kategorii, akcji.[^19][^41]
- Możliwość budowy menu bar app / login item, który zapewnia stabilne istnienie procesu (ważne dla sleep/wake, Focus state itd.).
- Potencjalnie – repo MCP server (np. notifications MCP) skompilowane jako część tej aplikacji.[^42][^11]

To wymaga jednak Xcode, podpisywania kodu i ewentualnie Developer ID.

## 4. IPC: jak Docker gada z hostem

### 4.1 Kandydaci

- **HTTP over localhost (`127.0.0.1`)** – najprostsze: System team wystawia port (np. 127.0.0.1:8765), kontenery łączą się po `host.docker.internal` (Docker Desktop na macOS) lub `--add-host`.[^11][^12]
- **Unix socket** – `/tmp/system-team.sock` montowane do kontenerów jako volume. Wymaga klienta HTTP/gRPC potrafiącego użyć Unix sockets.
- **MCP over stdio** – jeśli agenci to procesy uruchamiane bezpośrednio (nie w Dockerze), MCP z naturalnym stdio jest wygodny; w Dockerze też możliwy, ale mniej naturalny przy wielu kontenerach.[^12][^11]

### 4.2 Rekomendacja

Dla multi‑container, multi‑agent setupu **HTTP/gRPC over localhost + `host.docker.internal`** jest najbardziej pragmatyczne:

- Każdy język programowania ma proste biblioteki HTTP; debugowanie przez curl/browsers/mitmproxy jest trywialne.
- Docker Desktop zapewnia `host.docker.internal` jako alias hosta dla kontenera.[^11]
- Można dodać prostą autoryzację (token per agent, mTLS w przyszłości) bez wiązania się z konkretnym runtime.

Unix socket jest dobrą opcją, jeśli chcesz ograniczyć powierzchnię ataku do procesów, które mają zamontowany socket oraz odrobinę lepszy performance. Można rozważyć: **System team nasłuchuje na Unix socket, a prosty sidecar (np. Nginx/Envoy) robi HTTP‑to‑Unix bridging**.

MCP over stdio jest idealne **wewnątrz jednego procesu/hosta** – np. System team może mówić MCP do swoich wewnętrznych serwerów (notifications MCP, macos‑notification‑mcp itd.), ale komunikacja Docker↔host jest lepiej obsłużona przez HTTP.

## 5. One‑time setup checklist (TCC, launchd, etc.)

### 5.1 Uprawnienia TCC

Dla głównej aplikacji System team (i Hammerspoon, jeśli osobno):

- **Full Disk Access** (jeśli agenci mają oglądać cały filesystem, logi, zewnętrzne dyski) – System Settings → Privacy & Security → Full Disk Access, ręczne dodanie appki/Hammerspoon.[^32][^33]
- **Automation** – pozwolenie na sterowanie innymi aplikacjami (Mail, Calendar, Notes, Reminders, Shortcuts, Script Editor, Terminal).[^32]
- **Accessibility** – niezbędne dla Hammerspoon (eventtap, manipulacja oknami, wklejanie tekstu).[^10][^2]
- **Notifications** – dla Terminal/Script Editor (jeśli używany `osascript`), dla natywnej appki Swift oraz Hammerspoon jeśli wysyła powiadomienia.[^15][^13]
- **Files & Folders / Removable Volumes** – jeśli System team ma czytać np. zewnętrzne dyski / Desktop/Downloads bez promptów.[^33]

W praktyce macOS zapisuje te decyzje w bazie TCC per użytkownik; manualne modyfikowanie TCC.db jest możliwe, ale niezalecane bez MDM.[^43][^32]

### 5.2 Scriptability / Automation setup

- Zainstalować Hammerspoon (np. przez Homebrew), uruchomić, przyznać Accessibility.[^1][^2]
- Skonfigurować `~/.hammerspoon/init.lua` tak, aby:
  - startował lokalny serwer HTTP/WebSocket,
  - udostępniał API do clipboard, focus, powiadomień, metryk systemowych.
- Dodać System team jako **Login Item** (menu: Users & Groups → Login Items) lub skonfigurować `launchd` plist w `~/Library/LaunchAgents` dla automatycznego startu.[^39]
- Dla `osascript` powiadomień – raz wywołać prosty skrypt, aby macOS zapytał o powiadomienia dla Script Editor/Terminal.[^13][^15]

### 5.3 Docker / IPC

- Upewnić się, że Docker Desktop używa domyślnego `host.docker.internal` (na macOS jest wspierane out‑of‑the‑box).[^11]
- Ewentualnie otworzyć wybrany port na `127.0.0.1` i skonfigurować System team, by tam nasłuchiwał.
- Przy wielu agentach: wprowadzić identyfikator agenta w nagłówkach HTTP lub ścieżkach (np. `/agent/<id>/notify`).

## 6. Stos powiadomień – 3‑poziomowa eskalacja

### 6.1 Poziom 1 – zwykły banner

Cel: lekkie powiadomienie, które można łatwo przefiltrować.

- Narzędzie: `terminal-notifier` wywoływany przez System team (np. `terminal-notifier -title 'Agent' -message 'Job finished'`).[^4][^14]
- Alternatywa/backup: `osascript -e 'display notification "msg" with title "Title"'` – wymaga uprzedniego nadania powiadomień dla Script Editor/Terminal.[^15][^13]
- Integracja z MCP: można wykorzystać istniejące `macos-notification-mcp` lub ogólny Notifications MCP server, który mówi z `UNUserNotificationCenter` i wystawia prosty schema.[^12][^11]

### 6.2 Poziom 2 – interaktywne powiadomienie (przyciski/reply)

Cel: wymuszenie reakcji (Approve/Deny, krótka odpowiedź tekstowa) z minimalnym friction.

- Narzędzie: `alerter` lub nowsze CLI (np. NotifiCLI) obsługujące **Reply Input** i **Action Buttons**; zwracają wynik na stdout, więc System team może zablokować workflow do momentu odpowiedzi.[^16][^3]
- Konfiguracja: predefiniowane kategorie – np. „approval_required”, „user_input”, z mapowaniem na JSON payload dla agentów.
- Natywny fallback: mały Swift helper z `UNUserNotificationCenter` i `UNNotificationAction`, jeśli CLI okażą się nietrwałe na przyszłych wersjach macOS.[^41][^19]

### 6.3 Poziom 3 – „głośne” alerty

Cel: dotarcie do użytkownika mimo DND i mimo tego, że Mac może być w trybie uśpienia.

- Składnik 1: lokalne powiadomienie na macOS (baner lub alert) tak jak wyżej – dla historii/humans, gdy użytkownik wraca do komputera.[^19]
- Składnik 2: `kdeconnect-cli --ring -n "PHONE_NAME"` aby wymusić dzwonienie telefonu.[^18][^5]
- Składnik 3 (opcjonalny): wysłanie wiadomości przez kanał push (ntfy.sh, Matrix, Signal API via osobny bot) – do rozważenia jako kolejny „layer”, ale poza zakresem stricte macOS.

W ten sposób unika się wchodzenia w sporne rejony Critical Alerts w ekosystemie Apple, jednocześnie osiągając efekt, że **krytyczny alert budzi telefon**.

## 7. Otwartych pytań i czerwone flagi

### 7.1 Utrzymanie narzędzi CLI (alerter, terminal-notifier, NotifiCLI)

- `terminal-notifier` jest wciąż w Homebrew i używany w bieżących poradnikach (np. 2025 artykuły o powiadomieniach po SSH), więc można go uznać za względnie „żywy”.[^14][^4]
- `alerter` ma rzadkie aktualizacje; może być konieczne utrzymanie własnego forka lub zbudowanie prostego Swift CLI, jeśli Apple zmieni API powiadomień w macOS 15/16.[^3]
- Pojawiają się nowe narzędzia (np. NotifiCLI) ze wsparciem reply/buttons, ale trzeba ocenić ich community/utrzymanie na GitHub/Reddit.[^16]

### 7.2 AppleScript / JXA przyszłość

- AppleScript nie jest aktywnie rozwijany, ale Apple nie usunęło go z macOS; społeczność i vendorzy (DEVONthink, OmniGroup) nadal używają AppleScript/JXA.[^24][^25][^22]
- Apple przesuwa ciężar na Shortcuts, ale Shortcuts cierpi na „automation gap” – nie pokrywa wszystkich przypadków użycia, zwłaszcza na macOS.[^26][^29]
- Długoterminowo: warstwa automatyzacji powinna być z czasem przenoszona do Swift/SwiftData/`UNUserNotificationCenter`, a AppleScript traktowany jako „most” tam, gdzie inaczej się nie da.

### 7.3 macOS 15+ zmiany w automatyzacji/TCC

- macOS Sequoia (15) wprowadził zmiany w przechowywaniu konfiguracji dla niektórych elementów dostępności (np. VoiceOver AppleScript), przenosząc pliki z klasycznych `~/Library/Preferences` do sandboxed Group Containers. To sugeruje, że Apple dalej „uszczelnia” warstwy automatyzacji.[^44]
- Zgłoszenia z 2024–2025 pokazują, że Full Disk Access potrafi być „resetowany” po aktualizacji binarki; Apple wymaga odpowiednich entitlements (`com.apple.security.files.all`) by FDA trzymało się na poziomie team ID zamiast konkretnej wersji.[^45][^46]
- W praktyce dla solo‑foundera bez MDM oznacza to, że **aktualizacje przez Homebrew mogą powodować utratę FDA**, jeśli binarka nie jest odpowiednio podpisana – dlatego warto ograniczyć liczbę kluczowych binarek i rozważyć ręczne zarządzanie aktualizacjami.[^45]

### 7.4 Sleep/wake i launchd

- Hammerspoon i ewentualny Swift helper jako login items + launchd agents zapewniają, że System team działa tylko w sesji użytkownika – to ważne, bo TCC/Automation są per user.[^39][^2]
- Sleep/wake eventy można łapać w Hammerspoon (`hs.caffeinate.watcher`) i/lub w natywnym kodzie, żeby:
  - wznawiać nasłuchiwanie IPC,
  - przeliczać timeouty pytań do użytkownika,
  - ponownie wysyłać powiadomienia, które „wypadły” podczas snu.

### 7.5 Multi‑Mac story

- Architektura „System team jako lokalny daemon HTTP + Hammerspoon + CLI helpers” skaluje się liniowo na kolejne Maci – każdy Mac ma własny System team z tym samym API.[^40][^2]
- Agenci w Dockerze powinni być projektowani tak, aby akceptowali endpoint System team przez konfigurację (URL hosta), co ułatwia przełączanie między MacBook a Mac Studio.
- Można dodać warstwę discovery (np. mały serwis w chmurze lub Tailscale/IP‑based routing), ale to poza zakresem lokalnego macOS automation.

***

_Dokument przygotowany z myślą o jednoosobowym software house Octadecimal, z naciskiem na realistyczne, utrzymywalne ścieżki implementacyjne bez ciężkiej infrastruktury MDM/App Store._

---

## References

1. [Hammerspoon: The macOS Automation Powerhouse You're Not ...](https://dev.to/benriemer/hammerspoon-the-macos-automation-powerhouse-youre-not-using-but-should-be-45a6) - This open-source tool bridges Lua scripting with macOS system-level operations, giving developers un...

2. [Hammerspoon](https://www.hammerspoon.org) - This is a tool for powerful automation of macOS. At its core, Hammerspoon is just a bridge between t...

3. [vjeantet/alerter: Send User Alert Notification on MacOS ... - GitHub](https://github.com/vjeantet/alerter) - Alerter is a command-line tool for sending macOS notifications (alerts), built with Swift and Swift ...

4. [How to Get macOS Notifications for Long-Running Processes (Even ...](https://dev.to/jfpio/how-to-get-macos-notifications-for-long-running-processes-even-over-ssh-154d) - 1. Meet terminal-notifier. terminal-notifier is a command-line utility that lets you create macOS no...

5. [what is the terminal command to ring my phone with KDE Connect?](https://www.reddit.com/r/kde/comments/93nan1/what_is_the_terminal_command_to_ring_my_phone/) - Something useful is to use the -n argument instead of -d, so you don't have to look-up the device id...

6. [Get Critical Alert Permission from User instead of Apple - 肇鑫的技术 ...](https://zhaoxin.pro/technology/16703819971617.html) - However, to get the entitlement of critical alert, you have to ask Apple to give your permission. So...

7. [I can't understand Apple's Critical Alert policy (2023) - Hacker News](https://news.ycombinator.com/item?id=43922698) - The appeals process does not apply to Critical Alert Entitlement requests, which must be submitted t...

8. [iOS: Enable critical alerts · Issue #1235 · binwiederhier/ntfy - GitHub](https://github.com/binwiederhier/ntfy/issues/1235) - Apple states: "Critical alerts require a special entitlement issued by Apple." https://developer.app...

9. [UNAuthorizationOptionCriticalAlert | Apple Developer Documentation](https://developer.apple.com/documentation/usernotifications/unauthorizationoptions/criticalalert?language=objc) - You can specify a custom sound and volume. Critical alerts require a special entitlement issued by A...

10. [Hammerspoon Is Powerful Free Automation Tool for macOS - LifeTips](https://lifetips.alibaba.com/tech-efficiency/hammerspoon-is-powerful-free-automation-tool-for-os-x) - Hammerspoon is a powerful free automation tool for macOS that cuts repetitive task time by 40–75% an...

11. [devizor/macOS-Notification-MCP - GitHub](https://github.com/devizor/macos-notification-mcp) - macOS Notification MCP enables AI assistants to trigger native macOS sounds, visual notifications, a...

12. [Notifications - Awesome MCP Servers](https://mcpservers.org/servers/ohqay/notifications) - Notifications MCP Server. An MCP server that enables AI assistants like LLM to send native macOS ...

13. [Trigger customized Notifications from the macOS Terminal and Scripts](https://swissmacuser.ch/native-macos-notifications-from-terminal-scripts/) - A hidden AppleScript command line program allows you to to show individual Notifications.

14. [terminal-notifier - Homebrew Formulae](https://formulae.brew.sh/formula/terminal-notifier) - Send macOS User Notifications from the command-line. https://github.com/julienXX/terminal-notifier. ...

15. [Trying to use Terminal for Display Notification - MacScripter](https://www.macscripter.net/t/trying-to-use-terminal-for-display-notification/76593) - The solution supplied by Dirk in the OP's Late Night Software thread is to enable notification permi...

16. [I built a CLI for macOS notifications that actually supports replies and ...](https://www.reddit.com/r/macapps/comments/1qdjirt/i_built_a_cli_for_macos_notifications_that/) - I built a CLI for macOS notifications that actually supports replies and persistent alerts ... I've ...

17. [Swift Local Notifications in Do Not Disturb - Stack Overflow](https://stackoverflow.com/questions/76850471/swift-local-notifications-in-do-not-disturb) - ... Critical Alerts" Entitlement. Entitlement: com.apple.developer.usernotifications.critical-alerts...

18. [KDE Connect: how to run: Ring-my-phone from the command line](https://discuss.kde.org/t/kde-connect-how-to-run-ring-my-phone-from-the-command-line/6036) - If from command line you could run “kdeconnect-cli --ring --name “[device_name]””, provided they're ...

19. [User notifications on iOS, tvOS, macOS and Mac Catalyst - .NET for ...](https://learn.microsoft.com/en-us/dotnet/ios/app-fundamentals/user-notifications) - This article describes the User Notifications framework. It discusses local notifications, remote no...

20. [KDE Connect Guided Solution - Kubuntu Focus](https://kfocus.org/wf/kde-connect.html) - Find your phone by ringing it from your computer; Send shell commands to your computer from your mob...

21. [Be productive with Calendar, Notes, Reminders, and ...](https://support.apple.com/guide/mac-pro/be-productive-apd99814260c/mac) - Learn how to use Calendar, Notes, Reminders, and Shortcuts on your Mac to increase productivity.

22. [Beyond AppleScript - Automation - DEVONtechnologies Community](https://discourse.devontechnologies.com/t/beyond-applescript/77909) - It makes code faster to execute, because the JSContext is part of the application itself (OmniGraffl...

23. [Email to Calendar Event - Cool Workflows - MPU Talk](https://talk.macpowerusers.com/t/email-to-calendar-event/20124) - This Applescript will create a Calendar Event for the selected Mail item with a link back to the ema...

24. [Seeking Alternative to AppleScript for Automation Tasks](https://discussions.apple.com/thread/256081580) - Apple is moving away from Automator to its Shortcuts solution. Apple's Foundation Framework includes...

25. [I've long been worried that Apple will drop support for AppleScript ...](https://www.dzombak.com/blog/2025/07/ive-lobeen-worried-that-apple-will-drop-support-for-applescript-automation-in-macos-updates-or-at-least-allow-it-to-decay-into-a-horrible-broken-state/) - I've long been worried that Apple will drop support for AppleScript automation in macOS updates, or ...

26. [Shortcuts is falling into “the automation gap” - Six Colors](https://sixcolors.com/link/2025/03/shortcuts-is-falling-into-the-automation-gap/) - If Shortcuts is to become the default way to automate tasks on the Mac, there needs to be steady, ye...

27. [Notes straight to calendar events & Reminders! A ...](https://www.youtube.com/watch?v=N2t_jSCYfYY) - Purpose of this video: Apple Shortcuts tutorial and demo showing how to Make a Calendar event or a r...

28. [My Productivity Workflow 2025: Task Management + Apple ...](https://www.youtube.com/watch?v=DCecVFgTl14) - My Productivity Workflow 2025: Task Management + Apple Shortcuts + Gmail Chrome Extension w/NotePlan...

29. [Is it really true that Mac OS doesn't support automations in ... - Reddit](https://www.reddit.com/r/shortcuts/comments/1kf7nw7/is_it_really_true_that_mac_os_doesnt_support/) - There is a separate macOS app named Automator that can be used to run a shortcut as an SSH command, ...

30. [View CPU activity in Activity Monitor on Mac - Apple Support](https://support.apple.com/guide/activity-monitor/view-cpu-activity-actmntr43452/mac) - In Activity Monitor, view the processor activity of your Mac over time, including current and recent...

31. [Mac Activity Monitor Complete Guide 2025: CPU, Memory, Energy ...](https://macos-tahoe.com/blog/mac-activity-monitor-complete-guide-2025/) - Master Activity Monitor on macOS Tahoe. Learn to diagnose CPU issues, understand memory pressure, id...

32. [Ask the Mac Guy: What's the Deal with Full Disk Access for Mac?](https://www.huntress.com/blog/ask-the-mac-guy-whats-the-deal-with-full-disk-access) - Learn about the importance of Full Disk Access for Mac, its role in macOS security, and how it affec...

33. [How to toggle removable and full disk access for apps in macOS ...](https://forums.appleinsider.com/discussion/237963/how-to-toggle-removable-and-full-disk-access-for-apps-in-macos-sequoia) - System Settings->Privacy & Security->Full Disk Access allows you to set which apps should be allowed...

34. [KDE Connect For Mac - Sync Android On Mac - YouTube](https://www.youtube.com/watch?v=U1G-F1qwBss) - Now Upload and Download Files like Airdrop For Android, Receive Phone Calls, Notifications, Remote C...

35. [bitwarden/cli: The command line vault (Windows, macOS, & Linux).](https://github.com/bitwarden/cli) - The Bitwarden CLI is a powerful, full-featured command-line interface (CLI) tool to access and manag...

36. [How to install and use the Bitwarden command line tool](https://bitwarden.com/blog/how-to-install-and-use-the-bitwarden-command-line-tool/) - The command-line version of Bitwarden can be installed on Linux, macOS, and Windows by way of either...

37. [Bitwarden CLI | λ ryan.himmelwright.net](https://ryan.himmelwright.net/post/bitwarden-cli/) - The bw list command is used to list out contents from the password vault. This requires an object to...

38. [Password Manager CLI - Bitwarden](https://bitwarden.com/help/cli/) - The Bitwarden command-line interface (CLI) is a powerful, fully-featured tool for accessing and mana...

39. [Automation and GUI Scripting with Hammerspoon (macOS) - YouTube](https://www.youtube.com/watch?v=PJh3J9MaDUM) - Hammerspoon reminds me of Keyboard Maestro, it provides a daemon to execute actions for custom keybo...

40. [Powerful macOS Automation Tool Gains New Features - UBOS.tech](https://ubos.tech/news/hammerspoon-powerful-macos-automation-tool-gains-new-features/) - Hammerspoon is an open‑source macOS automation framework that lets power users script and control vi...

41. [UNUserNotificationCenter | Apple Developer Documentation](https://developer.apple.com/documentation/usernotifications/unusernotificationcenter) - Overview. Use the shared UNUserNotificationCenter object to manage all notification-related behavior...

42. [macOS Notifier MCP Server by Michael Darmousseh - PulseMCP](https://www.pulsemcp.com/servers/turlockmike-macos-notifier) - MCP (Model Context Protocol) Server. Enables interaction with macOS notifications and system dialogs...

43. [Anyone else seeing Full Disk Access suddenly disabled on macOS ...](https://www.reddit.com/r/macsysadmin/comments/1mwik4o/anyone_else_seeing_full_disk_access_suddenly/) - As others have said, this is a known UI bug. Final word on which permissions which app has are down ...

44. [MacOS Sequoia support for VoiceOver AppleScript automation](https://github.com/actions/runner-images/issues/11257) - Description. In MacOS Sequoia (15) Apple have changed where configuration is stored for enabling App...

45. [Full Disk Access revoked on every Homebrew update — binary ...](https://github.com/llm-providers/llm-code/issues/55661) - Summary Every time automation assistant updates via brew upgrade, macOS revokes Full Disk Access (FDA) becaus...

46. [MacOS Ventura Full-Disk Access Bug Fix - Automox](https://www.automox.com/blog/ventura-full-disk-fix) - It's meant to address a specific bug with MacOS Ventura where apps don't have Full Disk Access permi...

