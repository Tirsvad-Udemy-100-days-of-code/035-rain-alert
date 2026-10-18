🌐 [English](Architecture) · [Dansk](Architecture-da) · **Bahasa Melayu**

# Seni bina

> Nota: terjemahan Bahasa Melayu ini belum disemak oleh penutur asli; bahasa Inggeris ialah teks rasmi.

Kod dibahagikan kepada lapisan; kebergantungan menghala ke dalam (infrastruktur ke aplikasi ke domain). Keputusan itu dicatat dalam ADR-0001 (`docs/adr/`).

| Folder | Mengandungi |
| --- | --- |
| `src/rain_alert/domain/` | `HourlyForecast`, `will_rain` |
| `src/rain_alert/application/` | port `ForecastSource` dan `Notifier`, `check_rain`, `run_rain_alert` |
| `src/rain_alert/infrastructure/` | tetapan, akses web, klien OpenWeather, pemberitahu Twilio dan larian cuba, `DailyScheduler` |
| `src/rain_alert/constants.py` | pemalar |
| `src/rain_alert/main.py` | akar komposisi dan baris perintah |

## Skrip kursus dan ke mana ia pergi

| Skrip kursus | Rain Alert |
| --- | --- |
| `weather_params` (`lat`, `lon`, `appid`, `cnt`) | `OpenWeatherClient.weather_params`, `OpenWeatherForecastClient.weather_params` |
| `requests.get(...)` | `UrllibTransport` (pustaka standard) |
| gelung atas `weather[0]["id"] < 700` | `will_rain` dalam `domain/rain.py` |
| `twilio` `client.messages.create(...)` | `TwilioWhatsAppNotifier` (API REST Twilio dengan `urllib`) |
| jadual di PythonAnywhere atau GitHub Actions | `DailyScheduler` dalam bekas Docker |
| kunci dalam `os.environ.get(...)` | `Settings` dibaca daripada `config.env` dan persekitaran |

## Aliran

`main()` membaca tetapan, membina sumber ramalan yang dinamakan oleh `FORECAST_API` dan pemberitahu, dan `run_rain_alert` meminta sumber untuk 12 jam akan datang. `will_rain` memutuskan; jika hujan dijangka, pemberitahu menghantar tepat satu mesej.
