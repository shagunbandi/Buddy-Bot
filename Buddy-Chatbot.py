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


def get_response_and_type(messaging_text):
    what, value = wit_response(messaging_text)

    response = {
        'get_my_location': reply.location(value),
        'news': reply.news(value),
        'general': reply.general(value)
    }.get(what, ('Sorry', 'text'))
    return response


def send_message(sender_id, response, response_type=None):
    if response_type == 'text':
        bot.send_text_message(sender_id, response)
    elif response_type == 'generic':
        bot.send_generic_message(sender_id, response)
    else:
        bot.send_text_message(sender_id, str(response))
    return
    # execute = {
    #     'text': bot.send_text_message(sender_id, response),
    #     'generic': bot.send_generic_message(sender_id, response),
    # }.get(response_type, bot.send_text_message(sender_id, str(response)))


@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    log(data)

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

    return "ok", 200


if __name__ == "__main__":
    app.run(debug=True, port=8080)
