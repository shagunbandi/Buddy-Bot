import urllib.request
import json
import requests
from .utils import get_json

#
# def get_json(json_thing, sort=True, indents=4):
#     if type(json_thing) is str:
#         return json.dumps(json.loads(json_thing), sort_keys=sort, indent=indents)
#     else:
#         return json.dumps(json_thing, sort_keys=sort, indent=indents)


# https://newsapi.org/
NEWS_API_KEY = 'f2c2c4c7f5f449b5bb4f46e448c391dc'


def get_news_element_messenger_format(all_articles):
    news_elements = []
    for art in all_articles:
        element = {
            'title': art['title'],
            'subtitle': art['description'][:79],
            'buttons': [{
                'type': 'web_url',
                'title': 'Read More',
                'url': art['url']
            }],
            'image_url': art['image_url']
        }
        news_elements.append(element)
    return news_elements


'''
Main Reply
'''


def location(value):
    if value:
        response = 'Cool, Now I know you are from {}'.format(value)
    else:
        response = 'I see, you want to tell me something about location, sorry please use simpler language'
    return response, 'text'


def news(value):
    source = {
        'sports': 'talksport',
        'entertainment': 'buzzfeed',
        'business': 'business-insider',
        'politics': 'breitbart-news',
        'music': 'mtv-news',
        'tech': 'recode',
    }.get(value, 'the-times-of-india')
    try:
        url = 'https://newsapi.org/v1/articles?source=' + source + '&sortBy=latest&apiKey=' + NEWS_API_KEY
        response = urllib.request.urlopen(url).read()
    except:

        # For Recode API sortBY Top required
        try:
            url = 'https://newsapi.org/v1/articles?source=' + source + '&sortBy=top&apiKey=' + NEWS_API_KEY
            response = urllib.request.urlopen(url).read()
        except:
            return None, 'text'

    # For TOI API decode is required
    try:
        response = response.decode('utf-8')
    except:
        pass
    response = get_json(response)
    print(response)
    response = json.loads(response)
    all_articles = []
    if response['status'] == 'ok':
        articles = response['articles']
        for art in articles:
            article = {
                'title': art['title'],
                'description': art['description'],
                'author': art['author'],
                'publishedAt': art['publishedAt'],
                'image_url': art['urlToImage'],
                'url': art['url']
            }
            all_articles.append(article)

        return get_news_element_messenger_format(all_articles), 'generic'
    return 'Sorry, cannot get new for {}'.format(value), 'text'


def general(*args):
    response = 'okay then'
    return response, 'text'


def default():
    return 'Sorry', 'text'