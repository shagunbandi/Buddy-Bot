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

    entity_response = {
        'news': None,
        'greeting': None,
        'thanks': None,
        'bye': None,
        'okay': None,
        'start': None
    }

    if response['_text'] == '/start':
        entity_response['start'] = True
        return entity_response

    entities = response['entities']

    print(get_json(response))

    if len(entities):
        # print(get_json(entities))

        # For Type
        try:
            type = entities['type'][0]['value']

            # For News Type

            if type == 'news':
                try:
                    sub_type = entities['newstype'][0]['value']
                    entity_response['news'] = {
                        'newstype_found': True,
                        'newstype': sub_type
                    }
                except:
                    entity_response['news'] = {
                        'newstype_found': False,
                        'newstype': None
                    }
                return entity_response

            # For Ok

            if type == 'okay':
                entity_response['okay'] = True
                return entity_response

        except:
            pass

        # For Greetings
        try:
            greeting = entities['greetings'][0]['value']
            if greeting:
                entity_response['greeting'] = True
                return entity_response
        except:
            pass

        # For Thanks
        try:
            thanks = entities['thanks'][0]['value']
            if thanks:
                entity_response['thanks'] = True
                return entity_response
        except:
            pass

        # For Bye
        try:
            bye = entities['bye'][0]['value']
            if bye:
                entity_response['bye'] = True
                return entity_response
        except:
            pass



    return entity_response


# message = 'Show me sports news'
# wit_response(message)