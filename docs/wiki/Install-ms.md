🌐 [English](Install) · [Dansk](Install-da) · **Bahasa Melayu**

# Pemasangan

> Nota: terjemahan Bahasa Melayu ini belum disemak oleh penutur asli; bahasa Inggeris ialah teks rasmi.

## Keperluan

- Python 3.13 atau lebih baharu dengan `venv`.
- Tiada kebergantungan pihak ketiga semasa dijalankan. `pytest`, `ruff`, `mypy` (dan `tzdata` pada Windows) hanya alat pembangunan.
- Untuk mesej harian: Docker Desktop, kunci API OpenWeather dan akaun Twilio dengan sandbox WhatsApp.

## Windows (PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Linux dan macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

`python -m pip install --upgrade pip` menaik taraf pip di dalam `.venv`. Folder `.venv` diabaikan oleh git.

## Tetapan

Salin contoh dan isikan nilai anda sendiri. `config.env` diabaikan oleh git dan tidak pernah disalin ke dalam imej Docker.

```bash
cp config.env.example config.env
```

| Tetapan | Maksud |
| --- | --- |
| `OPENWEATHER_APIKEY` | Kunci API OpenWeather (digunakan untuk ramalan 2.5 percuma) |
| `OPENWEATHER4_APIKEY` | Kunci langganan One Call 4.0 (kembali kepada kunci di atas) |
| `FORECAST_API` | `onecall4` (lalai) atau `forecast25` |
| `LATITUDE`, `LONGITUDE` | Tempat yang disemak |
| `PHONENUMBER` | Nombor WhatsApp anda dalam format antarabangsa |
| `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN` | Daripada konsol Twilio |
| `TWILIO_WHATSAPP_FROM` | Nombor sandbox Twilio |
| `ALERT_TIME`, `TZ` | Waktu tempatan semakan harian dan zon waktunya |
