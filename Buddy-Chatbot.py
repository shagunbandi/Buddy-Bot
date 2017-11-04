import os, sys
from flask import Flask, request
from pymessenger import Bot
from utils import wit_response


app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAADm8UzoVcoBALclzCszW4YBcklqUWhYY37fxL3CcZAL3gUNufq6ih1jKsNXLPBd8imqntwo2OkYAoRk7EaZBXRdrrE9yc20bHedvSdaNkKODKfDsbQgbjo8xF7bBZC3ZC1Apzjl8Nd7EFShuzZBWZCEwyKS2bT4qreW3xPYDxaaueJZCCZCxkaac7F2JU9s1LsZD"

bot = Bot(PAGE_ACCESS_TOKEN)


@app.route('/', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "mysecretpasswordisthissothatyoucannotguessitunlessyouseethecode":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200


def log(message):
    print(message)
    sys.stdout.flush()


def get_response(messaging_text):
    response = None
    what, value = wit_response(messaging_text)
    if value:
        if what == 'get_my_location':
            response = 'Cool, Now I know you are from {}'.format(value)
        elif what == 'news':
            response = 'Bringin News with the category {} right away'.format(value)
        else:
            response = 'Could not get that... sorry'
    else:
        if what == 'get_my_location':
            response = 'I see, you want to tell me something about location, sorry please use simpler language'
        elif what == 'news':
            response = 'Bringing you news right away'
        else:
            response = 'Could not get that... sorry'
    return response


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
                        messaging_text = msg_event['message']['text']
                    else:
                        messaging_text = 'no text'

                    response = get_response(messaging_text)

                    bot.send_text_message(sender_id, response)

    return "ok", 200


if __name__ == "__main__":
    app.run(debug=True, port=8080)
