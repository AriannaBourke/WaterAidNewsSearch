from wateraid.search.utils import concept_filters, date_filters, language_filters, location_filters, no_wateraid, search_input, language_query, language_db, filter_parameters, entities_filters, sentiment_filters, source_filters, results_list_sets
import pytest


@pytest.fixture
def test_query(query_results, Database):
    Database.results.insert_one({'query_results': query_results})


@pytest.fixture
def results_found(Database):
    """ Database query to find last inserted search results set up """
    results_found = Database.results.find({},
                                          {"query_results.results.enriched_text.concepts.text": 1,
                                           "query_results.results.enriched_text.entities": 1,
                                           'query_results.results.publication_date': 1,
                                           'query_results.results.title': 1,
                                           'query_results.results.text': 1,
                                           'query_results.results.host': 1,
                                           'query_results.results.score': 1,
                                           'query_results.results.id': 1,
                                           }).sort('_id', -1).limit(1)
    return results_found


def test_results_sets(results_found):
    """Test output is a set (no duplicates) and contains relevant concepts"""
    res = results_list_sets(results_found)
    assert isinstance(res[0], set)
    assert 'Water' in res[0]
    assert isinstance(res[1], set)
    assert isinstance(res[2], set)


def test_results_sets_date(results_found):
    res = results_list_sets(results_found)
    """ Test date in correct format and output is a list """
    assert '09 Sep 2021' in res[3][0][0]['publication_date']
    assert isinstance(res[3], list)


def test_context(app):
    """ Test url path correct with search term input"""
    from flask import request
    with app.test_request_context('/search_results?search=water+shortage'):
        assert request.path == '/search_results'
        assert request.args['search'] == 'water shortage'


def test_search_form():
    """ Test input search term output correct when empty or with input"""
    assert search_input([]) == ''
    assert search_input(['search']) == 'search'


def test_no_wateraid():
    """ Test no wateraid filter output correct when empty or with input"""
    assert no_wateraid([], [], []) == None
    assert no_wateraid(['no wateraid'], [], []) == """enriched_text.entities.text:!"WaterAid", 
                                                    enriched_text.keywords.text:!"WaterAid", 
                                                    title:!"WaterAid", enriched_text.concepts.text:!"WaterAid" 
                                                    """


def test_concept_filters():
    """ Test concepts filter output correct when empty or with input"""
    assert concept_filters([], [], []) == None
    assert concept_filters(
        ['concept'], [], []) == 'enriched_text.concepts.text:concept'


def test_entities_filters():
    """ Test entities filter output correct when empty or with input"""
    assert entities_filters([], [], []) == None
    assert entities_filters(
        ['entity'], [], []) == 'enriched_text.entities.text:entity'


def test_sentiment_filters():
    """ Test sentiment filter output correct when empty or with input"""
    assert sentiment_filters([], [], []) == None
    assert sentiment_filters(
        ['positive'], [], []) == 'enriched_text.sentiment.document.label::positive'


def test_date_filters_today():
    """ Test todays date output correct when empty or with input"""
    from datetime import datetime
    date_today = datetime.today()
    today = datetime.strftime(date_today, '%Y-%m-%d')
    assert date_filters([], [], []) == None
    assert date_filters(['Past 24 Hours'], [], []
                        ) == 'publication_date::'+today


def test_date_filters_week():
    """ Test past week date filter output correct when empty or with input"""
    from datetime import datetime, timedelta
    start_date = datetime.today().date()
    end_date = datetime.today().date() - timedelta(days=int(7))
    start = str(start_date)
    end = str(end_date)
    assert date_filters([], [], []) == None
    assert date_filters(['Past Week'], [], []
                        ) == "publication_date>"+end+",publication_date<"+start


def test_language_filters():
    """ Test language filter string output correct when empty or with input"""
    assert language_filters([], []) == None
    assert language_filters(['Spanish'], []) == 'Spanish'


def test_language_query():
    """ Test language query filter output correct when empty or with input"""
    assert language_query([]) == 'news-en'
    assert language_query(['French']) == 'news-fr'


def test_location_filters():
    """ Test locations filter output correct when empty or with input"""
    assert location_filters([], [], []) == None
    assert location_filters(
        ['France'], [], []) == 'enriched_text.entities.text:France'


def test_source_filters():
    """ Test source filter output correct when empty or with input"""
    assert source_filters([], [], []) == None
    assert source_filters(['BBC News'], [], []) == 'host:bbc.co.uk'


def test_language_db():
    """ Test language output for database correct when empty or with input"""
    assert language_db([]) == 'English'
    assert language_db(['French']) == 'French'


def test_filter_parameters_empty():
    """ Test filters output correct when empty"""
    filters = filter_parameters([], [], [], [], [], [], [], [])
    assert isinstance(filters[0], str)
    assert isinstance(filters[1], str)
    assert filters[0] == ''
    assert filters[1] == ''


def test_filter_parameters_one():
    """ Test filters output correct with one input"""
    filters_included = filter_parameters(
        ['concept'], [], [], [], [], [], [], [])
    assert filters_included[0] == 'enriched_text.concepts.text:concept'
    assert filters_included[1] == 'concept'


def test_filter_parameters_multi():
    """ Test filters output correct with multiple inputs"""
    filters_included = filter_parameters(
        ['Water'], [], ['positive'], [], [], [], [], [])
    assert filters_included[0] == """enriched_text.concepts.text:Water,
                                enriched_text.sentiment.document.label::positive"""
    assert filters_included[1] == 'Water, positive'
