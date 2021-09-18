from flask import Blueprint, render_template
from flask_login import login_required
from wateraid.database import Database
from datetime import datetime
from wateraid.trends.utils import concepts_query, find_keywords, find_search_terms, find_sentiments, keywords_query, languages_dataset, search_terms_dataset, search_terms_query, sentiment_dataset, sentiment_query, trends_map, find_concepts, concepts_dataset, find_keywords, get_wordcloud, trends_map_query

trends_blueprint = Blueprint('trends_blueprint', __name__)


@trends_blueprint.route("/trends", methods=['GET', 'POST'])
@login_required
def trends():
    # create concepts dataset
    concepts_results = concepts_query()
    results_list = find_concepts(concepts_results)
    dataset = concepts_dataset(results_list)

    # create sentiment list
    sentiment_results = sentiment_query()
    sentiment_list = find_sentiments(sentiment_results)
    values_list = sentiment_dataset(sentiment_list)

    # number of searches
    search_count = Database.results.estimated_document_count()

    # number of searches today
    todays_date = datetime.now().date().strftime("%Y-%m-%d")
    count_today = Database.results.count_documents({'date': todays_date})

    # number of registered users
    users_count = Database.reg_users.estimated_document_count()

    # create locations map markers
    map_results = trends_map_query()
    map_markers = trends_map(map_results)

    # keywords wordcloud
    keywords_results = keywords_query()
    keywords = find_keywords(keywords_results)
    try:
        keywords_cloud = get_wordcloud(keywords)
    except:
        keywords_cloud = []

    # common search terms
    search_terms_results = search_terms_query()
    search_terms_list = find_search_terms(search_terms_results)
    search_terms = search_terms_dataset(search_terms_list)

    # create languages dataset
    language_count = languages_dataset()

    return render_template('trends.html', concepts=dataset, sentiment=values_list,
                           search_count=search_count, longlat=map_markers, keywords_cloud=keywords_cloud, search_terms=search_terms,
                           users_count=users_count, count_today=count_today, language_count=language_count)
