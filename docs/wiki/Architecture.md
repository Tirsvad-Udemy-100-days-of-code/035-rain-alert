🌐 **English** · [Dansk](Architecture-da) · [Bahasa Melayu](Architecture-ms)

# Architecture

The code is split in layers; dependencies point inward (infrastructure to application to domain). The decision is recorded in ADR-0001 (`docs/adr/`).

| Folder | Holds |
| --- | --- |
| `src/rain_alert/domain/` | `HourlyForecast`, `will_rain` |
| `src/rain_alert/application/` | `ForecastSource` and `Notifier` ports, `check_rain`, `run_rain_alert` |
| `src/rain_alert/infrastructure/` | settings, web access, OpenWeather clients, Twilio and dry-run notifiers, `DailyScheduler` |
| `src/rain_alert/constants.py` | constants |
| `src/rain_alert/main.py` | composition root and command line |

## The course script and where it went

| Course script | Rain Alert |
| --- | --- |
| `weather_params` (`lat`, `lon`, `appid`, `cnt`) | `OpenWeatherClient.weather_params`, `OpenWeatherForecastClient.weather_params` |
| `requests.get(...)` | `UrllibTransport` (standard library) |
| loop over `weather[0]["id"] < 700` | `will_rain` in `domain/rain.py` |
| `pywhatkit.sendwhatmsg(...)` | `PywhatkitNotifier` (default; `sendwhatmsg_instantly`) |
| `twilio` `client.messages.create(...)` | `TwilioWhatsAppNotifier` (optional; Twilio REST API with `urllib`) |
| a schedule on PythonAnywhere or GitHub Actions | Windows Task Scheduler, or `DailyScheduler` |
| keys in `os.environ.get(...)` | `Settings` read from `config.env` and the environment |

## Flow

`main()` reads the settings, builds the forecast source named by `FORECAST_API` and the notifier named by `NOTIFIER`, and `run_rain_alert` asks the source for the next 12 hours. `will_rain` decides; if rain is expected the notifier sends exactly one message.
