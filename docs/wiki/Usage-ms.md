🌐 [English](Usage) · [Dansk](Usage-da) · **Bahasa Melayu**

# Penggunaan

> Nota: terjemahan Bahasa Melayu ini belum disemak oleh penutur asli; bahasa Inggeris ialah teks rasmi.

Dengan `.venv` aktif dan `config.env` diisi:

```bash
python -m rain_alert --once --dry-run
python -m rain_alert --once
python -m rain_alert
```

- `--once --dry-run` menyemak sekarang dan mencetak mesej, bukan menghantarnya. Ia tidak memerlukan tetapan Twilio.
- `--once` menyemak sekarang dan menghantar mesej WhatsApp jika hujan dijangka. Dengan pywhatkit, WhatsApp Web dibuka dalam pelayar lalai anda, yang mesti sudah log masuk.
- Tanpa pilihan, program berjalan setiap hari pada `ALERT_TIME`.

![Larian cuba yang menjangka hujan](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/035-rain-alert/raw/branch/main/docs/images/dry-run-rain.png)

![Larian cuba yang tidak menjangka hujan](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/035-rain-alert/raw/branch/main/docs/images/dry-run-no-rain.png)

Program menghantar satu mesej apabila mana-mana id keadaan cuaca dalam 12 jam akan datang kurang daripada 700 (ribut petir, renyai, hujan, salji), dan tiada apa-apa jika tidak.

![Mesej seperti yang tiba dalam WhatsApp (segala-galanya kecuali mesej dikaburkan)](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/035-rain-alert/raw/branch/main/docs/images/whatsapp-message.png)

## Kod keluar

| Kod | Maksud |
| --- | --- |
| 0 | Berjaya |
| 1 | Ramalan atau mesej gagal |
| 2 | Tetapan tiada atau tidak sah (mesej menyebut kunci, tidak pernah nilainya) |

## Ramalan yang mana

`FORECAST_API=onecall4` menggunakan ramalan setiap jam One Call 4.0, yang memerlukan langganan One Call by Call yang berasingan. `FORECAST_API=forecast25` menggunakan ramalan 2.5 percuma dengan satu entri setiap tiga jam, seperti dalam kursus.

## Setiap pagi pada Windows

pywhatkit memerlukan pelayar anda yang telah log masuk, jadi jadualkan `--once` dengan Windows Task Scheduler (tugas berjalan semasa anda log masuk). Arahan ini mencipta tugas harian pada 07:00, menjalankannya sekali sekarang dan memadamkannya semula:

```powershell
$python = (Resolve-Path .venv\Scripts\python.exe).Path
schtasks /Create /TN "Rain Alert" /SC DAILY /ST 07:00 /IT /TR "cmd /c cd /d $PWD && $python -m rain_alert --once"
schtasks /Run /TN "Rain Alert"
schtasks /Delete /TN "Rain Alert" /F
```

## Docker Desktop (dengan Twilio)

Bekas tidak mempunyai pelayar, jadi `compose.yaml` menetapkan `NOTIFIER=twilio`.

```bash
docker compose up -d --build
docker compose logs -f
docker compose run --rm rain-alert python -m rain_alert --once --dry-run
docker compose down
```

![Bekas di Docker Desktop](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/035-rain-alert/raw/branch/main/docs/images/docker-container.png)

Bekas membaca `config.env` semasa bermula dan menyemak cuaca setiap hari pada `ALERT_TIME`. Ia dimulakan semula bersama Docker Desktop.

## WhatsApp melalui Twilio (pilihan)

1. Buka Twilio Sandbox for WhatsApp dalam konsol Twilio dan sertainya daripada telefon anda.
2. Letakkan SID akaun, token pengesahan dan nombor sandbox dalam `config.env`, tetapkan `NOTIFIER=twilio`, dan letakkan nombor anda sendiri dalam `PHONENUMBER`.
3. Sandbox melupakan telefon anda selepas 72 jam tanpa mesej; sertai semula jika tiada mesej tiba.
