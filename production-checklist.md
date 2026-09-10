# Production-readiness checklist

This repository is still a Python static HTML + SQLite-backed local dashboard. The items below model the production transition path requested by the user and should be adopted in a real deployment pipeline.

## Required environment variables

- `ALLOWED_ORIGIN`
- `ALLOWED_CORS_ORIGINS`
- `JWT_SECRET` or `JWT_SECRET_FILE`
- `HTTPS_OR_TLS`
- `CONTENT_SECURITY_POLICY`
- `DB_DSN`

## Production rules

1. Do not commit `JWT_SECRET` or any private key in source.
2. Inject `JWT_SECRET` from a secret manager or file-backed secret provider.
3. Run behind TLS/HTTPS and set `Strict-Transport-Security` header.
4. Restrict `ALLOWED_CORS_ORIGINS` in production to trusted domains only.
5. Do not use SQLite for production traffic; use PostgreSQL/MySQL/Azure SQL with migrations.
6. Capture audit log on every POST/PATCH/DELETE route and retain immutable logs for forensic review.
7. Use CI/CD scans for dependency vulnerability, secret scanning and test gates before deploy.
8. Backups and DB role enforcement are mandatory for live environments.
