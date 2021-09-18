from wateraid.database import Database
from geocode.geocode import Geocode
from collections import Counter
from wordcloud import WordCloud, STOPWORDS
import base64
import io


def trends_map_query():
    """ Query to Results collection to find all entities in entire collection """
    results_found = Database.results.find(
        {}, {"query_results.results.enriched_text.entities": 1})
    return results_found


def trends_map(results_found):
    """ Create dictionary of 10 most common location entities 
        Includes location entity, frequency, longitude and latitude """
    map_list = []
    for res in results_found:
        for i in res['query_results']['results']:
            for j in i['enriched_text']['entities']:
                if j['type'] == 'Location':
                    map_list.append(j['text'])

    c = Counter(map_list)
    count = c.most_common(10)
    common_list = []
    for elem in count:
        common_list.append({'entity': elem[0], 'number': elem[1]})
    gc = Geocode()
    gc.load()
    for dict in common_list:
        try:
            entity = dict['entity']
            loc = gc.decode(entity)
            long = loc[0]['longitude']
            lat = loc[0]['latitude']
            dict['lat'] = lat
            dict['long'] = long
        except:
            pass
    map_markers = [item for item in common_list if 'lat' and 'long' in item]
    return map_markers


def concepts_query():
    """ Query to Results collection to find all concepts in entire collection """
    concepts_results = Database.results.find({},
                                             {"query_results.results.enriched_text.concepts.text": 1})
    return concepts_results


def find_concepts(concepts_results):
    """ Create a list of all concepts """
    concepts_list = []
    for res in concepts_results:
        for i in res['query_results']['results']:
            for x in i['enriched_text']['concepts']:
                concepts_list.append(x['text'])
    return concepts_list


def concepts_dataset(results_list):
    """ Create dictionary of 15 most common concepts, 
    including concept name and count """
    count_results = Counter(results_list)
    count = count_results.most_common(15)
    newdict = []
    for x in count:
        newdict.append({'Name': x[0], 'Count': x[1]})
    dataset = {"children": newdict}
    return dataset


def sentiment_query():
    """ Query to Results collection to find all sentiments in entire collection """
    sentiment_results = Database.results.find({},
                                              {"query_results.results.enriched_text.sentiment.document.label": 1})
    return sentiment_results


def find_sentiments(sentiment_results):
    """ Create a list of all sentiments """
    sentiment_list = []
    for res in sentiment_results:
        for i in res['query_results']['results']:
            sentiment_list.append(
                i['enriched_text']['sentiment']['document']['label'])
    return sentiment_list


def sentiment_dataset(sentiment_list):
    """ Create a list of number of positive, neutral and negative sentiments """
    count_values = Counter(sentiment_list)
    values_list = []
    values_list.append(count_values['positive'])
    values_list.append(count_values['neutral'])
    values_list.append(count_values['negative'])
    return values_list


def keywords_query():
    """ Query to Results collection to find all keywords in entire collection """
    keywords_results = Database.results.find(
        {}, {"query_results.results.enriched_text.keywords.text": 1})
    return keywords_results


def find_keywords(keywords_results):
    """ Create a string of all keywords """
    keywords_list = []
    for res in keywords_results:
        for i in res['query_results']['results']:
            for j in i['enriched_text']['keywords']:
                keywords_list.append(j['text'])
    keywords = ','.join(keywords_list)
    return keywords


def get_wordcloud(keywords):
    """ Create keywords WordCloud with top 30 words (font scaled to frequency)
        and return base64 image for display """
    cloud_img = WordCloud(max_words=30, width=600, height=400,
                          background_color='#dcf4ff', collocations=False,
                          stopwords=STOPWORDS).generate(text=keywords).to_image()
    img = io.BytesIO()
    cloud_img.save(img, "PNG")
    img.seek(0)
    img_b64 = base64.b64encode(img.getvalue()).decode()
    return img_b64


def search_terms_query():
    """ Query to Results collection to find all search terms in entire collection """
    search_terms_results = Database.results.find({}, {'search_term': 1})
    return search_terms_results


def find_search_terms(search_terms_results):
    """ Create search terms list all in lowercase """
    search_terms_list = []
    for res in search_terms_results:
        if res['search_term'] != '':
            search_terms_list.append(res['search_term'].lower())
    return search_terms_list


def search_terms_dataset(search_terms_list):
    """ Create list of top 5 most common search terms """
    count_list = Counter(search_terms_list)
    search_terms_count = count_list.most_common(5)
    search_terms = []
    for x in search_terms_count:
        search_terms.append({'term': x[0]})
    return search_terms


def languages_dataset():
    """ Create list of number of times each language filtered """
    language_count = []
    language_list = ['English', 'French',
                     'Spanish', 'German', 'Japanese', 'Korean']
    for lang in language_list:
        results_count = Database.results.count_documents({'language': lang})
        language_count.append(results_count)
    return language_count
