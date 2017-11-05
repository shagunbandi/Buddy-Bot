import os, sys
from flask import Flask, request
from pymessenger import Bot

from utils.utils import wit_response
import utils.replies as reply

app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAADm8UzoVcoBABtKAE7osTrvare7jZBNEyK1N98Po37fhDmRHVRgMZCJ0dgbmepNfQcsusTTE7X36dumxOZCivMxrXC0tKrpUHOExwV1UVjSfHjG7086CmaQGU4Sh3VFoRVMyqMFYxWZCVNXIA8ZBmZCX9qPZBuHNhbmwbtRKOmDvPZCBZCyprjZAJXpN7zEMaSgMZD"


bot = Bot(PAGE_ACCESS_TOKEN)


@app.route('/', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "mycode":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200


def log(message):
    print(message)
    sys.stdout.flush()


def welcome_message():
    message = """
Welcome to the Buddy-Bot
---
It is easy to use messenger bot.
you can search for news of many categories.
just type in what you say and the NLP algorithm sitting behind it will do your tast.
---
Its currently in beta so you ay face few issues with it.
for any queries drop an email at shagunamitbandi@gmail.com
"""
    return message, 'text'


def get_response_and_type(messaging_text):
    # res_type, sub_type = wit_response(messaging_text)
    entity_response = wit_response(messaging_text)

    if entity_response['news'] is not None:
        return reply.news(entity_response['news']['newstype'])
    elif entity_response['greeting'] is not None:
        return reply.greeting()
    elif entity_response['thanks'] is not None:
        return reply.thanks()
    elif entity_response['bye'] is not None:
        return reply.bye()
    elif entity_response['okay'] is not None:
        return reply.general()
    elif entity_response['start'] is not None:
        return welcome_message()
    else:
        return reply.default()


def send_message(sender_id, response, response_type=None):
    if response_type == 'text':
        bot.send_text_message(sender_id, response)
    elif response_type == 'generic':
        bot.send_generic_message(sender_id, response)
    else:
        bot.send_text_message(sender_id, str(response))
    return


@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    log(data)
    try:
        if data['object'] == 'page':
            for entry in data['entry']:
                for msg_event in entry['messaging']:
                    sender_id = msg_event['sender']['id']
                    recipient_id = msg_event['recipient']['id']
                    if msg_event.get('message'):
                        if 'text' in msg_event['message']:
                            message_text = msg_event['message']['text']
                        else:
                            message_text = 'no text'

                        response, response_type = get_response_and_type(message_text)
                        send_message(sender_id, response, response_type)
    except:
        pass

    return "ok", 200


if __name__ == "__main__":
    app.run(debug=True, port=8080)
