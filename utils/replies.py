import urllib.request
import json
from .utils import get_json


# https://newsapi.org/
NEWS_API_KEY = 'f2c2c4c7f5f449b5bb4f46e448c391dc'


def get_news_element_messenger_format(news_json):
    news_elements = []
    if news_json['status'] == 'ok':
        articles = news_json['articles']
        for art in articles:
            title = art['title']
            body = art['description']
            image_url = art['urlToImage']
            url = art['url']

            element = {
                'title': title,
                'subtitle': body[:70],
                'buttons': [{
                    'type': 'web_url',
                    'title': 'Read More',
                    'url': url
                }],
                'image_url': image_url
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
    url = 'https://newsapi.org/v1/articles?source=the-times-of-india&sortBy=top&apiKey='+NEWS_API_KEY
    response = urllib.request.urlopen(url).read()
    response = get_json(response)
    response = json.loads(response)
    # print(response.keys())

    return get_news_element_messenger_format(response), 'generic'

    # if value:
    #     response = 'Bringin News with the category {} right away'.format(value)
    # else:
    #     response = 'Bringing you news right away'
    # return response


def general(*args):
    response = 'okay then'
    return response, 'text'
