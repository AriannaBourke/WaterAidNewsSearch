def test_home(client):
    r = client.get('/home')
    assert r.status_code == 200


def test_help(client):
    r = client.get('/help')
    assert r.status_code == 200


def test_login(client):
    r = client.get('/login')
    assert r.status_code == 200


def test_register(client):
    r = client.get('/register')
    assert r.status_code == 200


def test_search_results(client):
    r = client.get('/search_results')
    assert r.status_code == 200


def test_search(client):
    r = client.get('/search_results?search=water+shortage')
    assert r.status_code == 200


def test_context(app):
    from flask import request
    with app.test_request_context('/search_results?search=water+shortage'):
        assert request.path == '/search_results'
        assert request.args['search'] == 'water shortage'


def test_account(client):
    r = client.get('/account')
    assert r.status_code == 200


def test_trends(client):
    r = client.get('/trends')
    assert r.status_code == 200


def test_article(client):
    r = client.get(
        '/article/yjVI__d_P_bim8N6b_21-cfRR6VZCkQka-RQ2F7ZYaM2aINCJFhs4C65LvE67iRk')
    assert r.status_code == 200


def test_404(client):
    r = client.get('/12345')
    assert r.status_code == 404
    assert b'Oops. Page Not Found' in r.data
