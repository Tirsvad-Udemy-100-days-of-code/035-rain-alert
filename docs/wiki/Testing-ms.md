🌐 [English](Testing) · [Dansk](Testing-da) · **Bahasa Melayu**

# Ujian

> Nota: terjemahan Bahasa Melayu ini belum disemak oleh penutur asli; bahasa Inggeris ialah teks rasmi.

Jalankan ini dari akar repositori dengan `.venv` aktif:

```bash
python -m pytest
python -m pytest --cov=rain_alert
python -m ruff check src tests
python -m ruff format --check src tests
python -m mypy src tests
doxygen Doxyfile
```

Ujian menggunakan objek palsu dan tidak memerlukan internet (ujian akses web menggunakan pelayan setempat). Ujian hujung ke hujung memulakan program sebagai proses berasingan. Tiada ujian membaca `config.env` anda. Doxygen menulis dokumentasi API ke `doxygen/html`.
