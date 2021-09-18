from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from wateraid.search.utils import map_query, results_list_sets, results_query, language_db, map, filter_query, reference_lists, insert_results, search_input, language_query, filter_parameters

search_blueprint = Blueprint('search_blueprint', __name__)


@search_blueprint.route('/search_results', methods=['GET', 'POST'])
@login_required
def search_results():
    search = request.args.get('search', None)
    filter = request.args.get('filter', None)
    locations, languages, sources, popular_terms, sentiments, dates = reference_lists()
    if search == None:
        concepts_list, entities_list_ppl, entities_list_org, results_list = [], [], [], []
        count = 0
        map_tags = None
    else:
        # Get the last inserted search result in databse
        results_found, count = results_query()
        # create results lists and sets for template
        concepts_list, entities_list_ppl, entities_list_org, results_list = results_list_sets(
            results_found)
        # create map with markers
        results_map_found = map_query()
        map_tags = map(results_map_found)

    # Performing a new seach from the search results page, with no filters
    if request.method == "POST" and "new_search" in request.form:
        search = request.form.get("new_search")
        filter = ''
        language = 'news-en'
        language_str = 'English'
        # query Watson with search parameters
        query_results = filter_query(search, language, filter)
        # Insert result into database
        insert_results(query_results, search, filter, language_str)
        return redirect(url_for('search_blueprint.search_results', search=search))

     # advanced search
    if request.method == "POST" and 'filter_form' in request.form:
        search_form = request.form.getlist('search_form')
        concept_form = request.form.getlist('concept_form')
        entities_form = request.form.getlist('entities_form')
        sentiment_form = request.form.getlist('sentiment_form')
        date_form = request.form.getlist('date_form')
        lang_form = request.form.getlist('lang_form')
        loc_form = request.form.getlist('locations_form')
        source_form = request.form.getlist('source_form')
        wateraid_form = request.form.getlist('wateraid_form')

        # Get search in string format for database insertion
        input_search = search_input(search_form)
        # Get language in Watson query format
        language = language_query(lang_form)
        # Get language in database format (string)
        language_str = language_db(lang_form)
        # create filter parameter strings for Watson query and template display
        filter, url_filters = filter_parameters(concept_form, entities_form,
                                                sentiment_form, date_form, lang_form, loc_form, source_form, wateraid_form)
        # Query Watson with filters
        query_results = filter_query(input_search, language, filter)
        # Insert results to database
        insert_results(query_results, input_search, url_filters, language_str)
        return redirect(url_for('search_blueprint.search_results', search=input_search, filter=url_filters))

    if request.method == "POST" and "map_term" in request.form:
        map_term = request.form.get("map_term")
        # create location and language fields for Watson query
        location = 'enriched_title.entities.text::'+map_term
        language = 'news-en'
        # Query Watson
        query_results = filter_query(search, language, location)
        # Insert result to database
        language_str = 'English'
        insert_results(query_results, search, map_term, language_str)
        return redirect(url_for('search_blueprint.search_results', search=search, filter=map_term))

    return render_template('search_results.html', search_results=results_list, title='Search Results', search=search, longlat=map_tags,
                           count=count, locations=locations, filter=filter, languages=languages, sources=sources, popular_terms=popular_terms,
                           sentiments=sentiments, dates=dates, concepts=concepts_list, entities_ppl=entities_list_ppl,
                           entities_org=entities_list_org)
