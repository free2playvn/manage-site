-- Production-safe migration template for a relational database.
-- Replace SQLite DDL with PostgreSQL-safe migration semantics.
CREATE TABLE IF NOT EXISTS departments (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    manager TEXT NOT NULL,
    team_count INTEGER NOT NULL,
    employees INTEGER NOT NULL,
    budget REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    department_id INTEGER NOT NULL REFERENCES departments(id),
    level TEXT NOT NULL,
    permissions TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS employees (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    position TEXT NOT NULL,
    department_id INTEGER NOT NULL REFERENCES departments(id),
    role_id INTEGER NOT NULL REFERENCES roles(id),
    team TEXT NOT NULL,
    status TEXT NOT NULL,
    access_level TEXT NOT NULL,
    avatar TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS refresh_tokens (
    id SERIAL PRIMARY KEY,
    token_hash TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL,
    role TEXT NOT NULL,
    employee_id INTEGER NOT NULL,
    department TEXT NOT NULL,
    issued_at TEXT NOT NULL,
    expires_at TEXT NOT NULL,
    revoked INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS audit_logs (
    id SERIAL PRIMARY KEY,
    action TEXT NOT NULL,
    actor TEXT NOT NULL,
    resource_type TEXT NOT NULL,
    resource_id INTEGER,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    details TEXT NOT NULL
);
