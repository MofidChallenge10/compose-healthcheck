# Compose Healthcheck

A static Docker Compose reliability audit. Find missing healthchecks, references to missing dependencies, and startup-only dependencies that can race application readiness.

```bash
python -m pip install '.[yaml]'
compose-healthcheck compose.yaml
```

Uses PyYAML's safe loader. This is a static configuration check; it does not start containers, prove healthcheck correctness, or replace Docker's own validation.

## Tests
```bash
python -m unittest discover -s tests -v
```

MIT License.
