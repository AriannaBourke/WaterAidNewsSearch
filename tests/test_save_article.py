from wateraid.article.utils import insert_saved, set_button
from wateraid.article.utils import results, emotions
import pytest


@pytest.fixture
def results_found(Database):
    page_id = 'oNAQOkzYHTRdK_ciZe7_Qx4NahEqqL7licXiDmbzuF87NiNF8i8NKucQbIWY2EAO'
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


def test_set_button_unsave(Database):
    page_id = 'PAsJ6CGMv7ItDkZHjArg4AZsIpee7ndHaAiRS8rjoQsHKpCWkRGSAIOqXY5EzfuQ'
    userid = 'test@email.com'
    id = Database.saved.find_one({"results.results.id": page_id}, {
                                 'userid': 1, 'results.results.id': 1})
    assert set_button(page_id, userid, id) == 'unsave_button'


def test_set_button_save(Database):
    page_id = ''
    userid = 'test@email.com'
    id = Database.saved.find_one({"results.results.id": page_id}, {
                                 'userid': 1, 'results.results.id': 1})
    assert set_button(page_id, userid, id) == 'save_button'


def test_set_button_save2(Database):
    page_id = 'xyz'
    userid = 'test@email.com'
    id = Database.saved.find_one({"results.results.id": page_id}, {
                                 'userid': 1, 'results.results.id': 1})
    assert set_button(page_id, userid, id) == 'save_button'
