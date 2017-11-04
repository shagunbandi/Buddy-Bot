from wit import Wit
import json

access_token = 'XN6J7Y5N3ILXII66ARXNOWDEIOJ3JQ3R'

client = Wit(access_token=access_token)
message = 'let it be'


def get_json(json_thing, sort=True, indents=4):
    json_thing = json_thing.decode('utf-8')
    if type(json_thing) is str:
        return json.dumps(json.loads(json_thing), sort_keys=sort, indent=indents)
    else:
        return json.dumps(json_thing, sort_keys=sort, indent=indents)


def wit_response(message):
    response = client.message(msg=message)
    what = None
    value = None
    try:
        what = response['entities']['intent'][0]['value']
    except:
        pass
    if what == 'get_my_location':
        try:
            value = response['entities']['location'][0]['value']
        except:
            pass
    elif what == 'news':
        try:
            value = response['entities']['category'][0]['value']
        except:
            pass
    elif what == 'general':
        value = None

    return what, value
