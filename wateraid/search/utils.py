from wateraid.database import Database
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import DiscoveryV1
from geocode.geocode import Geocode
from datetime import datetime, timedelta
from wateraid.config import Config
import sys

authenticator_discovery = IAMAuthenticator(
    Config.AUTHENTICATOR_DISCOVERY)
discovery = DiscoveryV1(
    version='2017-09-01',
    authenticator=authenticator_discovery
)
discovery.set_service_url(Config.DISCOVERY_SERVICE_URL)


def reference_lists():
    """ Reference lists for filter buttons: locations, languages, sources, popular terms, sentiments and date ranges """
    locations = ['Ethiopia', 'Rwanda', 'Tanzania', 'Uganda', 'Australia', 'Bangladesh',
                 'Cambodia', 'India', 'Japan', 'Kingdom of eSwantini', 'Madagascar', 'Malawi',
                 'Mozambique', 'South Africa', 'Zambia', 'Burkina Faso', 'Liberia', 'Mali',
                 'Niger', 'Nigeria', 'Senegal', 'Sierra Leone', 'Canada', 'Colombia',
                 'Nicaragua', 'United States', 'Myanmar', 'Nepal', 'Pakistan', 'Papua New Guinea',
                 'Timor-Leste', 'Sweden', 'United Kingdom']
    languages = [{'Language': 'French', 'Code': 'fr'},
                 {'Language': 'Spanish', 'Code': 'es'}, {
                     'Language': 'German', 'Code': 'de'},
                 {'Language': 'Japanese', 'Code': 'ja'}, {'Language': 'Korean', 'Code': 'ko'}]
    sources = [{'source': 'BBC News', 'web': 'bbc.co.uk'},
               {'source': 'The Guardian', 'web': 'theguardian.com'},
               {'source': 'The Independent', 'web': 'independent.co.uk'},
               {'source': 'WHO', 'web': 'who.int'},
               {'source': 'Pubmed', 'web': 'pubmed.ncbi.nlm.nih.gov'}, {
                   'source': 'The Economist', 'web': 'economist.com'},
               {'source': 'New Scientist', 'web': 'newscientist.com'}, {
                   'source': 'United Nations', 'web': 'un.org'},
               {'source': 'gov.uk', 'web': 'gov.uk'},
               {'source': 'Telegraph', 'web': 'telegraph.co.uk'},
               {'source': 'Sky News', 'web': 'news.sky.com'}]
    popular_terms = ['politics', 'economics', 'WASH',
                     'sanitation', 'hygiene', 'climate change', 'water']
    sentiments = ['positive', 'negative']
    dates = [{'Date': 'Past 24 Hours', 'Value': 'today'}, {
        'Date': 'Past Week', 'Value': '7'}, {'Date': 'Past Month', 'Value': '31'}]
    return locations, languages, sources, popular_terms, sentiments, dates


def map_query():
    """ Database query to Results collection to find entities for map. 
        Finds last inserted document (last search performed), 
        with projection fields including all necessary data for display"""
    results_map_found = Database.results.find({},
                                              {"query_results.results.enriched_text.entities": 1, 'query_results.results.id': 1,
                                               'query_results.results.title': 1, 'query_results.results.score': 1}).sort('_id', -1).limit(1)
    return results_map_found


def map(results_map_found):
    """ Generates a dictionary to plot map markers.
    Includes article id, titles, score, location entity, latitude and longitude """
    map_list = []
    for res in results_map_found:
        for i in res['query_results']['results']:
            id = i['id']
            title = i['title']
            score = i['score']
            for j in i['enriched_text']['entities']:
                if j['type'] == 'Location':
                    entity = j['text']
                    map_list.append({'id': id, 'title': title,
                                    'score': score, 'entity': entity})
    gc = Geocode()
    gc.load()
    for dict in map_list:
        try:
            entity = dict['entity']
            loc = gc.decode(entity)
            long = loc[0]['longitude']
            lat = loc[0]['latitude']
            dict['lat'] = lat
            dict['long'] = long
        except:
            pass
    map_markers = [item for item in map_list if 'lat' and 'long' in item]
    return map_markers


