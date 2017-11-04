from wit import Wit
import json

access_token = 'XN6J7Y5N3ILXII66ARXNOWDEIOJ3JQ3R'

client = Wit(access_token=access_token)
# message = 'Kharagpur is where I live'


def pp_json(json_thing, sort=True, indents=4):
    if type(json_thing) is str:
        print(json.dumps(json.loads(json_thing), sort_keys=sort, indent=indents))
    else:
        print(json.dumps(json_thing, sort_keys=sort, indent=indents))
    return None


def wit_response(message):
    response = client.message(msg=message)
    # pp_json(response)
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

    return what, value


# print(wit_response(message))
