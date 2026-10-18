🌐 **English** · [Dansk](Testing-da) · [Bahasa Melayu](Testing-ms)

# Testing

Run these from the repository root with the `.venv` active:

```bash
python -m pytest
python -m pytest --cov=rain_alert
python -m ruff check src tests
python -m ruff format --check src tests
python -m mypy src tests
doxygen Doxyfile
```

The tests use fakes and need no internet (the web access test uses a local server). The end-to-end tests start the program as a separate process. No test reads your `config.env`. Doxygen writes the API documentation to `doxygen/html`.
