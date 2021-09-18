from wateraid.database import Database
from wateraid.config import Config
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EmotionOptions
from datetime import datetime

authenticator_NLU = IAMAuthenticator(Config.AUTHENTICATOR_NLU)
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2020-08-01',
    authenticator=authenticator_NLU
)
natural_language_understanding.set_service_url(Config.NLU_SERVICE_URL)


def article_query(page_id):
    """ Database query to find single article in Results table and extract it from the array,
        includes projection fields of all necessary data for display """
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


def results(results_found):
    """ Create results list of article data and format publication date """
    results_list = []
    for res in results_found:
        results_list.append(res['results'][0])
        for i in res['results']:
            date = (i['publication_date'][0:10])
            to_date = datetime.strptime(date, '%Y-%m-%d')
            format_date = datetime.strftime(to_date, '%d %b %Y')
    return results_list, format_date


def emotions(results_list):
    """ Watson NLU analysis of emotion of article """
    try:
        found_emotions = {}
        article = results_list[0]['url']
        response = natural_language_understanding.analyze(
            url=article,
            features=Features(emotion=EmotionOptions()))
        nlu_results = response.get_result()
        found_emotions = nlu_results['emotion']['document']['emotion']
    except:
        found_emotions = {}
    return found_emotions


def save_article_query(page_id):
    """ Database query to find single article in Results table and extract it from the array,
    includes projection fields of all necessary data for display """
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


def insert_saved(results_found, userid):
    """ Insert article into Saved collection of database """
    results_into = list(results_found)
    Database.saved.insert_one({'userid': userid, 'results': results_into})


def delete_article(page_id, userid):
    """ Delete article from Saved collection of database """
    Database.saved.remove({"results.results.id": page_id, 'userid': userid})


def button_query(page_id):
    """ Find if article exists in Saved collection in database to 
        determine if it has already been saved """
    id = Database.saved.find_one({"results.results.id": page_id}, {
                                 'userid': 1, 'results.results.id': 1})
    return id


def set_button(page_id, userid, id):
    """ Set button as save/unsave """
    if id == None:
        button = 'save_button'
    else:
        if id['userid'] == userid and page_id == id['results'][0]['results'][0]['id']:
            button = 'unsave_button'
        else:
            if id['userid'] != userid and page_id and id['results'][0]['results'][0]['id']:
                button = 'save_button'
    return button
