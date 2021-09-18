from datetime import datetime
from wateraid.database import Database
from flask_paginate import Pagination, get_page_args
import re


def account_pagination(results_found, userid):
    """ Pagination to display 10 articles per page from articles saved by a user """
    doc_count = Database.saved.count_documents({'userid': userid})
    page, per_page, offset = get_page_args()
    page_results = results_found.limit(per_page).skip(offset)
    pagination = Pagination(page=page, per_page=per_page, offset=offset,
                            total=doc_count,
                            css_framework='bootstrap4')
    return pagination


def results(results_found):
    """ Creation of a list of the results with date formatted from 
    Watson Discovery query to find all articles save by a user """
    results_list = []
    for res in results_found:
        results_list.append(res)
    format_date(results_list)
    return results_list


def format_date(results_list):
    """ Format the publication date of all articles in the results list 
    as day, month name, year eg 01 Sep 2021 """
    for dict in results_list:
        for i in dict['results']:
            for j in i['results']:
                date = (j['publication_date'][0:10])
                to_date = datetime.strptime(date, '%Y-%m-%d')
                format_date = datetime.strftime(to_date, '%d %b %Y')
                j['publication_date'] = format_date
    return results_list


def keywords_results(userid, search):
    """ Create a list of keywords from articles saved by a user to allow for a keyword search """
    keywords_list = []
    results_found = Database.saved.find(
        {"userid": userid, "results.results.enriched_text.keywords.text":  re.compile(search, re.IGNORECASE)})
    for res in results_found:
        keywords_list.append(res)
    return keywords_list


def no_duplicates(results_found, keywords_list):
    """ Create a results list from keyword search, remove duplicate articles and format date """
    results_list = []
    for res in results_found:
        for dict in keywords_list:
            if res['_id'] == dict['_id']:
                pass
            else:
                keywords_list.append(res)
    for i in keywords_list:
        if i not in results_list:
            results_list.append(i)
    format_date(results_list)
    return results_list


def delete_article(delete, userid):
    """ Delete articles from the Saved database collection """
    Database.saved.remove({"results.results.id": delete, 'userid': userid})