def results_query():
    """ Find query to Results collection to find last inserted document (last search perfomed).
        Includes projection fields for all data relevant for display
        and count of number of articles in the results array """
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
    count = (len(results_found[0]['query_results']['results']))
    return results_found, count


def results_list_sets(results_found):
    """ Creates list of search results and sets of concepts, organisation entities and people entities """
    concepts_list = []
    entities_list_org = []
    entities_list_ppl = []
    results_list = []
    for res in results_found:
        results_list.append(res['query_results']['results'])
        for i in res['query_results']['results']:
            for j in i['enriched_text']['entities'][0:3]:
                if j['type'] == 'Person':
                    entities_list_ppl.append(j['text'])
                if j['type'] == 'Organization':
                    entities_list_org.append(j['text'])
        for i in res['query_results']['results']:
            for j in i['enriched_text']['concepts'][0:2]:
                concepts_list.append(j['text'])

    for dict in results_list[0]:
        date = dict['publication_date'][0:10]
        to_date = datetime.strptime(date, '%Y-%m-%d')
        format_date = datetime.strftime(to_date, '%d %b %Y')
        dict['publication_date'] = format_date
    concepts_set = set(concepts_list)
    entities_set_org = set(entities_list_org)
    entities_set_ppl = set(entities_list_ppl)
    return concepts_set, entities_set_ppl, entities_set_org, results_list


def filter_query(search, language, filter):
    """ Watson Discovery query with user input search term, language of collection and filter paramters """
    try:
        query_results = discovery.query(
            environment_id='system',
            collection_id=language,
            natural_language_query=search,
            deduplicate=True,
            count=50,
            filter=filter
        ).get_result()
    except:
        query_results = ''
    return query_results


def insert_results(query_results, search, filter, language):
    """ Insert search results into Results collection  """
    today_date = datetime.now().date().strftime("%Y-%m-%d")
    Database.results.insert_one({'search_term': search, 'date': today_date,
                                 'filter': filter, 'language': language, 'query_results': query_results})


def filter_parameters(concept_form, entities_form, sentiment_form,
                      date_form, lang_form, loc_form, source_form, wateraid_form):
    """ Create string of filter parameters for Watson query and for URL/display """
    filter_list = []
    url_filter_list = []
    no_wateraid(wateraid_form, filter_list, url_filter_list)
    concept_filters(concept_form,  filter_list, url_filter_list)
    entities_filters(entities_form, filter_list, url_filter_list)
    sentiment_filters(sentiment_form, filter_list, url_filter_list)
    date_filters(date_form, filter_list, url_filter_list)
    language_filters(lang_form, url_filter_list)
    location_filters(loc_form, filter_list, url_filter_list)
    source_filters(source_form, filter_list, url_filter_list)
    filter = ','.join(filter_list)
    url_filters = ', '.join(url_filter_list)
    return filter, url_filters


def search_input(search_form):
    """ Convert user input search term to string """
    if search_form == []:
        input_search = ''
    else:
        for x in search_form:
            input_search = x
    return input_search


def no_wateraid(wateraid_form, filter_list, url_filter_list):
    """ If No WaterAid button selected, create filter parameter string to eliminate results with
        entites, keywords, title and concepts of WaterAid """
    if wateraid_form == []:
        pass
    else:
        wateraid_string = 'enriched_text.entities.text:!"WaterAid", enriched_text.keywords.text:!"WaterAid", title:!"WaterAid", enriched_text.concepts.text:!"WaterAid"'
        filter_list.append(wateraid_string)
        url_filter_list.append('No Wateraid')
        return wateraid_string


def concept_filters(concept_form, filter_list, url_filter_list):
    """ Create filter parameter string for concepts chosen """
    if concept_form == []:
        pass
    else:
        for concept in concept_form:
            concept_string = 'enriched_text.concepts.text:'+concept
            filter_list.append(concept_string)
            url_filter_list.append(concept)
        return concept_string


def entities_filters(entities_form, filter_list, url_filter_list):
    """ Create filter parameter string for entites chosen """
    if entities_form == []:
        pass
    else:
        for entities in entities_form:
            entities_string = 'enriched_text.entities.text:'+entities
            filter_list.append(entities_string)
            url_filter_list.append(entities)
        return entities_string


