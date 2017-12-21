# completly abstracts the sending to the firebase database
import requests
import json


def send_to_db(location, data):
    code = requests.put('https://xinyu-9c4c9.firebaseio.com/'+location+'.json', json.dumps(data))
    return code

