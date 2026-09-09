#!/usr/bin/env python3
import json
import os
import sqlite3
import urllib.parse
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse

BASE_DIR = Path(__file__).resolve().parent
DB_FILE = BASE_DIR / "company.db"
PORT = int(os.environ.get("PORT", "8001"))
ALLOWED_ORIGIN = os.environ.get("ALLOWED_ORIGIN", "http://127.0.0.1:8000")
ALLOWED_CORS_ORIGINS = {ALLOWED_ORIGIN, "http://localhost:8000"}
API_ALLOW_METHODS = "GET, OPTIONS"
API_ALLOW_HEADERS = "Content-Type, Authorization, X-Requested-With"


def get_origin(handler):
    origin = handler.headers.get("Origin")
    if origin in ALLOWED_CORS_ORIGINS:
        return origin
    return ALLOWED_ORIGIN


def connect_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    if DB_FILE.exists():
        DB_FILE.unlink()

    conn = connect_db()
    try:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS departments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                manager TEXT NOT NULL,
                team_count INTEGER NOT NULL,
                employees INTEGER NOT NULL,
                budget REAL NOT NULL
            );

            CREATE TABLE IF NOT EXISTS roles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                department_id INTEGER NOT NULL,
                level TEXT NOT NULL,
                permissions TEXT NOT NULL,
                FOREIGN KEY(department_id) REFERENCES departments(id)
            );

            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                position TEXT NOT NULL,
                department_id INTEGER NOT NULL,
                role_id INTEGER NOT NULL,
                team TEXT NOT NULL,
                status TEXT NOT NULL,
                access_level TEXT NOT NULL,
                avatar TEXT NOT NULL,
                FOREIGN KEY(department_id) REFERENCES departments(id),
                FOREIGN KEY(role_id) REFERENCES roles(id)
            );

            CREATE TABLE IF NOT EXISTS activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                department TEXT NOT NULL,
                time TEXT NOT NULL,
                type TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS devices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                asset_code TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                owner TEXT NOT NULL,
                department TEXT NOT NULL,
                location TEXT NOT NULL,
                status TEXT NOT NULL,
                last_seen TEXT NOT NULL,
                os TEXT NOT NULL,
                assigned_since TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                owner TEXT NOT NULL,
                department TEXT NOT NULL,
                status TEXT NOT NULL,
                progress INTEGER NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                budget REAL NOT NULL
            );

            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                owner TEXT NOT NULL,
                department TEXT NOT NULL,
                project_id INTEGER,
                status TEXT NOT NULL,
                updated_time TEXT NOT NULL,
                access_level TEXT NOT NULL,
                FOREIGN KEY(project_id) REFERENCES projects(id)
            );

            CREATE TABLE IF NOT EXISTS permissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee TEXT NOT NULL,
                resource_type TEXT NOT NULL,
                resource_name TEXT NOT NULL,
                access_level TEXT NOT NULL,
                granted_by TEXT NOT NULL,
                status TEXT NOT NULL,
                grant_time TEXT NOT NULL
            );
            """
        )

        dep = [
            ("Executive", "Amanda Rivera", 3, 26, 480000),
            ("Operations", "Ken Thompson", 7, 45, 320000),
            ("Technology", "Mina Patel", 8, 78, 900000),
            ("Commercial", "Nathan Reed", 6, 38, 260000),
            ("Finance", "Olivia Brooks", 4, 22, 200000),
        ]

        conn.executemany(
            "INSERT OR IGNORE INTO departments(name, manager, team_count, employees, budget) VALUES(?,?,?,?,?)",
            dep,
        )

        roles = [
            ("Executive Board", 1, "Executive", "Admin, Executive, Decision"),
            ("Operations Director", 2, "Department", "Manager, Operations, Reports"),
            ("Platform Lead", 3, "Technical", "Admin, Technology, Data"),
            ("Sales Strategy", 4, "Commercial", "Manager, Growth, Reports"),
            ("Finance Lead", 5, "Finance", "Finance, Reports, Budget"),
            ("Security Analyst", 3, "Technical", "Admin, Security, Access"),
        ]

        conn.executemany(
            "INSERT OR IGNORE INTO roles(name, department_id, level, permissions) VALUES(?,?,?,?)",
            roles,
        )

        emp = [
            ("Amanda Rivera", "amanda.r@companyhub.com", "Chief Executive", 1, 1, "Leadership", "Active", "Admin", "AR"),
            ("Ken Thompson", "ken.t@companyhub.com", "Operations Director", 2, 2, "Logistics", "Active", "Manager", "KT"),
            ("Mina Patel", "mina.p@companyhub.com", "Platform Lead", 3, 3, "Engineering", "Active", "Owner", "MP"),
            ("Nathan Reed", "nathan.r@companyhub.com", "Sales Strategy", 4, 4, "Growth", "Away", "User", "NR"),
            ("Sarah Wilson", "sarah.w@companyhub.com", "Security Analyst", 3, 6, "Risk", "Active", "Admin", "SW"),
            ("Olivia Brooks", "olivia.b@companyhub.com", "Finance Lead", 5, 5, "Finance", "Active", "Owner", "OB"),
            ("Samuel Stone", "samuel.s@companyhub.com", "Regional Manager", 2, 2, "Field Team", "Active", "Manager", "SS"),
            ("Chris Lee", "chris.l@companyhub.com", "Data Product Manager", 3, 3, "Analytics", "Active", "User", "CL"),
        ]

        conn.executemany(
            "INSERT OR IGNORE INTO employees(name, email, position, department_id, role_id, team, status, access_level, avatar) VALUES(?,?,?,?,?,?,?,?,?)",
            emp,
        )

        activities = [
            ("Operations team update", "Operations", "2 min ago", "update"),
            ("New role assigned", "Technology", "17 min ago", "role"),
            ("Commercial review", "Commercial", "1 hr ago", "report"),
            ("Finance team audit", "Finance", "2 hrs ago", "audit"),
        ]

        conn.executemany(
            "INSERT OR IGNORE INTO activities(title, department, time, type) VALUES(?,?,?,?)",
            activities,
        )

        devices = [
            ("DV-1001", "MacBook Pro 14", "Laptop", "Amanda Rivera", "Executive", "Head Office", "Active", "2026-09-09 08:12", "macOS", "2026-02-14"),
            ("DV-1002", "Dell Latitude 7440", "Laptop", "Ken Thompson", "Operations", "Warehouse A", "Active", "2026-09-09 08:20", "Windows 11", "2026-03-08"),
            ("DV-1003", "iPad Pro", "Tablet", "Mina Patel", "Technology", "Engineering Lab", "Active", "2026-09-09 08:43", "iPadOS", "2026-01-16"),
            ("DV-1004", "Surface Hub", "Conference", "Olivia Brooks", "Finance", "Finance Office", "Standby", "2026-09-09 07:55", "Windows 11", "2026-05-21"),
        ]

        conn.executemany(
            "INSERT OR IGNORE INTO devices(asset_code, name, type, owner, department, location, status, last_seen, os, assigned_since) VALUES(?,?,?,?,?,?,?,?,?,?)",
            devices,
        )

        projects = [
            ("Digital Transformation", "Mina Patel", "Technology", "In Progress", 76, "2026-01-01", "2026-12-31", 94000),
            ("Commercial Expansion", "Nathan Reed", "Commercial", "In Progress", 61, "2026-02-01", "2026-11-30", 60000),
            ("Supply Operations Review", "Ken Thompson", "Operations", "Planning", 43, "2026-04-01", "2026-10-15", 36000),
            ("Compliance Documentation", "Olivia Brooks", "Finance", "Active", 88, "2026-03-01", "2026-09-30", 24000),
        ]

        conn.executemany(
            "INSERT OR IGNORE INTO projects(name, owner, department, status, progress, start_date, end_date, budget) VALUES(?,?,?,?,?,?,?,?)",
            projects,
        )

        documents = [
            ("Employee Access Rules", "Policy", "Amanda Rivera", "Executive", 1, "Approved", "2026-09-09", "Admin"),
            ("Project Roadmap", "Plan", "Mina Patel", "Technology", 1, "In Review", "2026-09-08", "Owner"),
            ("Finance Budget Plan", "Budget", "Olivia Brooks", "Finance", 4, "Approved", "2026-09-09", "Owner"),
            ("Operations Device Rules", "Policy", "Ken Thompson", "Operations", 3, "Active", "2026-09-07", "Manager"),
        ]

        conn.executemany(
            "INSERT OR IGNORE INTO documents(name, type, owner, department, project_id, status, updated_time, access_level) VALUES(?,?,?,?,?,?,?,?)",
            documents,
        )

        permissions = [
            ("Amanda Rivera", "Document", "Employee Access Rules", "Admin", "Olivia Brooks", "Granted", "2026-09-09"),
            ("Mina Patel", "Project", "Digital Transformation", "Owner", "Amanda Rivera", "Granted", "2026-09-09"),
            ("Ken Thompson", "Device", "Dell Latitude 7440", "Manager", "Amanda Rivera", "Granted", "2026-09-08"),
            ("Sarah Wilson", "Document", "Security Standards", "Admin", "Mina Patel", "Granted", "2026-09-08"),
        ]

        conn.executemany(
            "INSERT OR IGNORE INTO permissions(employee, resource_type, resource_name, access_level, granted_by, status, grant_time) VALUES(?,?,?,?,?,?,?)",
            permissions,
        )

        conn.commit()
    finally:
        conn.close()


def api_json(handler, payload, status=200):
    body = json.dumps(payload, ensure_ascii=True).encode("utf-8")
    origin = get_origin(handler)
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.send_header("Cache-Control", "no-store")
    handler.send_header("Access-Control-Allow-Origin", origin)
    handler.send_header("Access-Control-Allow-Methods", API_ALLOW_METHODS)
    handler.send_header("Access-Control-Allow-Headers", API_ALLOW_HEADERS)
    handler.send_header("Vary", "Origin")
    handler.send_header("X-Content-Type-Options", "nosniff")
    handler.send_header("X-Frame-Options", "DENY")
    handler.send_header("Content-Security-Policy", "default-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'none';")
    handler.send_header("Referrer-Policy", "no-referrer")
    handler.send_header("Permissions-Policy", "geolocation=(), microphone=(), camera=()")
    handler.end_headers()
    handler.wfile.write(body)


def api_stats():
    conn = connect_db()
    try:
        total_users = conn.execute("SELECT COUNT(*) AS c FROM employees").fetchone()["c"]
        total_departments = conn.execute("SELECT COUNT(*) AS c FROM departments").fetchone()["c"]
        total_roles = conn.execute("SELECT COUNT(*) AS c FROM roles").fetchone()["c"]
        total_managers = conn.execute("SELECT COUNT(*) AS c FROM employees WHERE access_level IN ('Manager', 'Owner', 'Admin')").fetchone()["c"]

        return {
            "total_users": total_users,
            "departments": total_departments,
            "managers": total_managers,
            "roles": total_roles,
            "access_level": "76%",
            "updated_at": "2026-09-09T00:00:00Z",
        }
    finally:
        conn.close()


def api_departments():
    conn = connect_db()
    try:
        rows = conn.execute(
            """
            SELECT id, name, manager, team_count, employees, budget
            FROM departments
            ORDER BY id ASC
            """
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def api_employees(role=None):
    conn = connect_db()
    try:
        query = """
            SELECT e.id, e.name, e.email, e.position, e.team, e.status, e.access_level, e.avatar,
                   d.name AS department, r.name AS role_name, r.level AS role_level, r.permissions
            FROM employees e
            JOIN departments d ON d.id = e.department_id
            JOIN roles r ON r.id = e.role_id
        """
        params = []
        if role and role != 'all':
            role_norm = role.strip().lower()
            query += " WHERE LOWER(d.name) = ? OR LOWER(r.name) = ?"
            params = [role_norm, role_norm]
        query += " ORDER BY e.id ASC"
        rows = conn.execute(query, params).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def api_roles():
    conn = connect_db()
    try:
        rows = conn.execute(
            """
            SELECT r.id, r.name, r.level, r.permissions, d.name AS department
            FROM roles r
            JOIN departments d ON d.id = r.department_id
            ORDER BY r.id ASC
            """
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def api_activity():
    conn = connect_db()
    try:
        rows = conn.execute("SELECT id,title,department,time,type FROM activities ORDER BY id DESC LIMIT 4").fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def api_devices():
    conn = connect_db()
    try:
        rows = conn.execute("SELECT id, asset_code, name, type, owner, department, location, status, last_seen, os, assigned_since FROM devices ORDER BY id ASC").fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def api_projects():
    conn = connect_db()
    try:
        rows = conn.execute("SELECT id, name, owner, department, status, progress, start_date, end_date, budget FROM projects ORDER BY id ASC").fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def api_documents():
    conn = connect_db()
    try:
        rows = conn.execute("SELECT d.id, d.name, d.type, d.owner, d.department, d.status, d.updated_time, d.access_level, p.name AS project_name FROM documents d LEFT JOIN projects p ON p.id = d.project_id ORDER BY d.id ASC").fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def api_permissions():
    conn = connect_db()
    try:
        rows = conn.execute("SELECT id, employee, resource_type, resource_name, access_level, granted_by, status, grant_time FROM permissions ORDER BY id ASC").fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


class CompanyHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, directory=None, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

    def do_OPTIONS(self):
        origin = get_origin(self)
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", origin)
        self.send_header("Access-Control-Allow-Methods", API_ALLOW_METHODS)
        self.send_header("Access-Control-Allow-Headers", API_ALLOW_HEADERS)
        self.send_header("Vary", "Origin")
        self.send_header("Content-Length", "0")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path
        if path.startswith('/api/'):
            self.handle_api(path)
            return

        if path == '/':
            path = '/index.html'

        requested = (BASE_DIR / path.lstrip('/')).resolve(strict=False)
        root = BASE_DIR.resolve()
        if root not in requested.parents and requested != root:
            self.send_error(403, 'Forbidden path')
            return
        if not requested.exists() or requested.is_dir():
            self.send_error(404, 'Resource not found')
            return

        try:
            data = requested.read_bytes()
            content_type = 'text/html; charset=utf-8' if requested.name.endswith('.html') else 'application/octet-stream'
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Cache-Control', 'public, max-age=86400')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('X-Frame-Options', 'DENY')
            self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self' http://127.0.0.1:8001; object-src 'none'; base-uri 'self'; frame-ancestors 'none';")
            self.send_header('Referrer-Policy', 'no-referrer')
            self.end_headers()
            self.wfile.write(data)
        except Exception as exc:
            self.send_error(500, str(exc))

    def handle_api(self, path):
        try:
            if path == '/api/overview':
                payload = {
                    "stats": api_stats(),
                    "departments": api_departments(),
                    "roles": api_roles(),
                    "employees": api_employees(),
                    "activities": api_activity(),
                    "devices": api_devices(),
                    "projects": api_projects(),
                    "documents": api_documents(),
                    "permissions": api_permissions(),
                }
                api_json(self, payload)
            elif path == '/api/stats':
                api_json(self, api_stats())
            elif path == '/api/departments':
                api_json(self, api_departments())
            elif path == '/api/employees':
                parsed = urlparse(self.path)
                role = urllib.parse.parse_qs(parsed.query).get('role', ['all'])[0]
                api_json(self, api_employees(role.lower()))
            elif path == '/api/roles':
                api_json(self, api_roles())
            elif path == '/api/activity':
                api_json(self, api_activity())
            elif path == '/api/devices':
                api_json(self, api_devices())
            elif path == '/api/projects':
                api_json(self, api_projects())
            elif path == '/api/documents':
                api_json(self, api_documents())
            elif path == '/api/permissions':
                api_json(self, api_permissions())
            else:
                api_json(self, {"error": "Endpoint not found"}, status=404)
        except Exception as exc:
            api_json(self, {"error": str(exc)}, status=500)

    def log_message(self, format, *args):
        # Keep console logs lightweight and clean.
        return


if __name__ == '__main__':
    init_db()
    httpd = ThreadingHTTPServer(("0.0.0.0", PORT), CompanyHandler)
    print(f"Company dashboard API running at http://0.0.0.0:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")
        httpd.server_close()
