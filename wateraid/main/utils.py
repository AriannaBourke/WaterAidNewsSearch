from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import DiscoveryV1
from datetime import datetime
from wateraid.database import Database
from wateraid.config import Config

authenticator_discovery = IAMAuthenticator(
    Config.AUTHENTICATOR_DISCOVERY)
discovery = DiscoveryV1(
    version='2017-09-01',
    authenticator=authenticator_discovery
)
discovery.set_service_url(Config.DISCOVERY_SERVICE_URL)


def search_query(search):
    """ Watson Discovery query with user input search term """
    try:
        query_results = discovery.query(
            environment_id='system',
            collection_id='news-en',
            natural_language_query=search,
            deduplicate=True,
            count=50,
        ).get_result()
    except:
        query_results = ''
    return query_results


def insert_results(query_results, search):
    """ Insert query results in Results collection """
    today_date = datetime.now().date().strftime("%Y-%m-%d")
    Database.results.insert_one({'search_term': search, 'date': today_date,
                                 'filter': '', 'language': 'English', 'query_results': query_results})
