import pytest
from wateraid import create_app
from pymongo import MongoClient
import mongomock
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import DiscoveryV1
from wateraid.config import Config
from flask_login import login_user, logout_user


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    ctx = app.app_context()
    ctx.push()
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def Database():
    client = mongomock.MongoClient("mongodb://localhost:27017")
    client = MongoClient()
    Database = client.tests
    reg_users = Database.users
    results = Database.results
    saved = Database.saved
    Database.saved.insert_one({'userid': 'test@email.com', 'results': [{'results': [
                              {'id': 'PAsJ6CGMv7ItDkZHjArg4AZsIpee7ndHaAiRS8rjoQsHKpCWkRGSAIOqXY5EzfuQ'}]}]})
    yield Database


@pytest.fixture
def query_results(Database):
    authenticator_discovery = IAMAuthenticator(
        Config.AUTHENTICATOR_DISCOVERY)
    discovery = DiscoveryV1(
        version='2017-09-01',
        authenticator=authenticator_discovery
    )
    discovery.set_service_url(Config.DISCOVERY_SERVICE_URL)
    query_results = discovery.query(
        environment_id='system',
        collection_id='news-en',
        natural_language_query='water',
        deduplicate=True,
        count=3,
    ).get_result()
    Database.results.insert_one({'query_results': query_results})
    return query_results


@pytest.fixture
def user(Database):
    """ Creates a user """
    from wateraid.users.user import User
    user = User(email='test@email.com')
    password = user.set_password('test')
    Database.users.insert_one({'email': user.email, 'password': password})
    return user


@pytest.fixture
def log_in_user(app, request, user):
    """ Creates a logged in user and logs them out again when the test is complete using Flask-Login """
    with app.test_request_context():
        login_user(user)

    request.addfinalizer(logout_user)


# python -m pytest tests
# python -m pytest --setup-show --cov=wateraid
