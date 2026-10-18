🌐 [English](Architecture) · **Dansk** · [Bahasa Melayu](Architecture-ms)

# Arkitektur

Koden er delt i lag; afhængighederne peger indad (infrastruktur til applikation til domæne). Beslutningen står i ADR-0001 (`docs/adr/`).

| Mappe | Indeholder |
| --- | --- |
| `src/rain_alert/domain/` | `HourlyForecast`, `will_rain` |
| `src/rain_alert/application/` | portene `ForecastSource` og `Notifier`, `check_rain`, `run_rain_alert` |
| `src/rain_alert/infrastructure/` | indstillinger, webadgang, OpenWeather-klienter, Twilio- og tørkørselsnotifikatorer, `DailyScheduler` |
| `src/rain_alert/constants.py` | konstanter |
| `src/rain_alert/main.py` | sammensætningsrod og kommandolinje |

## Kursets script og hvor det blev af

| Kursets script | Rain Alert |
| --- | --- |
| `weather_params` (`lat`, `lon`, `appid`, `cnt`) | `OpenWeatherClient.weather_params`, `OpenWeatherForecastClient.weather_params` |
| `requests.get(...)` | `UrllibTransport` (standardbiblioteket) |
| løkke over `weather[0]["id"] < 700` | `will_rain` i `domain/rain.py` |
| `twilio` `client.messages.create(...)` | `TwilioWhatsAppNotifier` (Twilios REST-API med `urllib`) |
| en tidsplan på PythonAnywhere eller GitHub Actions | `DailyScheduler` i Docker-containeren |
| nøgler i `os.environ.get(...)` | `Settings` læst fra `config.env` og miljøet |

## Forløb

`main()` læser indstillingerne, bygger den vejrkilde, som `FORECAST_API` angiver, og notifikatoren, og `run_rain_alert` beder kilden om de næste 12 timer. `will_rain` afgør det; hvis der forventes regn, sender notifikatoren præcis én besked.
