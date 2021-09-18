def test_register_data(client):
    r = client.get('/register')
    assert b"Already Have An Account?" in r.data


def register_post(client, email, password):
    return client.post('/register', data=dict(
        email=email, password=password),
        follow_redirects=True)


def test_register(client, Database):
    email = 'test@email.com'
    password = 'test'
    r = register_post(client, email, password)
    assert r.status_code == 200
    results = Database.users.find_one({'email': email, 'password': password})
    assert results != None
