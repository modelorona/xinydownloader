# completly abstracts the sending to the firebase database
import json

import requests


def send_to_db(location, data):
    code = requests.put('https://xinyu-9c4c9.firebaseio.com/'+location+'.json', json.dumps(data))
    return code

