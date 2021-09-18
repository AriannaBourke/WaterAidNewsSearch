from wateraid.trends.utils import concepts_dataset, find_concepts, find_search_terms, find_sentiments, sentiment_dataset, find_keywords
import pytest


@pytest.fixture
def results_found(Database):
    results_found = Database.results.find({},
                                          {"query_results.results.enriched_text.concepts.text": 1,
                                           "query_results.results.enriched_text.sentiment.document.label": 1,
                                           "query_results.results.enriched_text.keywords.text": 1,
                                           'search_term': 1
                                           })
    return results_found


def test_find_concepts(results_found):
    res = find_concepts(results_found)
    assert isinstance(res, list)
    assert 'Water' in res


def test_concepts_dataset(results_found):
    res = find_concepts(results_found)
    dataset = concepts_dataset(res)
    assert isinstance(dataset, dict)
    for x in dataset['children']:
        assert 'Name' in x
        assert 'Count' in x


def test_find_sentiment(results_found):
    res = find_sentiments(results_found)
    assert isinstance(res, list)
    assert 'positive' in res


def test_sentiment_dataset(results_found):
    res = find_sentiments(results_found)
    assert sentiment_dataset(res) != [0]


def test_find_keywords(results_found):
    res = find_keywords(results_found)
    assert isinstance(res, str)
    assert 'Water' in res
