from wateraid.article.utils import results, emotions
import pytest
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EmotionOptions
from wateraid.config import Config


@pytest.fixture
def results_found(Database):
    page_id = '7uc_Iw3_Vb0kRlBmyZzolWHddLPxbirajX9XGI_E0fGD6e6d7YqUl86MqlNN8hDc'
    results_found = Database.results.aggregate([
        {
            '$match': {'query_results.results.id': page_id}
        },
        {'$project': {
            'results': {'$filter': {
                'input': '$query_results.results',
                'as': 'result',
                'cond': {'$eq': ['$$result.id', page_id]}
            }},
            '_id': 0,
            "query_results.results.enriched_text.concepts.text": 1,
            "query_results.results.enriched_text.entities": 1,
            'query_results.results.publication_date': 1,
            'query_results.results.title':1,
            'query_results.results.text':1,
            'query_results.results.host':1,
            "query_results.results.enriched_text.concepts.text": 1,
            "query_results.results.enriched_text.sentiment.document.label": 1,
            "query_results.results.enriched_text.keywords.text": 1
        }}
    ])
    return results_found


4


@pytest.fixture
def results_list(Database):
    page_id = '7uc_Iw3_Vb0kRlBmyZzolWHddLPxbirajX9XGI_E0fGD6e6d7YqUl86MqlNN8hDc'
    results_found = Database.results.aggregate([
        {
            '$match': {'query_results.results.id': page_id}
        },
        {'$project': {
            'results': {'$filter': {
                'input': '$query_results.results',
                'as': 'result',
                'cond': {'$eq': ['$$result.id', page_id]}
            }},
            '_id': 0,
            "query_results.results.enriched_text.concepts.text": 1,
            "query_results.results.enriched_text.entities": 1,
            'query_results.results.publication_date': 1,
            'query_results.results.title':1,
            'query_results.results.text':1,
            'query_results.results.host':1,
            "query_results.results.enriched_text.concepts.text": 1,
            "query_results.results.enriched_text.sentiment.document.label": 1,
            "query_results.results.enriched_text.keywords.text": 1
        }}
    ])
    results_list = []
    for res in results_found:
        results_list.append(res['results'][0])
    return results_list


def test_results_date(results_found):
    res = results(results_found)
    """ Test if date in correct format"""
    assert '09 Sep 2021' in res[1]
    """Test if output is a list"""
    assert isinstance(res[0], list)


def test_emotions_url(results_list):
    assert 'url' in results_list[0]


def test_emotions_no_url():
    results_list = []
    assert emotions(results_list) == {}


def test_emotions_NLU(results_list):
    authenticator_NLU = IAMAuthenticator(Config.AUTHENTICATOR_NLU)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2020-08-01',
        authenticator=authenticator_NLU
    )
    natural_language_understanding.set_service_url(Config.NLU_SERVICE_URL)
    res = emotions(results_list)
    assert 'anger' in res
    assert 'disgust' in res
    assert 'fear' in res
    assert 'joy' in res
    assert 'sadness' in res
