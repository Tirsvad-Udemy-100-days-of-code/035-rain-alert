🌐 [English](Testing) · **Dansk** · [Bahasa Melayu](Testing-ms)

# Test

Kør disse fra repositoryets rod med `.venv` aktiv:

```bash
python -m pytest
python -m pytest --cov=rain_alert
python -m ruff check src tests
python -m ruff format --check src tests
python -m mypy src tests
doxygen Doxyfile
```

Testene bruger falske afhængigheder og kræver ikke internet (testen af webadgang bruger en lokal server). End-to-end-testene starter programmet som en separat proces. Ingen test læser din `config.env`. Doxygen skriver API-dokumentationen til `doxygen/html`.
