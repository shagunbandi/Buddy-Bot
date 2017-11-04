from wit import Wit
import json

access_token = 'STJOPOYXOVUVBD2QGW3GQ6T4CKFLAFOT'

client = Wit(access_token=access_token)


def get_json(json_thing, sort=True, indents=4):
    if type(json_thing) is str:
        return json.dumps(json.loads(json_thing), sort_keys=sort, indent=indents)
    else:
        return json.dumps(json_thing, sort_keys=sort, indent=indents)


def wit_response(message):
    response = client.message(msg=message)
    # print(get_json(response))
    type = None
    sub_type = None
    entities = response['entities']
    if len(entities):
        print('len satisfied')
        print(get_json(entities))
        # type = entities['type'][0]['value']
        # sub_type = entities['newstype'][0]['value']
        try:
            type = entities['type'][0]['value']
            print('type found {}'.format(type))
            if type == 'news':
                try:
                    sub_type = entities['newstype'][0]['value']
                    print('subtype found {}'.format(sub_type))
                except:
                    pass
        except:
            print('yaha')
            pass
    return type, sub_type


# message = 'Show me sports news'
# wit_response(message)