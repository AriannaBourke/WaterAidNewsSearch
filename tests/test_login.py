def login(client, email, password):
    """ Login setup """
    return client.post('/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)


def logout(client):
    """ Logout setup """
    return client.get('/logout', follow_redirects=True)


def test_login_data(client):
    """ Test login route and data returned on page correct"""
    r = client.get('/login')
    assert b"Need An Account?" in r.data


def test_login_success(client, user):
    """ Test login post request when successful"""
    r = client.post('/login', data=dict(
        email=user.email,
        password=user.password
    ), follow_redirects=True)
    assert r.status_code == 200
    assert b'Log in successful' in r.data


def test_login_fails(client):
    """ Test login post request when unsuccessful"""
    r = login(client, email="wrong@emai.com", password='123')
    assert b'Log in unsuccessful' in r.data


def test_logout(client):
    """ Test logout successful """
    r = logout(client)
    assert r.status_code == 200


def test_search_displayed_when_logged_in(client, user):
    """ Test search only displayed when logged in """
    r = login(client, email=user.email, password=user.email)
    r = client.get('/home')
    assert r.status_code == 200
    assert b'Search' in r.data


def test_login_displayed_when_not_logged_in(client):
    """ Test login prompt only displayed when not logged in """
    r = client.get('/home')
    assert r.status_code == 200
    assert b'Log In' in r.data
