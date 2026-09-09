# Manage Site Dashboard

A lightweight organizational dashboard with static HTML, CSS, JavaScript, and a Python SQLite-backed API.

## Features

- Responsive dashboard UI for departments, employees, roles, permissions, devices, projects, and documents.
- Lightweight local API using Python `http.server` and SQLite.
- Resource sections for devices, documents, projects, permissions, and overview stats.

## Run locally

```bash
python server.py
python -m http.server 8000
```

Then open:

```text
http://127.0.0.1:8000
```

## API

```text
GET /api/overview
GET /api/devices
GET /api/projects
GET /api/documents
GET /api/permissions
```
