#!/usr/bin/env python3
import json
import urllib.request
import urllib.error
import sys

BASE = 'http://127.0.0.1:8001'

def request(path, method='GET', payload=None, token=None):
    data = None
    headers = {'Origin': 'http://127.0.0.1:8000'}
    if payload is not None:
        data = json.dumps(payload).encode('utf-8')
        headers['Content-Type'] = 'application/json'
    if token:
        headers['Authorization'] = 'Bearer ' + token
    req = urllib.request.Request(BASE + path, data=data, method=method, headers=headers)
    try:
        resp = urllib.request.urlopen(req, timeout=5)
        out = resp.status, resp.read().decode('utf-8')
        return out
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8')


def main():
    checks = []
    # login check
    status, body = request('/api/login', method='POST', payload={'email': 'admin@companyhub.com', 'password': 'admin123'})
    checks.append(('login', status == 200 and 'login_ok' in body))
    token = None
    try:
        token = json.loads(body).get('token')
    except Exception:
        token = None

    # route smoke checks
    status, body = request('/api/overview', method='GET', token=token)
    checks.append(('overview', status == 200 and 'audit_logs' in body))
    status, body = request('/api/departments', method='GET', token=token)
    checks.append(('departments', status == 200 and 'Executive' in body))
    status, body = request('/api/employees', method='GET', token=token)
    checks.append(('employees', status == 200 and 'Amanda Rivera' in body))
    status, body = request('/api/roles', method='GET', token=token)
    checks.append(('roles', status == 200 and 'Executive Board' in body))
    status, body = request('/api/leave-requests', method='GET', token=token)
    checks.append(('leave_requests', status == 200 and 'Annual Leave' in body))
    status, body = request('/api/tasks', method='GET', token=token)
    checks.append(('tasks', status == 200 and 'Security Policy Review' in body))
    status, body = request('/api/audit-logs', method='GET', token=token)
    checks.append(('audit_logs', status == 200 and 'document_access' in body))

    failed = [name for name, ok in checks if not ok]
    if failed:
        print('FAILED:', ', '.join(failed))
        sys.exit(2)
    print('PASS smoke tests:', len(checks))


if __name__ == '__main__':
    main()