def sentiment_filters(sentiment_form, filter_list, url_filter_list):
    """ Create filter parameter string for sentiment chosen """
    if sentiment_form == []:
        pass
    else:
        for sent in sentiment_form:
            sentiment_string = 'enriched_text.sentiment.document.label::'+sent
            filter_list.append(sentiment_string)
            url_filter_list.append(sent)
        return sentiment_string


def date_filters(date_form, filter_list, url_filter_list):
    """ Create filter parameter string for date range chosen """
    dates = [{'Date': 'Past 24 Hours', 'Value': 'today'}, {
        'Date': 'Past Week', 'Value': '7'}, {'Date': 'Past Month', 'Value': '31'}]
    if date_form == []:
        pass
    else:
        for date in date_form:
            if date == 'Past 24 Hours':
                date_today = datetime.today()
                today = datetime.strftime(date_today, '%Y-%m-%d')
                date_string = 'publication_date::'+today
                filter_list.append(date_string)
                url_filter_list.append(date)
                return date_string
            else:
                for x in dates:
                    if date == x['Date']:
                        date_value = x['Value']
                        start_date = datetime.today().date()
                        end_date = datetime.today().date() - timedelta(days=int(date_value))
                        start = str(start_date)
                        end = str(end_date)
                        date_string = "publication_date>"+end+",publication_date<"+start
                        filter_list.append(date_string)
                        url_filter_list.append(x['Date'])
                return date_string


def language_filters(lang_form, url_filter_list):
    """ Create filter parameter string for language chosen """
    languages = [{'Language': 'French', 'Code': 'fr'},
                 {'Language': 'Spanish', 'Code': 'es'}, {
                     'Language': 'German', 'Code': 'de'},
                 {'Language': 'Japanese', 'Code': 'ja'}, {'Language': 'Korean', 'Code': 'ko'}]
    if lang_form == []:
        pass
    else:
        for lang in lang_form:
            for x in languages:
                if lang == x['Language']:
                    url_filter_list.append(lang)
        return lang


def language_query(lang_form):
    """ Create string for Watson query with chosen """
    languages = [{'Language': 'French', 'Code': 'fr'},
                 {'Language': 'Spanish', 'Code': 'es'}, {
                     'Language': 'German', 'Code': 'de'},
                 {'Language': 'Japanese', 'Code': 'ja'}, {'Language': 'Korean', 'Code': 'ko'}]
    if lang_form == []:
        language = 'news-en'
        return language
    else:
        for lang in lang_form:
            for x in languages:
                if lang == x['Language']:
                    language = 'news-'+x['Code']
        return language


def location_filters(loc_form, filter_list, url_filter_list):
    """ Create filter parameter string for locations chosen """
    if loc_form == []:
        pass
    else:
        for loc in loc_form:
            location_string = 'enriched_text.entities.text::'+loc
            filter_list.append(location_string)
            url_filter_list.append(loc)
        return location_string


def source_filters(source_form, filter_list, url_filter_list):
    """ Create filter parameter string for sources chosen """
    sources = [{'source': 'BBC News', 'web': 'bbc.co.uk'},
               {'source': 'The Guardian', 'web': 'theguardian.com'},
               {'source': 'The Independent', 'web': 'independent.co.uk'},
               {'source': 'WHO', 'web': 'who.int'},
               {'source': 'Pubmed', 'web': 'pubmed.ncbi.nlm.nih.gov'}, {
        'source': 'The Economist', 'web': 'economist.com'},
        {'source': 'New Scientist', 'web': 'newscientist.com'}, {
        'source': 'United Nations', 'web': 'un.org'},
        {'source': 'gov.uk', 'web': 'gov.uk'},
        {'source': 'Telegraph', 'web': 'telegraph.co.uk'},
        {'source': 'Sky News', 'web': 'news.sky.com'}]
    if source_form == []:
        pass
    else:
        for source in source_form:
            for x in sources:
                if source == x['source']:
                    source_string = 'host:'+x['web']
                    filter_list.append(source_string)
                    url_filter_list.append(source)
        return source_string


def language_db(lang_form):
    """ Create string for database insertion for language chosen """
    if lang_form == []:
        language_str = 'English'
    else:
        language_str = ','.join(lang_form)
    return language_str
