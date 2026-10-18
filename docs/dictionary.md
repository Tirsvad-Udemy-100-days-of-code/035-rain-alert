# Domain Dictionary: Rain Alert

## Metadata
| Key | Value |
| --- | --- |
| ID | DICT-001 |
| CrossReference | [BC-001], [SA-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-18 | Deprecated | Jens Tirsvad Nielsen | AI as stand-in for S01 | Forecast period in the definition of the hourly forecast; added forecast API | [5da8060] |
| 2026-10-18 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Added WhatsApp Web message and alert channel | [6434347] |

---

## Purpose and Scope

Maps each Product Owner (PO) term to its professional IT term for Rain Alert. The PO language is English (`en`) and the PO domain is Software and IT (`it`); the PO terms are the words of the course assignment and of S01, the IT terms are the class, function and attribute names used in the source code. The dictionary covers the terms of [BC-001]; the project has no Domain Model yet.

## Dictionary

| PO term | Language | IT term | Definition | Used as PO term in | Used as IT term in |
| --- | --- | --- | --- | --- | --- |
| hourly forecast | en | HourlyForecast | The expected weather for one forecast period (one hour for One Call 4.0, three hours for the 2.5 forecast), with its weather condition ids. | BC, MIL | PY |
| weather condition id | en | condition_id | The OpenWeather number that names a kind of weather; a number below 700 means thunderstorm, drizzle, rain or snow. | BC, MIL | PY |
| rain expected | en | will_rain | The decision that at least one of the next 12 hourly forecasts has a weather condition id below 700. | BC, MIL | PY |
| forecast source | en | ForecastSource | The service that supplies the hourly forecast, here the OpenWeather One Call 4.0 API. | BC, MIL | PY |
| rain check | en | check_rain | The use case that fetches the next 12 hours and returns whether rain is expected. | BC, MIL | PY |
| request parameters | en | weather_params | The latitude, longitude, API key and units sent to the forecast source. | BC, MIL | PY |
| location | en | latitude, longitude | The place whose weather is checked, here 2.927761, 101.897999. | BC, MIL | PY |
| alert | en | Notifier | The component that tells the owner to bring an umbrella. | BC, MIL | PY |
| WhatsApp message | en | TwilioWhatsAppNotifier | The alert sent as a WhatsApp message through the Twilio sandbox. | BC, MIL | PY |
| WhatsApp Web message | en | PywhatkitNotifier | The alert sent as a WhatsApp message through WhatsApp Web in the browser of the host, with pywhatkit. | BC, MIL | PY |
| alert channel | en | notifier | The setting that names how the alert is sent: `pywhatkit` or `twilio`. | BC, MIL | PY |
| dry run | en | DryRunNotifier | A run that prints the message instead of sending it. | BC, MIL | PY |
| alert time | en | alert_time | The local time of day at which the daily check runs, default 07:00. | BC, MIL | PY |
| forecast API | en | forecast_api | The setting that names the OpenWeather endpoint used: `onecall4` or `forecast25`. | BC, MIL | PY |
| daily scheduler | en | Scheduler | The loop that waits for the alert time and runs the rain check once a day. | BC, MIL | PY |
| configuration file | en | config.env | The git-ignored file with the API key, phone number, location and Twilio values, passed to the container as environment variables. | BC, MIL | PY |
| settings | en | Settings | The values read from the environment for one run. | BC, MIL | PY |

## Rules

- The Business Case and the milestones use the PO term; the source code uses the IT term. `PY` is the short name of Python source code in the catalog.
- One IT term per PO term and one PO term per IT term; no synonyms.
- A new concept in the code gets a row in the same change.

---

[BC-001]: ./business-case.md
[SA-001]: ./stakeholder-analysis.md
[728ff3e]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/035-rain-alert/commit/728ff3e9e195f722540d4959f4f0035b7af37c36
[5da8060]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/035-rain-alert/commit/5da8060e2000533a95fed0b380e9ba2aa8b25be2
[6434347]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/035-rain-alert/commit/64343473499f718679459bbf4b580073ffafa370
