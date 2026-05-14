# Kanały komunikacji z founderem

| Kanał | Latency | Niezawodność | Użycie |
|---|---|---|---|
| **macOS banner** (`terminal-notifier`) | natychmiast | nisko (banner znika) | informacyjne (L2 podsumowania) |
| **macOS interactive** (`alerter`) | natychmiast | średnio (czeka na akcję, ale ginie przy reboot) | L3 wymagające szybkiej akcji |
| **E-mail** (SMTP) | minuty | wysoko | L3 z kontekstem; archiwizacja |
| **Komunikator** (TBD) | sekundy-minuty | wysoko (na telefonie) | L3 gdy founder z dala od laptopa |
| **KDE Connect "find my phone"** | natychmiast | wysoko (ignoruje silent mode) | critical alerts (zastępstwo Apple Critical Alerts, niemożliwych bez Developer Program) |

Decyzja kanału komunikatora (Telegram / Signal / Rocket.Chat) — do podjęcia w Story 002 / 003
