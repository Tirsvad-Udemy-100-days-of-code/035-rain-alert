🌐 [English](Usage) · **Dansk** · [Bahasa Melayu](Usage-ms)

# Brug

Med `.venv` aktiv og `config.env` udfyldt:

```bash
python -m rain_alert --once --dry-run
python -m rain_alert --once
python -m rain_alert
```

- `--once --dry-run` tjekker nu og skriver beskeden i stedet for at sende den. Den kræver ingen Twilio-indstillinger.
- `--once` tjekker nu og sender WhatsApp-beskeden, hvis der forventes regn.
- Uden valgmuligheder kører programmet hver dag på `ALERT_TIME`.

![En tørkørsel, der forventer regn](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/035-rain-alert/raw/branch/main/docs/images/dry-run-rain.png)

![En tørkørsel, der ikke forventer regn](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/035-rain-alert/raw/branch/main/docs/images/dry-run-no-rain.png)

Programmet sender én besked, når et vejrforholds-id inden for de næste 12 timer er under 700 (tordenvejr, støvregn, regn, sne), og ellers intet.

## Afslutningskoder

| Kode | Betydning |
| --- | --- |
| 0 | Det lykkedes |
| 1 | Vejrudsigten eller beskeden fejlede |
| 2 | En indstilling mangler eller er ugyldig (meddelelsen nævner nøglen, aldrig værdien) |

## Hvilken vejrudsigt

`FORECAST_API=onecall4` bruger One Call 4.0 time for time, som kræver det separate One Call by Call-abonnement. `FORECAST_API=forecast25` bruger den gratis 2.5-udsigt med ét punkt hver tredje time, som kurset gør.

## Docker Desktop

```bash
docker compose up -d --build
docker compose logs -f
docker compose run --rm rain-alert python -m rain_alert --once --dry-run
docker compose down
```

![Containeren i Docker Desktop](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/035-rain-alert/raw/branch/main/docs/images/docker-container.png)

Containeren læser `config.env` ved start og tjekker vejret hver dag på `ALERT_TIME`. Den genstarter sammen med Docker Desktop.

## WhatsApp via Twilio

1. Åbn Twilio Sandbox for WhatsApp i Twilio-konsollen og tilmeld dig fra din telefon.
2. Sæt konto-SID, auth-token og sandbox-nummer i `config.env`, og dit eget nummer i `PHONENUMBER`.
3. Sandboxen glemmer din telefon efter 72 timer uden en besked; tilmeld dig igen, hvis intet ankommer.
