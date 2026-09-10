#!/usr/bin/env python3
import json
import urllib.request
import urllib.error
import sys

BASE = 'http://127.0.0.1:8001'


def request(path, method='GET', payload=None, token=None, x_forwarded_for=None):
    data = None
    headers = {'Origin': 'http://127.0.0.1:8000'}
    if payload is not None:
        data = json.dumps(payload).encode('utf-8')
        headers['Content-Type'] = 'application/json'
    if token:
        headers['Authorization'] = 'Bearer ' + token
    if x_forwarded_for:
        headers['X-Forwarded-For'] = x_forwarded_for
    req = urllib.request.Request(BASE + path, data=data, method=method, headers=headers)
    try:
        resp = urllib.request.urlopen(req, timeout=5)
        return resp.status, resp.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8')


def parse_json(body):
    try:
        return json.loads(body)
    except Exception:
        return {}


def main():
    checks = []

    # Login returns actual signed JWT access token plus signed JWT refresh token.
    status, body = request('/api/login', method='POST', payload={'email': 'admin@companyhub.com', 'password': 'admin123'})
    print('login:', status, body[:80])
    token = parse_json(body).get('token') if status == 200 else None
    refresh_token = parse_json(body).get('refresh_token') if status == 200 else None
    checks.append(('login_200', status == 200 and bool(token) and bool(refresh_token)))

    # 401 missing authentication
    missing_token_status, missing_token_body = request('/api/accounts', method='GET', x_forwarded_for='401_ip')
    checks.append(('401_missing_auth', missing_token_status == 401))

    # 403 forbidden role from low privilege user
    employee_status, employee_body = request('/api/login', method='POST', payload={'email': 'amanda.r@companyhub.com', 'password': 'employee123'}, x_forwarded_for='403_ip')
    emp_token = parse_json(employee_body).get('token') if employee_status == 200 else None
    forbid_status, forbid_body = request('/api/accounts', method='GET', token=emp_token, x_forwarded_for='403_ip')
    checks.append(('403_forbidden_role', forbid_status == 403))

    # 429 rate limit from a different IP, isolated from 401/403/404/409/refresh.
    rate_status = 200
    for idx in range(140):
        s, b = request('/api/stats', method='GET', token=token, x_forwarded_for='429_ip')
        if s == 429:
            rate_status = 429
            break
    checks.append(('429_rate_limit', rate_status == 429))

    # 404 route
    not_found_status, not_found_body = request('/api/no-such-route', method='GET', token=token, x_forwarded_for='404_ip')
    checks.append(('404_not_found', not_found_status == 404))

    # 409 duplicate email on account creation
    dup_status, dup_body = request('/api/accounts', method='POST', payload={
        'name': 'Rina Bennett', 'email': 'admin@companyhub.com', 'password': 'admin123', 'role': 'admin'
    }, token=token, x_forwarded_for='409_ip')
    checks.append(('409_duplicate_email', dup_status == 409))

    # Refresh route rotates access and refresh token as JWT objects.
    refresh_status, refresh_body = request('/api/refresh', method='POST', payload={'refresh_token': refresh_token}, token=token, x_forwarded_for='refresh_ip')
    checks.append(('refresh_200', refresh_status == 200 and 'token_refreshed' in refresh_body))

    failed = [name for name, ok in checks if not ok]
    if failed:
        print('FAILED:', ', '.join(failed))
        sys.exit(2)
    print('PASS auth and error smoke tests:', len(checks))


if __name__ == '__main__':
    main()
