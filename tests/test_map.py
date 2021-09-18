from wateraid.search.utils import map
import pytest


@pytest.fixture
def test_query(query_results, Database):
    Database.results.insert_one(
        {'search_term': 'water', 'query_results': query_results})


@pytest.fixture
def results_map_found(Database):
    results_map_found = Database.results.find({},
                                              {"query_results.results.enriched_text.entities": 1, 'query_results.results.id': 1,
                                               'query_results.results.title': 1, 'query_results.results.score': 1}).sort('_id', -1).limit(1)
    return results_map_found


@pytest.fixture
def trends_map_results(Database):
    trends_map_results = Database.results.find(
        {}, {"query_results.results.enriched_text.entities": 1})
    return trends_map_results


def test_map(results_map_found):
    """ Test if each result contains all required fields for plotting map markers"""
    results = map(results_map_found)
    for res in results:
        assert 'lat' and 'long' and 'id' and 'title' and 'score' and 'entity' in res
        assert 'concept' not in res


def test_map_longlat(results_map_found):
    """Test if the correct long and lat returned for a country/city entity"""
    results = map(results_map_found)
    for res in results:
        if res['entity'] == 'malaysia':
            assert res['lat'] == 2.5
            assert res['long'] == 112.5
