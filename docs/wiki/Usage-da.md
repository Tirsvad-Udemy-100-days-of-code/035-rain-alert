🌐 [English](Usage) · **Dansk** · [Bahasa Melayu](Usage-ms)

# Brug

Med `.venv` aktiv og `config.env` udfyldt:

```bash
python -m rain_alert --once --dry-run
python -m rain_alert --once
python -m rain_alert
```

- `--once --dry-run` tjekker nu og skriver beskeden i stedet for at sende den. Den kræver ingen Twilio-indstillinger.
- `--once` tjekker nu og sender WhatsApp-beskeden, hvis der forventes regn. Med pywhatkit åbnes WhatsApp Web i din standardbrowser, som skal være logget ind.
- Uden valgmuligheder kører programmet hver dag på `ALERT_TIME`.

![En tørkørsel, der forventer regn](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/035-rain-alert/raw/branch/main/docs/images/dry-run-rain.png)

![En tørkørsel, der ikke forventer regn](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/035-rain-alert/raw/branch/main/docs/images/dry-run-no-rain.png)

Programmet sender én besked, når et vejrforholds-id inden for de næste 12 timer er under 700 (tordenvejr, støvregn, regn, sne), og ellers intet.

![Beskeden, som den ankommer i WhatsApp (alt andet end beskeden er sløret)](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/035-rain-alert/raw/branch/main/docs/images/whatsapp-message.png)

## Afslutningskoder

| Kode | Betydning |
| --- | --- |
| 0 | Det lykkedes |
| 1 | Vejrudsigten eller beskeden fejlede |
| 2 | En indstilling mangler eller er ugyldig (meddelelsen nævner nøglen, aldrig værdien) |

## Hvilken vejrudsigt

`FORECAST_API=onecall4` bruger One Call 4.0 time for time, som kræver det separate One Call by Call-abonnement. `FORECAST_API=forecast25` bruger den gratis 2.5-udsigt med ét punkt hver tredje time, som kurset gør.

## Hver morgen på Windows

pywhatkit skal bruge din indloggede browser, så planlæg `--once` med Windows Opgavestyring (opgaven kører, mens du er logget ind). Kommandoerne opretter den daglige opgave kl. 07:00, kører den én gang nu og fjerner den igen:

```powershell
$python = (Resolve-Path .venv\Scripts\python.exe).Path
schtasks /Create /TN "Rain Alert" /SC DAILY /ST 07:00 /IT /TR "cmd /c cd /d $PWD && $python -m rain_alert --once"
schtasks /Run /TN "Rain Alert"
schtasks /Delete /TN "Rain Alert" /F
```

## Docker Desktop (med Twilio)

En container har ingen browser, så `compose.yaml` sætter `NOTIFIER=twilio`.

```bash
docker compose up -d --build
docker compose logs -f
docker compose run --rm rain-alert python -m rain_alert --once --dry-run
docker compose down
```

![Containeren i Docker Desktop](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/035-rain-alert/raw/branch/main/docs/images/docker-container.png)

Containeren læser `config.env` ved start og tjekker vejret hver dag på `ALERT_TIME`. Den genstarter sammen med Docker Desktop.

## WhatsApp via Twilio (valgfrit)

1. Åbn Twilio Sandbox for WhatsApp i Twilio-konsollen og tilmeld dig fra din telefon.
2. Sæt konto-SID, auth-token og sandbox-nummer i `config.env`, sæt `NOTIFIER=twilio`, og dit eget nummer i `PHONENUMBER`.
3. Sandboxen glemmer din telefon efter 72 timer uden en besked; tilmeld dig igen, hvis intet ankommer.
